from openai import OpenAI

class OpenAIHandler:
    def __init__(self, config):
        self.client = OpenAI(api_key=config['OPENAI_API_KEY'])
        self.model = config['OPEN_AI_MODEL']
        self.prompt_template_path = config['PROMPT_TEMPLATE_PATH']
        print(f"Initialized OpenAI handler with model: {self.model}")

    def load_prompt_template(self):
        """Load the prompt template from the specified path."""
        print(f"\nLoading prompt template from: {self.prompt_template_path}")
        try:
            with open(self.prompt_template_path, 'r') as file:
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