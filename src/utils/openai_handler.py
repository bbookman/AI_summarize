import time
import random
from openai import OpenAI
# Update the error imports for newer OpenAI SDK versions
from openai import APIError, APIConnectionError, RateLimitError, AuthenticationError # Added AuthenticationError
import sys # Added import

class OpenAIHandler:
    def __init__(self, config):
        self.client = OpenAI(api_key=config['OPENAI_API_KEY'])
        self.model = config['OPEN_AI_MODEL']
        # Load journal prompt template during initialization
        self.journal_prompt_path = config.get('JOURNAL_PROMPT', '')
        self.journal_template = self._load_prompt_template(self.journal_prompt_path)
        
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
            except AuthenticationError as e: # Catch AuthenticationError specifically
                print(f"\n❌ FATAL ERROR: OpenAI Authentication Failed (Invalid API Key?):")
                print(f"   {str(e)}")
                print(f"\nPlease check your API key and ensure it's valid and has permissions.")
                print("Exiting application.")
                sys.exit(1) # Exit the application
            except (APIError, APIConnectionError) as e:
                error_str = str(e)
                
                # Check specifically for context length exceeded error
                if "context_length_exceeded" in error_str or "maximum context length" in error_str:
                    print(f"\n❌ FATAL ERROR: The prompt is too large for the model's context window:")
                    print(f"   {error_str}")
                    print(f"\nThe application will now terminate. Please reduce the amount of data being processed.")
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

    def _load_prompt_template(self, path):
        """Load the prompt template from the specified path."""
        print(f"\nLoading prompt template from: {path}")
        try:
            with open(path, 'r') as file:
                template = file.read()
            print(f"✓ Loaded prompt template ({len(template)} chars)")
            return template
        except Exception as e:
            print(f"❌ Error loading prompt template: {e}")
            return None

    def send_prompt(self, prompt):
        """Send a prompt to OpenAI and get the response."""
        try:
            print(f"Sending prompt to OpenAI (length: {len(prompt)} chars)")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            print("Received response from OpenAI")
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error sending prompt to OpenAI: {e}")
            return None

    def format_prompt(self, template, bee_content="", limitless_content="", facts_content="", errors_content=""):
        """Format the prompt template with all content."""
        print("\nFormatting prompt with:")
        if bee_content:
            print(f"- Bee content (length: {len(bee_content)} chars)")
        if limitless_content:
            print(f"- Limitless content (length: {len(limitless_content)} chars)")
        if facts_content:
            print(f"- Facts content (length: {len(facts_content)} chars)")
        if errors_content:
            print(f"- Errors content (length: {len(errors_content)} chars)")
            
        return template.replace("{BEE_CONTENT}", bee_content)\
                      .replace("{LIMITLESS_CONTENT}", limitless_content)\
                      .replace("{FACTS_CONTENT}", facts_content)\
                      .replace("{ERRORS_CONTENT}", errors_content)