import os
from datetime import datetime
from utils.openai_handler import OpenAIHandler
from utils.file_handler import write_file, ensure_directory_exists
import calendar # Added import
import sys # Added import

class Summarizer:
    """Service to handle data reading and OpenAI summarization."""
    
    def __init__(self, config):
        """Initialize summarizer with configuration."""
        # print("\nInitializing Summarizer...")
        self.openai = OpenAIHandler(config)
        self.config = config  # Store the entire config object
        self.output_dir = config.get('OUTPUT_DIR')
        if not self.output_dir:
            raise ValueError("OUTPUT_DIR not configured")
        # print("✓ Summarizer initialized")

    def save_summary(self, summary, date=None, suffix=""):
        """Save summary with YYYY-MM-DD format filename, organized by year and month."""
        if not summary:
            raise ValueError("Summary content cannot be empty")
            
        # Ensure we have a valid date string
        if not date:
            date_str = datetime.now().strftime('%Y-%m-%d')
        else:
            date_str = date # Assuming date is already a 'YYYY-MM-DD' string

        try:
            # Parse the date string to get year and month
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            year = str(date_obj.year)
            month_name = calendar.month_name[date_obj.month]
        except ValueError:
            print(f"❌ Invalid date format: {date_str}. Cannot organize by date.")
            # Fallback to saving directly in OUTPUT_DIR
            year = ""
            month_name = ""

        # Construct the target directory path
        target_dir = self.output_dir
        if year and month_name:
            target_dir = os.path.join(self.output_dir, year, month_name)
        
        # Create output directory structure if it doesn't exist
        ensure_directory_exists(target_dir)
        
        # Create filename in YYYY-MM-DD format with optional suffix
        filename = f"{date_str}{suffix}.md"
        filepath = os.path.join(target_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(summary)
            return filepath
        except Exception as e:
            raise IOError(f"Failed to save summary to {filepath}: {e}")

    def generate_journal(self, date, bee_data, limitless_data, facts=None, errors=None):
        """Generate a journal entry using the JOURNAL_PROMPT template."""
        print(f"\nGenerating journal for {date}...")

        # 1. Load the journal prompt template
        try:
            with open(self.config['JOURNAL_PROMPT'], 'r') as file:
                template = file.read()
        except Exception as e:
            print(f"❌ Failed to load journal prompt template: {e}")
            return False

        # 2. Format the prompt with data
        prompt = template.format(
            BEE_CONTENT=bee_data if bee_data else "No data available",
            LIMITLESS_CONTENT=limitless_data if limitless_data else "No data available",
            FACTS_CONTENT=facts if facts else "No additional facts available",
            ERRORS_CONTENT=errors if errors else "No known errors"
        )

        # 3. Generate the journal using OpenAI
        journal = self.openai.generate_text(prompt)

        if journal:
            # Save the journal with the specific date
            filepath = self.save_summary(journal, date)
            print(f"✓ Journal entry saved to: {filepath}")
            return True
        else:
            print(f"❌ Failed to generate journal for {date}")
            return False

    def process_date(self, date, bee_data, limitless_data, facts=None, errors=None):
        """Process data for a specific date to generate journal."""
        # Generate the journal entry
        journal_success = self.generate_journal(date, bee_data, limitless_data, facts, errors)
        return journal_success

    def process_all(self, bee_data, limitless_data, facts, errors, date):
        """Process data for a specific date (calls process_date)."""
        try:
            print(f"\nProcessing all data for {date}...")
            
            if not date:
                print("❌ No date provided for processing")
                return False

            # Use the process_date method to handle journal generation
            success = self.process_date(date, bee_data, limitless_data, facts, errors)
            
            if success:
                print(f"✓ All processing complete for {date}")
            else:
                print(f"❌ Some processing failed for {date}")
            
            return success
            
        except Exception as e:
            print(f"❌ Error in process_all: {e}")
            print("Exiting application due to error.")
            sys.exit(1) # Exit the application with an error code