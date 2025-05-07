import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class ClaudeClient:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
    def generate_response(self, prompt, system_prompt=None, max_tokens=4000, model="claude-3-opus-20240229", thinking=None):
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        # Build request parameters - ignore thinking parameter completely
        request_params = {
            "model": model,
            "max_tokens": max_tokens,
            "system": system_prompt,
            "messages": messages
        }
        
        # Extended thinking is not supported in this version, just log a message if it was requested
        if thinking:
            print("\nNote: Extended thinking requested but not available in this version.")
            print("Using standard Claude model without extended thinking.")
        
        response = self.client.messages.create(**request_params)
        
        # Standard response handling
        return response.content[0].text 