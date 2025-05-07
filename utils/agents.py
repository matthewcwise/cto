from .claude_client import ClaudeClient
from .prompts import (
    # Task Generator prompts
    TASK_GENERATOR_SYSTEM_PROMPT,
    TASK_GENERATOR_TEMPLATE,
    # Prototype workflow prompts
    PROTOTYPE_CTO_SYSTEM_PROMPT,
    PROTOTYPE_PRODUCT_MANAGER_SYSTEM_PROMPT,
    PROTOTYPE_ENGINEERING_MANAGER_SYSTEM_PROMPT,
    PROTOTYPE_CTO_TEMPLATE,
    PROTOTYPE_PRODUCT_MANAGER_TEMPLATE,
    PROTOTYPE_ENGINEERING_MANAGER_TEMPLATE,
    # Robust workflow prompts
    ROBUST_CTO_SYSTEM_PROMPT,
    ROBUST_PRODUCT_MANAGER_SYSTEM_PROMPT,
    ROBUST_ENGINEERING_MANAGER_SYSTEM_PROMPT,
    ROBUST_CTO_TEMPLATE,
    ROBUST_PRODUCT_MANAGER_TEMPLATE,
    ROBUST_ENGINEERING_MANAGER_TEMPLATE
)
import os
import json
import re
from datetime import datetime
from .json_utils import robust_json_parse

# Default model to use across all agents
DEFAULT_MODEL = "claude-3-7-sonnet-20250219"

class AgentResponse:
    def __init__(self, json_str):
        self.raw_response = json_str
        self.is_truncated = False

        # Use the robust JSON parser
        try:
            data = robust_json_parse(json_str)
            self.command = data.get("command", "")
            self.content = data.get("content", "")
            self.questions = data.get("questions", [])
            self.needs_followup = self.command == "follow-up"
            return
        except Exception as e:
            print("\n[AgentResponse] Robust JSON parse failed:", e)
            print("Offending content:\n", json_str)

        # If parsing fails, fallback handling for non-JSON responses
        if json_str.strip().endswith(("...", "cursor", "```", "'", "\"", ",", "{", "[")):
            self.is_truncated = True
            print("\nDetected truncated response from agent.")
            self.needs_followup = True
        elif "follow-up" in json_str.lower() or "?" in json_str:
            self.needs_followup = True
            self.command = "follow-up"
        else:
            self.needs_followup = False
            self.command = "pass-on"

        self.content = json_str
        self.questions = self._extract_questions(json_str)

    def _extract_questions(self, text):
        """Attempt to extract numbered questions from text."""
        questions = []
        lines = text.split('\n')
        
        # If we detected a truncated response, add a standard question
        if self.is_truncated:
            questions.append("The previous response appears to be incomplete. Would you like me to regenerate it or continue from where it left off?")
            return questions
        
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
        
        if self.is_truncated:
            questions_md += "## ⚠️ Incomplete Response Detected\n\n"
            questions_md += "The previous response appears to have been cut off unexpectedly.\n\n"
        
        for i, q in enumerate(self.questions, 1):
            questions_md += f"{i}. {q}\n"
        
        return questions_md

class CTO:
    def __init__(self):
        self.client = ClaudeClient()
        self.system_prompt = PROTOTYPE_CTO_SYSTEM_PROMPT
        self.model = DEFAULT_MODEL

    def evaluate_project(self, requirements):
        # requirements is now the output from ProductManager
        if isinstance(requirements, AgentResponse):
            requirements = requirements.content
        prompt = PROTOTYPE_CTO_TEMPLATE.format(requirements=requirements)
        response = self.client.generate_response(prompt, self.system_prompt, model=self.model)
        return AgentResponse(response)

class ProductManager:
    def __init__(self):
        self.client = ClaudeClient()
        self.system_prompt = PROTOTYPE_PRODUCT_MANAGER_SYSTEM_PROMPT
        self.model = DEFAULT_MODEL

    def evaluate_project(self, description):
        prompt = PROTOTYPE_PRODUCT_MANAGER_TEMPLATE.format(
            description=description
        )
        response = self.client.generate_response(prompt, self.system_prompt, model=self.model)
        return AgentResponse(response)

