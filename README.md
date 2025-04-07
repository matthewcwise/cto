# Software Development Assistant

This program creates a team of agentic LLM agents to support software development projects. The system uses Claude for text generation and creates structured markdown outputs with two distinct workflows.

## Features

- Two Workflow Options:
  - **Rapid Prototyper**: Focus on quick implementation and minimal viable features
  - **Virtual CTO**: Focus on robust, scalable architecture and comprehensive planning
- Project Management Tools:
  - Create new projects or reopen existing ones
  - Intelligent agents for project evaluation and planning
  - Structured output for implementation

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

## Workflows

### Rapid Prototyper Workflow

Ideal for quick proof-of-concepts and MVPs:

1. Technical Advisor suggests practical technologies for rapid development
2. Prototype Planner defines minimal core features
3. Prototype Developer creates a practical implementation plan
4. All outputs focus on speed and simplicity

### Virtual CTO Workflow

Ideal for production-grade software development:

1. CTO designs a robust technical architecture with scalability in mind
2. Product Strategy Manager defines comprehensive requirements and roadmap
3. Engineering Lead creates a detailed implementation plan with best practices
4. All outputs focus on maintainability, scalability, and long-term success

## Usage

1. Choose your workflow (Rapid Prototyper or Virtual CTO)
2. Start a new project or reopen an existing one
3. Provide a project description
4. Answer follow-up questions from each agent
5. Review detailed output reports in the `outputs` directory 