import os
import re
import glob
import calendar
from datetime import datetime, timedelta
from utils.file_handler import ensure_directory_exists, read_file
from utils.openai_handler import OpenAIHandler

class WeeklyProcessor:
    """Process weekly journal data using multiple prompts."""
    
    def __init__(self, config, openai_handler=None):
        """Initialize the weekly processor with configuration."""
        self.config = config
        self.output_dir = config.get('OUTPUT_DIR')
        self.weekly_results_path = config.get('WEEKLY_RESULTS_PATH', 'weekly')
        self.weekly_prompts = self._parse_weekly_prompts(config.get('WEEKLY_PROMPTS', ''))
        self.openai = openai_handler or OpenAIHandler(config)
    
    def _parse_weekly_prompts(self, prompts_str):
        """Parse comma-separated list of weekly prompts into a list."""
        if not prompts_str:
            return []
        return [prompt.strip() for prompt in prompts_str.split(',')]
    
    def _get_prompt_path(self, prompt_filename):
        """Get the full path to a prompt template."""
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates', prompt_filename)
    
    def _load_prompt_template(self, prompt_filename):
        """Load a prompt template from file."""
        prompt_path = self._get_prompt_path(prompt_filename)
        print(f"\nLoading weekly prompt template: {prompt_path}")
        try:
            with open(prompt_path, 'r') as file:
                template = file.read()
            print(f"✓ Loaded prompt template ({len(template)} chars)")
            return template
        except Exception as e:
            print(f"❌ Error loading prompt template {prompt_filename}: {e}")
            return None
    
    def _get_week_number(self, date_str):
        """Get the week number (01-53) for a given date string."""
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            week_num = date_obj.isocalendar()[1]
            return f"{week_num:02d}"  # Format as 01, 02, etc.
        except ValueError:
            print(f"❌ Invalid date format: {date_str}")
            return "00"
    
    def _get_dates_for_week(self, date_str):
        """Get all 7 dates in the week that contains the given date."""
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            # Get the Monday of the week
            start_of_week = date_obj - timedelta(days=date_obj.weekday())
            # Get all 7 days of the week
            week_dates = [
                (start_of_week + timedelta(days=i)).strftime('%Y-%m-%d') 
                for i in range(7)
            ]
            return week_dates
        except ValueError:
            print(f"❌ Invalid date format: {date_str}")
            return []
    
    def _check_week_has_any_data(self, week_dates, existing_files):
        """Check if at least one day in the week has a journal entry."""
        for date in week_dates:
            if date in existing_files:
                return True
        return False
    
    def _collect_weekly_data(self, week_dates, existing_files):
        """Collect data from all journal entries in the week."""
        print(f"\nCollecting data for week with dates: {', '.join(week_dates)}")
        weekly_data = {}
        
        for date in week_dates:
            if date in existing_files:
                try:
                    file_path = existing_files[date]
                    content = read_file(file_path)
                    weekly_data[date] = content
                    print(f"✓ Loaded data for {date}")
                except Exception as e:
                    print(f"❌ Error reading data for {date}: {e}")
                    weekly_data[date] = f"Error reading data: {e}"
            else:
                print(f"⚠️ Missing data for {date}")
                weekly_data[date] = "No data available for this date"
        
        return weekly_data
    
    def _format_weekly_data(self, weekly_data):
        """Format the weekly data for use in prompt templates."""
        formatted_data = ""
        for date, content in sorted(weekly_data.items()):
            formatted_data += f"\n\n--- {date} ---\n{content}"
        return formatted_data
    
    def _save_weekly_result(self, week_number, prompt_name, content):
        """Save the weekly result to a file."""
        # Get the base filename without extension
        base_name = os.path.splitext(prompt_name)[0]
        
        # Get all dates in the week
        week_dates = self._get_dates_for_week(week_number)
        
        if week_dates:
            # Get the last date of the week (Sunday)
            last_date = datetime.strptime(week_dates[-1], '%Y-%m-%d')
            
            # Format the filename: YYYY-Sunday-Month-DD-template.md
            year = last_date.strftime("%Y")
            day_name = last_date.strftime("%A")  # Sunday
            month = last_date.strftime("%B")     # May
            day = last_date.strftime("%d")       # 23
            
            filename = f"{year}-{day_name}-{month}-{day}-{base_name}.md"
        else:
            # Fallback in case week_dates is empty
            print("⚠️ Could not determine week dates, using fallback filename")
            filename = f"unknown-date-{base_name}.md"
        
        # Check if weekly_results_path is absolute or relative
        if os.path.isabs(self.weekly_results_path):
            # If it's an absolute path, use it directly
            weekly_dir = self.weekly_results_path
        else:
            # If it's relative, join it with output_dir
            weekly_dir = os.path.join(self.output_dir, self.weekly_results_path)
        
        # Ensure the weekly results directory exists
        ensure_directory_exists(weekly_dir)
        
        # Create the full file path
        file_path = os.path.join(weekly_dir, filename)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Saved weekly result to {file_path}")
            return file_path
        except Exception as e:
            print(f"❌ Error saving weekly result: {e}")
            return None
    
    def process_week(self, date_str, existing_files):
        """Process all weekly prompts for a specific week."""
        # Get all dates in the week
        week_dates = self._get_dates_for_week(date_str)
        
        # Check if at least one day of the week has journal entries
        if not self._check_week_has_any_data(week_dates, existing_files):
            print(f"❌ Week containing {date_str} has no data at all. Skipping weekly processing.")
            return False
        
        # Get the week number
        week_number = self._get_week_number(date_str)
        
        # Collect data from all available journal entries in the week
        weekly_data = self._collect_weekly_data(week_dates, existing_files)
        
        # Format the weekly data for use in prompt templates
        formatted_data = self._format_weekly_data(weekly_data)
        
        success_count = 0
        
        # Process each weekly prompt
        for prompt_filename in self.weekly_prompts:
            print(f"\nProcessing weekly prompt: {prompt_filename}")
            
            # Load the prompt template
            template = self._load_prompt_template(prompt_filename)
            if not template:
                continue
            
            # Replace the WEEKLY_FILES placeholder with the formatted weekly data
            prompt = template.replace("{WEEKLY_FILES}", formatted_data)
            
            # Generate the weekly summary using OpenAI
            print(f"Generating weekly summary using {prompt_filename}")
            weekly_summary = self.openai.generate_text(prompt)
            
            if weekly_summary:
                # Save the weekly summary
                self._save_weekly_result(week_number, prompt_filename, weekly_summary)
                success_count += 1
            else:
                print(f"❌ Failed to generate weekly summary using {prompt_filename}")
        
        return success_count > 0
    
    def find_weeks_with_data(self, existing_files):
        """Find all weeks that have at least one day of data."""
        if not existing_files:
            print("No existing files to process for weekly summaries")
            return []
        
        # Get all unique dates
        all_dates = list(existing_files.keys())
        
        # Get all unique weeks
        unique_weeks = set()
        for date in all_dates:
            week_dates = self._get_dates_for_week(date)
            week_start = week_dates[0]  # Monday of the week
            unique_weeks.add(week_start)
        
        return sorted(list(unique_weeks))
    
    def process_all_complete_weeks(self, existing_files):
        """Process all weeks that have at least one day of data."""
        # Find all weeks with any data
        weeks_with_data = self.find_weeks_with_data(existing_files)
        
        if not weeks_with_data:
            print("No weeks with data found to process")
            return 0
        
        print(f"\nFound {len(weeks_with_data)} weeks with at least one day of data to process")
        
        processed_count = 0
        
        # Process each week with data
        for week_start in weeks_with_data:
            print(f"\nProcessing week starting {week_start}")
            
            if self.process_week(week_start, existing_files):
                processed_count += 1
        
        print(f"\nProcessed {processed_count} weeks successfully")
        return processed_count