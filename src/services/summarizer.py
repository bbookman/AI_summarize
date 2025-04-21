import os
from datetime import datetime
from utils.openai_handler import OpenAIHandler
from utils.file_handler import write_file

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

    def generate_insights(self, date, bee_data, limitless_data, facts=None, errors=None):
        """Generate insights using the INSIGHT_PROMPT template."""
        print(f"\nGenerating insights for {date}...")

        # 1. Load the insight prompt template
        try:
            # Debug: Check if the file exists
            if os.path.exists(self.config['INSIGHT_PROMPT']):
                print(f"✓ INSIGHT_PROMPT file found at: {self.config['INSIGHT_PROMPT']}")
            else:
                print(f"❌ INSIGHT_PROMPT file NOT FOUND at: {self.config['INSIGHT_PROMPT']}")

            with open(self.config['INSIGHT_PROMPT'], 'r') as file:
                template = file.read()
            # print(f"✓ Loaded insight prompt template ({len(template)} chars)")  # Debug
        except Exception as e:
            print(f"❌ Failed to load insight prompt template: {e}")
            return False

        # 2. Format the prompt with data
        prompt = template.format(
            BEE_CONTENT=bee_data if bee_data else "No data available",
            LIMITLESS_CONTENT=limitless_data if limitless_data else "No data available",
            FACTS_CONTENT=facts if facts else "No additional facts available",
            ERRORS_CONTENT=errors if errors else "No known errors"
        )
        # print(f"Formatted prompt (length: {len(prompt)} chars):")  # Debug
        print(prompt[:10])  # Debug - Print the entire prompt

        # 3. Generate the insights using OpenAI
        insights = self.openai.generate_text(prompt)

        if insights:
            # print(f"✓ Successfully generated insights (length: {len(insights)} chars)")  # Debug
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

    def generate_text(self, template, bee_content="", limitless_content="", facts_content="", errors_content=""):
        """Generate text with retries for connection issues"""
        prompt = template.format(
            BEE_CONTENT=bee_content if bee_content else "No data available",
            LIMITLESS_CONTENT=limitless_content if limitless_content else "No data available",
            FACTS_CONTENT=facts_content if facts_content else "No additional facts available",
            ERRORS_CONTENT=errors_content if errors_content else "No known errors"
        )
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
                attempt += 1
                if attempt >= max_retries:
                    print(f"Failed after {max_retries} attempts: {str(e)}")
                    return None
                    
                # Exponential backoff with jitter
                sleep_time = (2 ** attempt) + random.uniform(0, 1)
                print(f"Connection error: {str(e)}. Retrying in {sleep_time:.2f} seconds...")
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