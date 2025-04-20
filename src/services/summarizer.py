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
        self.config = config  # Store the entire config object
        self.output_dir = config.get('OUTPUT_DIR')
        if not self.output_dir:
            raise ValueError("OUTPUT_DIR not configured")
        print("✓ Summarizer initialized")

    def save_summary(self, summary, date=None, suffix=""):
        """Save summary with YYYY-MM-DD format filename, with optional suffix"""
        if not summary:
            raise ValueError("Summary content cannot be empty")
            
        # Ensure we have a valid date
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Create filename in YYYY-MM-DD format with optional suffix
        filename = f"{date}{suffix}.md"
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(summary)
            return filepath
        except Exception as e:
            raise IOError(f"Failed to save summary: {e}")

    def generate_journal(self, date, bee_data, limitless_data, facts=None, errors=None):
        """Generate a journal entry using the JOURNAL_PROMPT template."""
        print(f"\nGenerating journal for {date}...")

        # Load prompt template
        try:
            with open(self.config['JOURNAL_PROMPT'], 'r') as file:
                template = file.read()
        except Exception as e:
            print(f"❌ Failed to load journal prompt template: {e}")
            return False

        # Format the prompt with data - UPDATED PARAMETER NAMES TO MATCH TEMPLATE
        formatted_prompt = template.format(
            date=date,
            BEE_CONTENT=bee_data if bee_data else "No data available",
            LIMITLESS_CONTENT=limitless_data if limitless_data else "No data available",
            FACTS_CONTENT=facts if facts else "No additional facts available",
            ERRORS_CONTENT=errors if errors else "No errors noted"
        )

        # Get response from OpenAI
        journal = self.openai.generate_text(formatted_prompt)
        
        if journal:
            # Save the journal with the specific date
            filepath = self.save_summary(journal, date)
            print(f"✓ Journal entry saved to: {filepath}")
            return True
        else:
            print(f"❌ Failed to generate journal for {date}")
            return False

    def generate_insights(self, date, bee_data, limitless_data, facts=None, errors=None):
        """Generate insights using the INSIGHT_PROMPT template."""
        print(f"\nGenerating insights for {date}...")
        
        # Load the insight prompt template
        try:
            with open(self.config['INSIGHT_PROMPT'], 'r') as file:
                template = file.read()
        except Exception as e:
            print(f"❌ Failed to load insight prompt template: {e}")
            return False
        
        # Prepare the prompt with data
        prompt = template.format(
            BEE_CONTENT=bee_data if bee_data else "No data available",
            LIMITLESS_CONTENT=limitless_data if limitless_data else "No data available",
            FACTS_CONTENT=facts if facts else "No additional facts available",
            ERRORS_CONTENT=errors if errors else "No known errors"
        )
        
        # Generate the insights using OpenAI
        insights = self.openai.generate_text(prompt)
        
        if insights:
            # Create the insight filename with pattern YYYY-MM-DD-insight.md
            filepath = self.save_summary(insights, date, suffix="-insight")
            print(f"✓ Insights saved to: {filepath}")
            return True
        else:
            print(f"❌ Failed to generate insights for {date}")
            return False

    def process_date(self, date, bee_data, limitless_data, facts=None, errors=None):
        """Process data for a specific date to generate both journal and insights."""
        # Generate the journal entry
        journal_success = self.generate_journal(date, bee_data, limitless_data, facts, errors)
        
        # Generate the insights
        insight_success = self.generate_insights(date, bee_data, limitless_data, facts, errors)
        
        return journal_success and insight_success

    def process_all(self, bee_data, limitless_data, facts, errors, date):
        """Process data for a specific date (calls process_date)."""
        try:
            print(f"\nProcessing all data for {date}...")
            
            if not date:
                print("❌ No date provided for processing")
                return False

            # Use the process_date method to handle both journal and insights
            success = self.process_date(date, bee_data, limitless_data, facts, errors)
            
            if success:
                print(f"✓ All processing complete for {date}")
            else:
                print(f"❌ Some processing failed for {date}")
            
            return success
            
        except Exception as e:
            print(f"❌ Error in process_all: {e}")
            return False

    def generate_text(self, prompt, max_retries=3):
        """Generate text with retries for connection issues"""
        attempt = 0
        while attempt < max_retries:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )
                return response.choices[0].message.content
            except (APIError, APIConnectionError) as e:
                error_str = str(e)
                
                # Check specifically for context length exceeded error
                if "context_length_exceeded" in error_str or "maximum context length" in error_str:
                    print(f"\n❌ FATAL ERROR: The prompt is too large for the model's context window:")
                    print(f"   {error_str}")
                    print(f"\nThe application will now terminate. Please reduce the amount of data being processed.")
                    import sys
                    sys.exit(1)  # Exit with error code
                    
                # Handle other API errors with retry
                attempt += 1
                if attempt >= max_retries:
                    print(f"Failed after {max_retries} attempts: {error_str}")
                    return None
                    
                # Exponential backoff with jitter
                sleep_time = (2 ** attempt) + random.uniform(0, 1)
                print(f"Connection error: {error_str}. Retrying in {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)
            except RateLimitError:
                # Special handling for rate limits
                sleep_time = 20 + random.uniform(0, 10)
                print(f"Rate limit exceeded. Waiting {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)
                attempt += 1
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
                return None
                
        return None