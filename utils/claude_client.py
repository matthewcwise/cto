import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class ClaudeClient:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
    def generate_response(self, prompt, system_prompt=None, max_tokens=1000):
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=max_tokens,
            system=system_prompt,
            messages=messages
        )
        
        return response.content[0].text 