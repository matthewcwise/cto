# Agentic Team Workflow

This program creates a team of agentic LLM agents to support project management and engineering tasks. The system uses Claude for text generation and creates structured markdown outputs.

## Features

- Project Management Workflow
  - Create new projects or reopen existing ones
  - Project Manager agent for initial evaluation
  - Engineering Manager agent for task breakdown
  - Engineering Team for task execution

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your Claude API key:
```
ANTHROPIC_API_KEY=your_api_key_here
```

3. Run the program:
```bash
python main.py
```

## Workflow

1. Start a new project or reopen an existing one
2. Provide a project description
3. Project Manager evaluates and either:
   - Asks follow-up questions
   - Generates detailed instructions
4. Engineering Manager either:
   - Asks follow-up questions
   - Creates detailed task checklist
5. Output is generated as markdown files in the `outputs` directory 