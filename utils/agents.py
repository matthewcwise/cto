from .claude_client import ClaudeClient
from .prompts import (
    CTO_SYSTEM_PROMPT,
    PRODUCT_MANAGER_SYSTEM_PROMPT,
    ENGINEERING_MANAGER_SYSTEM_PROMPT,
    CTO_EVALUATION_TEMPLATE,
    PRODUCT_MANAGER_EVALUATION_TEMPLATE,
    ENGINEERING_MANAGER_TASK_TEMPLATE
)
import os
import json
import re
from datetime import datetime

class AgentResponse:
    def __init__(self, json_str):
        self.raw_response = json_str
        
        # Try to extract JSON from the response if it's embedded in text
        json_match = re.search(r'(\{.*\})', json_str, re.DOTALL)
        json_content = json_match.group(1) if json_match else json_str
        
        try:
            data = json.loads(json_content)
            self.command = data.get("command", "")
            self.content = data.get("content", "")
            self.questions = data.get("questions", [])
            self.needs_followup = self.command == "follow-up"
        except json.JSONDecodeError as e:
            # Fallback handling for non-JSON responses
            self.command = "follow-up" if "?" in json_str else "pass-on"
            self.content = json_str
            self.questions = self._extract_questions(json_str)
            self.needs_followup = "?" in json_str
    
    def _extract_questions(self, text):
        """Attempt to extract numbered questions from text."""
        questions = []
        lines = text.split('\n')
        
        for line in lines:
            # Look for numbered questions (1. What is...?)
            match = re.match(r'^\s*\d+\.\s*(.*\?)\s*$', line)
            if match:
                questions.append(match.group(1))
        
        return questions
            
    def get_formatted_questions(self):
        if not self.questions:
            return self.content
        
        questions_md = "# Follow-up Questions\n\n"
        for i, q in enumerate(self.questions, 1):
            questions_md += f"{i}. {q}\n"
        
        return questions_md

class CTO:
    def __init__(self):
        self.client = ClaudeClient()
        self.system_prompt = CTO_SYSTEM_PROMPT

    def evaluate_project(self, description):
        prompt = CTO_EVALUATION_TEMPLATE.format(description=description)
        response = self.client.generate_response(prompt, self.system_prompt)
        return AgentResponse(response)

class ProductManager:
    def __init__(self):
        self.client = ClaudeClient()
        self.system_prompt = PRODUCT_MANAGER_SYSTEM_PROMPT

    def evaluate_project(self, description, technical_strategy):
        # Extract just the content from CTO's technical strategy if it's an AgentResponse
        if isinstance(technical_strategy, AgentResponse):
            technical_strategy = technical_strategy.content
            
        prompt = PRODUCT_MANAGER_EVALUATION_TEMPLATE.format(
            description=description,
            technical_strategy=technical_strategy
        )
        response = self.client.generate_response(prompt, self.system_prompt)
        return AgentResponse(response)

class EngineeringManager:
    def __init__(self):
        self.client = ClaudeClient()
        self.system_prompt = ENGINEERING_MANAGER_SYSTEM_PROMPT

    def create_task_list(self, requirements, technical_strategy):
        # Extract just the content if they're AgentResponses
        if isinstance(requirements, AgentResponse):
            requirements = requirements.content
        if isinstance(technical_strategy, AgentResponse):
            technical_strategy = technical_strategy.content
            
        prompt = ENGINEERING_MANAGER_TASK_TEMPLATE.format(
            requirements=requirements,
            technical_strategy=technical_strategy
        )
        response = self.client.generate_response(prompt, self.system_prompt)
        return AgentResponse(response)

def save_to_markdown(agent_response, filename, project_name):
    # Create outputs directory if it doesn't exist
    os.makedirs("outputs", exist_ok=True)
    
    # Create project-specific directory
    project_dir = os.path.join("outputs", project_name)
    os.makedirs(project_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(project_dir, f"{filename}_{timestamp}.md")
    
    content = agent_response.content
    if agent_response.needs_followup:
        content = agent_response.get_formatted_questions()
    
    with open(filepath, "w") as f:
        f.write(content)
    
    return filepath 