class EngineeringManager:
    def __init__(self):
        self.client = ClaudeClient()
        self.system_prompt = PROTOTYPE_ENGINEERING_MANAGER_SYSTEM_PROMPT
        self.model = DEFAULT_MODEL

    def create_task_list(self, requirements, technical_strategy):
        # Extract just the content if they're AgentResponses
        if isinstance(requirements, AgentResponse):
            requirements = requirements.content
        if isinstance(technical_strategy, AgentResponse):
            technical_strategy = technical_strategy.content
            
        prompt = PROTOTYPE_ENGINEERING_MANAGER_TEMPLATE.format(
            requirements=requirements,
            technical_strategy=technical_strategy
        )
        # Use a higher max_tokens limit for implementation plans
        response = self.client.generate_response(
            prompt, 
            self.system_prompt, 
            model=self.model,
            max_tokens=8000  # Doubled from default 4000
        )
        return AgentResponse(response)

    def continue_from_truncated(self, requirements, technical_strategy, previous_response):
        """Continue from a truncated response."""
        # Extract just the content if they're AgentResponses
        if isinstance(requirements, AgentResponse):
            requirements = requirements.content
        if isinstance(technical_strategy, AgentResponse):
            technical_strategy = technical_strategy.content
            
        prompt = f"""
Your previous response was cut off. Here are the requirements and technical strategy again:

Requirements:
{requirements}

Technical Approach:
{technical_strategy}

Your partial response was:
{previous_response}

Please continue your implementation plan from where you left off.
"""
        # Use a higher max_tokens limit for continuation
        response = self.client.generate_response(
            prompt, 
            self.system_prompt, 
            model=self.model,
            max_tokens=8000  # Doubled from default 4000
        )
        return AgentResponse(response)

class RobustCTO:
    def __init__(self):
        self.client = ClaudeClient()
        self.system_prompt = ROBUST_CTO_SYSTEM_PROMPT
        self.model = DEFAULT_MODEL

    def evaluate_project(self, description):
        prompt = ROBUST_CTO_TEMPLATE.format(description=description)
        response = self.client.generate_response(prompt, self.system_prompt, model=self.model)
        return AgentResponse(response)

class RobustProductManager:
    def __init__(self):
        self.client = ClaudeClient()
        self.system_prompt = ROBUST_PRODUCT_MANAGER_SYSTEM_PROMPT
        self.model = DEFAULT_MODEL

    def evaluate_project(self, description, technical_strategy):
        # Extract just the content from CTO's technical strategy if it's an AgentResponse
        if isinstance(technical_strategy, AgentResponse):
            technical_strategy = technical_strategy.content
            
        prompt = ROBUST_PRODUCT_MANAGER_TEMPLATE.format(
            description=description,
            technical_strategy=technical_strategy
        )
        response = self.client.generate_response(prompt, self.system_prompt, model=self.model)
        return AgentResponse(response)

class RobustEngineeringManager:
    def __init__(self):
        self.client = ClaudeClient()
        self.system_prompt = ROBUST_ENGINEERING_MANAGER_SYSTEM_PROMPT
        self.model = DEFAULT_MODEL

    def create_task_list(self, requirements, technical_strategy):
        # Extract just the content if they're AgentResponses
        if isinstance(requirements, AgentResponse):
            requirements = requirements.content
        if isinstance(technical_strategy, AgentResponse):
            technical_strategy = technical_strategy.content
            
        prompt = ROBUST_ENGINEERING_MANAGER_TEMPLATE.format(
            requirements=requirements,
            technical_strategy=technical_strategy
        )
        # Use a higher max_tokens limit for detailed implementation plans
        response = self.client.generate_response(
            prompt, 
            self.system_prompt,
            model=self.model,
            max_tokens=8000  # Doubled from default 4000
        )
        return AgentResponse(response)

class TaskGenerator:
    def __init__(self):
        self.client = ClaudeClient()
        self.system_prompt = TASK_GENERATOR_SYSTEM_PROMPT
        self.model = DEFAULT_MODEL

    def generate_tasks(self, implementation_plan, technical_strategy):
        # Extract just the content if they're AgentResponses
        if isinstance(implementation_plan, AgentResponse):
            implementation_plan = implementation_plan.content
        if isinstance(technical_strategy, AgentResponse):
            technical_strategy = technical_strategy.content
            
        prompt = TASK_GENERATOR_TEMPLATE.format(
            implementation_plan=implementation_plan,
            technical_strategy=technical_strategy
        )
        
        # Simple approach - higher max_tokens for detailed tasks
        print("\nTask Generator is creating a detailed task list...")
        response = self.client.generate_response(
            prompt, 
            self.system_prompt,
            model=self.model,
            max_tokens=12000  # Doubled from default 4000
        )
            
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
    
    # Log truncated responses for debugging
    if agent_response.is_truncated:
        debug_path = os.path.join(project_dir, f"debug_{filename}_{timestamp}.log")
        with open(debug_path, "w") as f:
            f.write(f"TRUNCATED RESPONSE DETECTED:\n\n")
            f.write(f"Raw response:\n{agent_response.raw_response}\n\n")
            f.write(f"Content length: {len(agent_response.content)} characters\n")
    
    with open(filepath, "w") as f:
        f.write(content)
    
    return filepath 