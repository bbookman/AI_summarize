import os
from datetime import datetime
from utils.openai_handler import OpenAIHandler
from utils.file_handler import write_file

class Summarizer:
    """Service to handle data reading and OpenAI summarization."""
    
    def __init__(self, config):
        """Initialize summarizer with configuration."""
        print("\nInitializing Summarizer...")
        self.openai = OpenAIHandler(config)
        self.output_dir = config.get('OUTPUT_DIR')
        if not self.output_dir:
            raise ValueError("OUTPUT_DIR not configured")
        print("✓ Summarizer initialized")

    def save_summary(self, summary, date=None):
        """Save summary with YYYY-MM-DD format filename"""
        if not summary:
            raise ValueError("Summary content cannot be empty")
            
        # Ensure we have a valid date
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Create filename in YYYY-MM-DD format
        filename = f"{date}.md"
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(summary)
            return filepath
        except Exception as e:
            raise IOError(f"Failed to save summary: {e}")

    def process_all(self, bee_data, limitless_data, facts, errors, date):
        """Process data for a specific date (date is passed in from filename)."""
        try:
            print("\nPreparing data for analysis...")

            # Use the date argument directly
            if not date:
                print("❌ No date provided for summary file name")
                return False

            # Load prompt template
            template = self.openai.load_prompt_template()
            if not template:
                print("❌ Failed to load prompt template")
                return False

            # Format and send prompt for this specific date
            formatted_prompt = self.openai.format_prompt(
                template=template,
                bee_content=bee_data or "",
                limitless_content=limitless_data or "",
                facts_content=facts or "",
                errors_content=errors or ""
            )

            # Get response from OpenAI
            response = self.openai.send_prompt(formatted_prompt)
            if not response:
                raise ValueError("Failed to generate summary content")
            
            # Save the summary with the specific date
            filepath = self.save_summary(response, date)
            print(f"✓ Summary saved to: {filepath}")
            return True
        except Exception as e:
            print(f"❌ Error generating summary: {e}")
            return False

    def generate_insights(self, date, bee_data, limitless_data, facts=None):
        """Generate insights using the INSIGHT_PROMPT template."""
        print(f"\nGenerating insights for {date}...")
        
        # Load the insight prompt template
        with open(self.config['INSIGHT_PROMPT'], 'r') as file:
            template = file.read()
        
        # Prepare the prompt with data
        prompt = template.format(
            date=date,
            bee_conversation=bee_data if bee_data else "No data available",
            limitless_conversation=limitless_data if limitless_data else "No data available",
            facts=facts if facts else "No additional facts available"
        )
        
        # Generate the insights using OpenAI
        insights = self.openai.generate_text(prompt)
        
        if insights:
            # Create the insight filename with pattern YYYY-MM-DD-insight.md
            insight_filename = f"{date}-insight.md"
            output_path = os.path.join(self.config['OUTPUT_DIR'], insight_filename)
            
            # Save the insights to file (no markdown formatting)
            with open(output_path, 'w') as file:
                file.write(insights)
            
            print(f"✓ Insights for {date} saved to {insight_filename}")
            return True
        else:
            print(f"❌ Failed to generate insights for {date}")
            return False

    def process_date(self, date, bee_data, limitless_data, facts=None):
        """Process data for a specific date to generate both journal and insights."""
        # Generate the journal entry (assuming this already exists)
        journal_success = self.generate_journal(date, bee_data, limitless_data, facts)
        
        # Generate the insights
        insight_success = self.generate_insights(date, bee_data, limitless_data, facts)
        
        return journal_success and insight_success