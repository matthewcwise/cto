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
# Copy the example file
cp .env.example .env

# Then edit .env with your actual API key
ANTHROPIC_API_KEY=your_api_key_here
```

3. Run the program:
```bash
python main.py
```bash

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
python main.py
```bash
python main.py
```bash
python main.py
```bash
python main.py
```



## Sample Workflow:
$ python main.py

Welcome to the Software Development Assistant!
----------------------------------------
Choose your workflow:
1. Rapid Prototyper - Focus on quick implementation and minimal viable features
2. Virtual CTO - Focus on robust, scalable architecture and comprehensive planning

Select workflow (1 or 2): 1

Options:
1. Start a new project
2. Reopen existing project

Enter your choice (1 or 2): 1

Enter a name for your project: productivity coach

Please describe your idea in detail: I want a tool that helps me track my focus and productivity on my computer

--- RAPID PROTOTYPE WORKFLOW ---
This workflow focuses on quick implementation and minimal viable features.

Prototype Planner is defining core features...

Prototype requirements saved to: outputs/productivity_coach/prototype_requirements_20250507_131942.md

Prototype Planner has some questions about core functionality:
1. What specific aspects of focus and productivity do you want to track? (Time spent on applications, focus sessions, distractions, etc.)
2. Who is the primary target user for this tool? (Professionals, students, freelancers, yourself personally?)
3. What platforms should this run on? (Windows, Mac, web-based, mobile?)
4. What key problems are you trying to solve with this tool?
5. Do you want the tool to just track and report data, or also provide interventions (like blocking distracting sites, sending reminders)?
6. Are there any existing tools you've tried that didn't meet your needs? What was missing?

Please provide additional information: 1. all of the above. 2. this is for myself on my computer. 3. windows. 4. I get distracted and lose track of time and waste it on unproductive stuff. 5. track and report data. 6. Data visualization is a big motivator for me, so I have found success when things visualize and quantify how much time I have spent being productive and where my wasted time/productive time has gone

Updated prototype requirements saved to: outputs/productivity_coach/prototype_requirements_20250507_132111.md

Prototype Planner has some questions about core functionality:
1. What specific activities or applications do you want to track as 'productive' vs 'unproductive'?
2. Do you want the tool to run in the background automatically or would you prefer to manually start/stop tracking sessions?
3. What type of data visualizations would be most motivating for you (e.g., daily charts, weekly summaries, real-time dashboards)?
4. Would you like notifications or alerts when you spend too much time on unproductive activities?
5. Do you need the ability to set goals or targets for productive time?
6. How would you prefer to categorize or tag your activities (predefined categories or custom tagging)?

Please provide additional information: 1. work time, personal productive time (e.g. working on project like this), and distracted time (e.g. playing chess or starcraft). 2) Automatically would be wonderful. 3) Daily/hourly charts, weekly summaries, and real-time dashboards all sound important. 4. Alerts would be grat. 5. Yes. 6. I think we need to have the ability to review data regularly to recategorize it, but having some predefined categories would be a good starter

Updated prototype requirements saved to: outputs/productivity_coach/prototype_requirements_20250507_132249.md

Prototype Planner has some questions about core functionality:
1. Which tracking method would be most important for your initial prototype: automatic application tracking, manual time logging, or a combination?
2. For the MVP, which single data visualization would provide the most value to you (daily breakdown, weekly summary, or real-time dashboard)?
3. What's the minimum categorization system you need to start testing (how many categories and what are the most critical ones)?
4. Would you prefer the prototype to run as a background process, a taskbar application, or an application you manually open?
5. What would be your primary success metric for this prototype (increased productive time, reduced distractions, better awareness of habits)?

Please provide additional information: 1. automatic tracking is a core function. 2. Real-time dashboard would be best. 3. Work. Personal Productivity. Gaming. 4. Application I manually open. 5. Better awareness of habits

Updated prototype requirements saved to: outputs/productivity_coach/prototype_requirements_20250507_132417.md

Technical Advisor is suggesting practical technologies for your prototype...

Technical approach saved to: outputs/productivity_coach/technical_approach_20250507_132440.md

Prototype Developer is creating a practical implementation plan...

Implementation plan saved to: outputs/productivity_coach/implementation_plan_20250507_132626.md

Task Generator is creating a detailed task list for engineers...

Task Generator is creating a detailed task list...

Detailed engineering tasks saved to: outputs/productivity_coach/engineering_tasks_20250507_132810.md

Prototype plan for 'productivity_coach' completed!
All outputs saved to: outputs/productivity_coach/

Your prototype development plan includes:
1. Technical Approach: outputs/productivity_coach/technical_approach_20250507_132440.md
2. Prototype Requirements: outputs/productivity_coach/prototype_requirements_20250507_132417.md
3. Implementation Plan: outputs/productivity_coach/implementation_plan_20250507_132626.md
4. Engineering Tasks: outputs/productivity_coach/engineering_tasks_20250507_132810.md