import json
import re

def robust_json_parse(text):
    """
    Try to robustly parse a JSON object from a string, even if it is pretty-printed,
    has leading/trailing whitespace, or is embedded in other text.
    Returns the parsed dict, or raises ValueError if parsing fails.
    """
    text = text.strip()
    # Try direct parse if it looks like a JSON object
    if text.startswith("{") and text.endswith("}"):
        try:
            return json.loads(text)
        except Exception:
            pass
    # Try to extract JSON object from anywhere in the string
    json_match = re.search(r'(\{.*\})', text, re.DOTALL)
    if json_match:
        json_content = json_match.group(1).strip()
        try:
            return json.loads(json_content)
        except Exception:
            pass
    raise ValueError("Could not robustly parse JSON from text.") 