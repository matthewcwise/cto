import os
import re
import json
from utils.agents import (
    CTO, ProductManager, EngineeringManager, 
    RobustCTO, RobustProductManager, RobustEngineeringManager,
    TaskGenerator, AgentResponse,
    save_to_markdown
)

def get_valid_project_name(prompt):
    """Get a valid project name that can be used as a directory name."""
    while True:
        project_name = input(prompt)
        # Replace spaces with underscores and remove special characters
        project_name = re.sub(r'[^\w\s-]', '', project_name).strip().replace(' ', '_')
        if project_name:
            return project_name
        print("Please enter a valid project name.")

def display_questions(response):
    """Display questions from an agent response more clearly."""
    if response.is_truncated:
        print("\n⚠️ INCOMPLETE RESPONSE DETECTED")
        print("The agent's response appears to have been cut off unexpectedly.")
        print("Options:")
        print("1. Try regenerating the response")
        print("2. Continue from where it left off")
        print("3. Provide more information and retry")
    
    for i, question in enumerate(response.questions, 1):
            print(f"{i}. {question}")

def run_prototype_workflow(project_name, project_description):
    """Run the rapid prototype workflow."""
    print("\n--- RAPID PROTOTYPE WORKFLOW ---")
    print("This workflow focuses on quick implementation and minimal viable features.")
    
    # Initialize agents
    prototype_planner = ProductManager()
    technical_advisor = CTO()
    prototype_developer = EngineeringManager()
    task_generator = TaskGenerator()
    
    # Save project description to a file
    os.makedirs(os.path.join("outputs", project_name), exist_ok=True)
    with open(os.path.join("outputs", project_name, "project_description.md"), "w") as f:
        f.write(f"# {project_name}\n\n{project_description}")
    
    # Prototype Planner evaluation (first)
    print("\nPrototype Planner is defining core features...")
    planner_response = prototype_planner.evaluate_project(project_description)
    planner_file = save_to_markdown(planner_response, "prototype_requirements", project_name)
    print(f"\nPrototype requirements saved to: {planner_file}")
    
    # Loop through Planner follow-up questions if needed
    while planner_response.needs_followup:
        print("\nPrototype Planner has some questions about core functionality:")
        display_questions(planner_response)
        additional_info = input("\nPlease provide additional information: ")
        project_description += "\n\nAdditional Feature Information:\n" + additional_info
        planner_response = prototype_planner.evaluate_project(project_description)
        planner_file = save_to_markdown(planner_response, "prototype_requirements", project_name)
        print(f"\nUpdated prototype requirements saved to: {planner_file}")
    
    # Technical Advisor evaluation (second)
    print("\nTechnical Advisor is suggesting practical technologies for your prototype...")
    tech_response = technical_advisor.evaluate_project(planner_response)
    tech_file = save_to_markdown(tech_response, "technical_approach", project_name)
    print(f"\nTechnical approach saved to: {tech_file}")
    
    # Loop through Technical Advisor follow-up questions if needed
    while tech_response.needs_followup:
        print("\nTechnical Advisor needs some clarification about your prototype:")
        display_questions(tech_response)
            
        additional_info = input("\nPlease provide additional information: ")
        project_description += "\n\nAdditional Information:\n" + additional_info
        tech_response = technical_advisor.evaluate_project(project_description)
        tech_file = save_to_markdown(tech_response, "technical_approach", project_name)
        print(f"\nUpdated technical approach saved to: {tech_file}")
    
    # Prototype Developer implementation plan
    print("\nPrototype Developer is creating a practical implementation plan...")
    developer_response = prototype_developer.create_task_list(planner_response, tech_response)
    developer_file = save_to_markdown(developer_response, "implementation_plan", project_name)
    print(f"\nImplementation plan saved to: {developer_file}")
    
    # Loop through Developer follow-up questions if needed
    while developer_response.needs_followup:
        print("\nPrototype Developer has some implementation questions:")
        display_questions(developer_response)
            
        if developer_response.is_truncated:
            action = input("\nHow would you like to proceed? (1/2/3): ")
            if action == "1":
                # Regenerate response
                print("\nRegenerating the implementation plan...")
                developer_response = prototype_developer.create_task_list(planner_response, tech_response)
                developer_file = save_to_markdown(developer_response, "implementation_plan", project_name)
                print(f"\nUpdated implementation plan saved to: {developer_file}")
                continue
            elif action == "2":
                # Continue from where it left off
                print("\nContinuing from where the response left off...")
                # We'll use the same prompt but ask to continue
                additional_prompt = "\n\nYour previous response was cut off. Please continue from where you left off."
                developer_response = prototype_developer.continue_from_truncated(planner_response, tech_response, developer_response.raw_response)
                developer_file = save_to_markdown(developer_response, "implementation_plan", project_name)
                print(f"\nUpdated implementation plan saved to: {developer_file}")
                continue
        
        additional_info = input("\nPlease provide additional information: ")
        project_description += "\n\nAdditional Implementation Information:\n" + additional_info
        developer_response = prototype_developer.create_task_list(planner_response, tech_response)
        developer_file = save_to_markdown(developer_response, "implementation_plan", project_name)
        print(f"\nUpdated implementation plan saved to: {developer_file}")
    
    # Generate detailed task list
    print("\nTask Generator is creating a detailed task list for engineers...")
    task_response = task_generator.generate_tasks(developer_response, tech_response)
    task_file = save_to_markdown(task_response, "engineering_tasks", project_name)
    print(f"\nDetailed engineering tasks saved to: {task_file}")
    
    # Loop through Task Generator follow-up questions if needed
    while task_response.needs_followup:
        print("\nTask Generator has some questions about task breakdown:")
        display_questions(task_response)
            
        additional_info = input("\nPlease provide additional information: ")
        project_description += "\n\nAdditional Task Information:\n" + additional_info
        task_response = task_generator.generate_tasks(developer_response, tech_response)
        task_file = save_to_markdown(task_response, "engineering_tasks", project_name)
        print(f"\nUpdated engineering tasks saved to: {task_file}")
    
    print(f"\nPrototype plan for '{project_name}' completed!")
    print(f"All outputs saved to: outputs/{project_name}/")
    print(f"\nYour prototype development plan includes:")
    print(f"1. Technical Approach: {tech_file}")
    print(f"2. Prototype Requirements: {planner_file}")
    print(f"3. Implementation Plan: {developer_file}")
    print(f"4. Engineering Tasks: {task_file}")

def run_cto_workflow(project_name, project_description):
    """Run the CTO workflow for robust, scalable software."""
    print("\n--- CTO WORKFLOW FOR ROBUST SOFTWARE ---")
    print("This workflow focuses on scalability, maintainability, and long-term architecture.")
    
    # Initialize agents
    technical_advisor = RobustCTO()
    product_manager = RobustProductManager()
    engineering_manager = RobustEngineeringManager()
    task_generator = TaskGenerator()
    
    # Save project description to a file
    os.makedirs(os.path.join("outputs", project_name), exist_ok=True)
    with open(os.path.join("outputs", project_name, "project_description.md"), "w") as f:
        f.write(f"# {project_name}\n\n{project_description}")
    
    # CTO evaluation
    print("\nCTO is designing a robust technical architecture...")
    tech_response = technical_advisor.evaluate_project(project_description)
    tech_file = save_to_markdown(tech_response, "technical_architecture", project_name)
    print(f"\nTechnical architecture saved to: {tech_file}")
    
    # Loop through CTO follow-up questions if needed
    while tech_response.needs_followup:
        print("\nCTO needs more information about your long-term vision:")
        display_questions(tech_response)
            
        additional_info = input("\nPlease provide additional information: ")
        project_description += "\n\nAdditional Information:\n" + additional_info
        tech_response = technical_advisor.evaluate_project(project_description)
        tech_file = save_to_markdown(tech_response, "technical_architecture", project_name)
        print(f"\nUpdated technical architecture saved to: {tech_file}")
    
    # Product Strategy evaluation
    print("\nProduct Strategy Manager is defining comprehensive requirements...")
    product_response = product_manager.evaluate_project(project_description, tech_response)
    product_file = save_to_markdown(product_response, "product_requirements", project_name)
    print(f"\nProduct requirements saved to: {product_file}")
    
    # Loop through Product Manager follow-up questions if needed
    while product_response.needs_followup:
        print("\nProduct Strategy Manager has questions about product vision:")
        display_questions(product_response)
            
        additional_info = input("\nPlease provide additional information: ")
        project_description += "\n\nAdditional Product Information:\n" + additional_info
        product_response = product_manager.evaluate_project(project_description, tech_response)
        product_file = save_to_markdown(product_response, "product_requirements", project_name)
        print(f"\nUpdated product requirements saved to: {product_file}")
    
    # Engineering Lead implementation plan
    print("\nEngineering Lead is creating a robust implementation plan...")
    engineering_response = engineering_manager.create_task_list(product_response, tech_response)
    engineering_file = save_to_markdown(engineering_response, "engineering_plan", project_name)
    print(f"\nEngineering plan saved to: {engineering_file}")
    
    # Loop through Engineering Lead follow-up questions if needed
    while engineering_response.needs_followup:
        print("\nEngineering Lead has some implementation questions:")
        display_questions(engineering_response)
            
        additional_info = input("\nPlease provide additional information: ")
        project_description += "\n\nAdditional Technical Information:\n" + additional_info
        engineering_response = engineering_manager.create_task_list(product_response, tech_response)
        engineering_file = save_to_markdown(engineering_response, "engineering_plan", project_name)
        print(f"\nUpdated engineering plan saved to: {engineering_file}")
    
    # Generate detailed task list
    print("\nTask Generator is creating a detailed task list for engineers...")
    task_response = task_generator.generate_tasks(engineering_response, tech_response)
    task_file = save_to_markdown(task_response, "engineering_tasks", project_name)
    print(f"\nDetailed engineering tasks saved to: {task_file}")
    
    # Loop through Task Generator follow-up questions if needed
    while task_response.needs_followup:
        print("\nTask Generator has some questions about task breakdown:")
        display_questions(task_response)
            
        additional_info = input("\nPlease provide additional information: ")
        project_description += "\n\nAdditional Task Information:\n" + additional_info
        task_response = task_generator.generate_tasks(engineering_response, tech_response)
        task_file = save_to_markdown(task_response, "engineering_tasks", project_name)
        print(f"\nUpdated engineering tasks saved to: {task_file}")
    
    print(f"\nRobust software plan for '{project_name}' completed!")
    print(f"All outputs saved to: outputs/{project_name}/")
    print(f"\nYour comprehensive development plan includes:")
    print(f"1. Technical Architecture: {tech_file}")
    print(f"2. Product Requirements: {product_file}")
    print(f"3. Engineering Plan: {engineering_file}")
    print(f"4. Engineering Tasks: {task_file}")

def main():
    print("\nWelcome to the Software Development Assistant!")
    print("----------------------------------------")
    print("Choose your workflow:")
    print("1. Rapid Prototyper - Focus on quick implementation and minimal viable features")
    print("2. Virtual CTO - Focus on robust, scalable architecture and comprehensive planning")
    
    workflow_choice = input("\nSelect workflow (1 or 2): ")
    
    print("\nOptions:")
    print("1. Start a new project")
    print("2. Reopen existing project")
    
    choice = input("\nEnter your choice (1 or 2): ")
    
    if choice == "1":
        # Get project name
        project_name = get_valid_project_name("\nEnter a name for your project: ")
        project_description = input("\nPlease describe your idea in detail: ")
        
        if workflow_choice == "1":
            run_prototype_workflow(project_name, project_description)
        else:
            run_cto_workflow(project_name, project_description)
            
    elif choice == "2":
        # List existing projects
        if not os.path.exists("outputs"):
            print("No existing projects found.")
            return
            
        # Get list of project directories
        projects = [d for d in os.listdir("outputs") if os.path.isdir(os.path.join("outputs", d))]
        if not projects:
            print("No existing projects found.")
            return
            
        print("\nExisting projects:")
        for i, project in enumerate(projects, 1):
            print(f"{i}. {project}")
            
        project_choice = int(input("\nSelect a project to reopen (enter number): ")) - 1
        if 0 <= project_choice < len(projects):
            project_name = projects[project_choice]
            project_dir = os.path.join("outputs", project_name)
            
            # Get project description
            description_path = os.path.join(project_dir, "project_description.md")
            if os.path.exists(description_path):
                with open(description_path, "r") as f:
                    project_description = f.read()
                    # Strip the project name heading if present
                    project_description = re.sub(f"^# {project_name}\n\n", "", project_description)
            else:
                project_description = input("\nProject description not found. Please describe your project: ")
                
            # Check for incomplete workflow
            print("\nChecking project status...")
            
            # Define the sequence of files expected for each workflow
            prototype_files = [
                ("technical_approach", "Technical Approach"),
                ("prototype_requirements", "Prototype Requirements"),
                ("implementation_plan", "Implementation Plan"),
                ("engineering_tasks", "Engineering Tasks")
            ]
            
            cto_files = [
                ("technical_architecture", "Technical Architecture"),
                ("product_requirements", "Product Requirements"),
                ("engineering_plan", "Engineering Plan"),
                ("engineering_tasks", "Engineering Tasks")
            ]
            
            # Determine which workflow was used
            workflow_files = prototype_files
            workflow_type = "prototype"
            
            # Check for CTO workflow files
            if any(os.path.exists(os.path.join(project_dir, f"*{file_prefix}*.md")) for file_prefix, _ in cto_files):
                workflow_files = cto_files
                workflow_type = "cto"
            
            # Find the most recent version of each file type
            existing_files = {}
            missing_files = []
            
            for file_prefix, file_desc in workflow_files:
                # Find files matching the pattern
                matching_files = [f for f in os.listdir(project_dir) 
                                 if f.startswith(file_prefix) and f.endswith(".md")]
                
                if matching_files:
                    # Sort by timestamp (newest first)
                    matching_files.sort(reverse=True)
                    existing_files[file_prefix] = os.path.join(project_dir, matching_files[0])
                    print(f"✓ {file_desc}: {matching_files[0]}")
                else:
                    missing_files.append((file_prefix, file_desc))
                    print(f"✗ {file_desc}: Missing")
            
            if missing_files:
                print("\nThis project has incomplete steps that can be resumed.")
                print("Options:")
                print("1. View existing files")
                print("2. Resume workflow from incomplete step")
                resume_choice = input("\nEnter your choice (1 or 2): ")
                
                if resume_choice == "1":
                    # Show existing files (original behavior)
                    files = os.listdir(project_dir)
                    if not files:
                        print(f"No files found in project {project_name}.")
                        return
                        
                    print(f"\nFiles in project '{project_name}':")
                    for i, file in enumerate(files, 1):
                        print(f"{i}. {file}")
                        
                    file_choice = int(input("\nSelect a file to view (enter number): ")) - 1
                    if 0 <= file_choice < len(files):
                        file_path = os.path.join(project_dir, files[file_choice])
                        with open(file_path, "r") as f:
                            content = f.read()
                            print(f"\nContent of {files[file_choice]}:")
                            print(content)
                    else:
                        print("Invalid file selection.")
                elif resume_choice == "2":
                    # Resume workflow
                    print("\nResuming workflow from incomplete step...")
                    
                    # Load existing outputs for the resume
                    tech_response = None
                    planner_response = None
                    developer_response = None
                    
                    # For prototype workflow
                    if workflow_type == "prototype":
                        # Initialize agents
                        prototype_planner = ProductManager()
                        technical_advisor = CTO()
                        prototype_developer = EngineeringManager()
                        task_generator = TaskGenerator()
                        
                        # Load existing outputs
                        if "prototype_requirements" in existing_files:
                            with open(existing_files["prototype_requirements"], "r") as f:
                                req_content = f.read()
                            planner_response = AgentResponse('{"command": "pass-on", "content": ' + json.dumps(req_content) + '}')
                            
                        if "technical_approach" in existing_files:
                            with open(existing_files["technical_approach"], "r") as f:
                                tech_content = f.read()
                            tech_response = AgentResponse('{"command": "pass-on", "content": ' + json.dumps(tech_content) + '}')
                            
                        if "implementation_plan" in existing_files:
                            with open(existing_files["implementation_plan"], "r") as f:
                                impl_content = f.read()
                            developer_response = AgentResponse('{"command": "pass-on", "content": ' + json.dumps(impl_content) + '}')
                        
                        # Resume from the earliest missing step, in the correct order
                        # 1. Prototype Requirements
                        if "prototype_requirements" not in existing_files:
                            print("\nResuming from Prototype Requirements step...")
                            print("\nPrototype Planner is defining core features...")
                            planner_response = prototype_planner.evaluate_project(project_description)
                            planner_file = save_to_markdown(planner_response, "prototype_requirements", project_name)
                            print(f"\nPrototype requirements saved to: {planner_file}")
                            while planner_response.needs_followup:
                                print("\nPrototype Planner has some questions about core functionality:")
                                display_questions(planner_response)
                                additional_info = input("\nPlease provide additional information: ")
                                project_description += "\n\nAdditional Feature Information:\n" + additional_info
                                planner_response = prototype_planner.evaluate_project(project_description)
                                planner_file = save_to_markdown(planner_response, "prototype_requirements", project_name)
                                print(f"\nUpdated prototype requirements saved to: {planner_file}")
                            # After this, update existing_files so next steps can use the new file
                            existing_files["prototype_requirements"] = planner_file

                        # 2. Technical Approach
                        if "technical_approach" not in existing_files:
                            print("\nResuming from Technical Approach step...")
                            print("\nTechnical Advisor is suggesting practical technologies for your prototype...")
                            # Always load the latest requirements
                            with open(existing_files["prototype_requirements"], "r") as f:
                                req_content = f.read()
                            planner_response = AgentResponse('{"command": "pass-on", "content": ' + json.dumps(req_content) + '}')
                            tech_response = technical_advisor.evaluate_project(planner_response)
                            tech_file = save_to_markdown(tech_response, "technical_approach", project_name)
                            print(f"\nTechnical approach saved to: {tech_file}")
                            while tech_response.needs_followup:
                                print("\nTechnical Advisor needs some clarification about your prototype:")
                                display_questions(tech_response)
                                additional_info = input("\nPlease provide additional information: ")
                                project_description += "\n\nAdditional Information:\n" + additional_info
                                tech_response = technical_advisor.evaluate_project(planner_response)
                                tech_file = save_to_markdown(tech_response, "technical_approach", project_name)
                                print(f"\nUpdated technical approach saved to: {tech_file}")
                            existing_files["technical_approach"] = tech_file

                        # 3. Implementation Plan
                        if "implementation_plan" not in existing_files:
                            print("\nResuming from Implementation Plan step...")
                            print("\nPrototype Developer is creating a practical implementation plan...")
                            # Always load the latest requirements and tech approach
                            with open(existing_files["prototype_requirements"], "r") as f:
                                req_content = f.read()
                            planner_response = AgentResponse('{"command": "pass-on", "content": ' + json.dumps(req_content) + '}')
                            with open(existing_files["technical_approach"], "r") as f:
                                tech_content = f.read()
                            tech_response = AgentResponse('{"command": "pass-on", "content": ' + json.dumps(tech_content) + '}')
                            developer_response = prototype_developer.create_task_list(planner_response, tech_response)
                            developer_file = save_to_markdown(developer_response, "implementation_plan", project_name)
                            print(f"\nImplementation plan saved to: {developer_file}")
                            while developer_response.needs_followup:
                                print("\nPrototype Developer has some implementation questions:")
                                display_questions(developer_response)
                                additional_info = input("\nPlease provide additional information: ")
                                project_description += "\n\nAdditional Implementation Information:\n" + additional_info
                                developer_response = prototype_developer.create_task_list(planner_response, tech_response)
                                developer_file = save_to_markdown(developer_response, "implementation_plan", project_name)
                                print(f"\nUpdated implementation plan saved to: {developer_file}")
                            existing_files["implementation_plan"] = developer_file

                        # 4. Engineering Tasks
                        if "engineering_tasks" not in existing_files:
                            print("\nResuming from Engineering Tasks step...")
                            print("\nTask Generator is creating a detailed task list for engineers...")
                            # Always load the latest implementation plan and tech approach
                            with open(existing_files["implementation_plan"], "r") as f:
                                impl_content = f.read()
                            developer_response = AgentResponse('{"command": "pass-on", "content": ' + json.dumps(impl_content) + '}')
                            with open(existing_files["technical_approach"], "r") as f:
                                tech_content = f.read()
                            tech_response = AgentResponse('{"command": "pass-on", "content": ' + json.dumps(tech_content) + '}')
                            task_response = task_generator.generate_tasks(developer_response, tech_response)
                            task_file = save_to_markdown(task_response, "engineering_tasks", project_name)
                            print(f"\nDetailed engineering tasks saved to: {task_file}")
                            while task_response.needs_followup:
                                print("\nTask Generator has some questions about task breakdown:")
                                display_questions(task_response)
                                additional_info = input("\nPlease provide additional information: ")
                                task_response = task_generator.generate_tasks(developer_response, tech_response)
                                task_file = save_to_markdown(task_response, "engineering_tasks", project_name)
                                print(f"\nUpdated engineering tasks saved to: {task_file}")
                            existing_files["engineering_tasks"] = task_file
                            
                        print(f"\nPrototype plan for '{project_name}' completed!")
                        print(f"All outputs saved to: outputs/{project_name}/")
                    
                    # For CTO workflow
                    else:
                        # Similar structure to resume CTO workflow
                        # Initialize agents
                        technical_advisor = RobustCTO()
                        product_manager = RobustProductManager()
                        engineering_manager = RobustEngineeringManager()
                        task_generator = TaskGenerator()
                        
                        # Load existing outputs
                        if "technical_architecture" in existing_files:
                            with open(existing_files["technical_architecture"], "r") as f:
                                tech_content = f.read()
                            tech_response = AgentResponse('{"command": "pass-on", "content": ' + json.dumps(tech_content) + '}')
                            
                        if "product_requirements" in existing_files:
                            with open(existing_files["product_requirements"], "r") as f:
                                req_content = f.read()
                            product_response = AgentResponse('{"command": "pass-on", "content": ' + json.dumps(req_content) + '}')
                            
                        if "engineering_plan" in existing_files:
                            with open(existing_files["engineering_plan"], "r") as f:
                                eng_content = f.read()
                            engineering_response = AgentResponse('{"command": "pass-on", "content": ' + json.dumps(eng_content) + '}')
                        
                        # Resume from the earliest missing step
                        if "technical_architecture" not in existing_files:
                            print("\nResuming from Technical Architecture step...")
                            # CTO evaluation
                            print("\nCTO is designing a robust technical architecture...")
                            tech_response = technical_advisor.evaluate_project(project_description)
                            tech_file = save_to_markdown(tech_response, "technical_architecture", project_name)
                            print(f"\nTechnical architecture saved to: {tech_file}")
                            
                            # Handle follow-up questions if needed
                            while tech_response.needs_followup:
                                print("\nCTO needs more information about your long-term vision:")
                                display_questions(tech_response)
                                additional_info = input("\nPlease provide additional information: ")
                                project_description += "\n\nAdditional Information:\n" + additional_info
                                tech_response = technical_advisor.evaluate_project(project_description)
                                tech_file = save_to_markdown(tech_response, "technical_architecture", project_name)
                                print(f"\nUpdated technical architecture saved to: {tech_file}")
                        
                        if "product_requirements" not in existing_files:
                            print("\nResuming from Product Requirements step...")
                            # Product Strategy evaluation
                            print("\nProduct Strategy Manager is defining comprehensive requirements...")
                            product_response = product_manager.evaluate_project(project_description, tech_response)
                            product_file = save_to_markdown(product_response, "product_requirements", project_name)
                            print(f"\nProduct requirements saved to: {product_file}")
                            
                            # Handle follow-up questions if needed
                            while product_response.needs_followup:
                                print("\nProduct Strategy Manager has questions about product vision:")
                                display_questions(product_response)
                                additional_info = input("\nPlease provide additional information: ")
                                project_description += "\n\nAdditional Product Information:\n" + additional_info
                                product_response = product_manager.evaluate_project(project_description, tech_response)
                                product_file = save_to_markdown(product_response, "product_requirements", project_name)
                                print(f"\nUpdated product requirements saved to: {product_file}")
                        
                        if "engineering_plan" not in existing_files:
                            print("\nResuming from Engineering Plan step...")
                            # Engineering Lead implementation plan
                            print("\nEngineering Lead is creating a robust implementation plan...")
                            engineering_response = engineering_manager.create_task_list(product_response, tech_response)
                            engineering_file = save_to_markdown(engineering_response, "engineering_plan", project_name)
                            print(f"\nEngineering plan saved to: {engineering_file}")
                            
                            # Handle follow-up questions if needed
                            while engineering_response.needs_followup:
                                print("\nEngineering Lead has some implementation questions:")
                                display_questions(engineering_response)
                                additional_info = input("\nPlease provide additional information: ")
                                project_description += "\n\nAdditional Technical Information:\n" + additional_info
                                engineering_response = engineering_manager.create_task_list(product_response, tech_response)
                                engineering_file = save_to_markdown(engineering_response, "engineering_plan", project_name)
                                print(f"\nUpdated engineering plan saved to: {engineering_file}")
                        
                        if "engineering_tasks" not in existing_files:
                            print("\nResuming from Engineering Tasks step...")
                            # Generate detailed task list
                            print("\nTask Generator is creating a detailed task list for engineers...")
                            task_response = task_generator.generate_tasks(engineering_response, tech_response)
                            task_file = save_to_markdown(task_response, "engineering_tasks", project_name)
                            print(f"\nDetailed engineering tasks saved to: {task_file}")
                            
                            # Handle follow-up questions if needed
                            while task_response.needs_followup:
                                print("\nTask Generator has some questions about task breakdown:")
                                display_questions(task_response)
                                additional_info = input("\nPlease provide additional information: ")
                                project_description += "\n\nAdditional Task Information:\n" + additional_info
                                task_response = task_generator.generate_tasks(engineering_response, tech_response)
                                task_file = save_to_markdown(task_response, "engineering_tasks", project_name)
                                print(f"\nUpdated engineering tasks saved to: {task_file}")
                            
                        print(f"\nRobust software plan for '{project_name}' completed!")
                        print(f"All outputs saved to: outputs/{project_name}/")
                    
                else:
                    print("Invalid choice.")
            else:
                # All files exist, just show files as in original behavior
                print("\nAll workflow steps are complete for this project.")
                print("Options:")
                print("1. View existing files")
                print("2. Regenerate the last step (Engineering Tasks)")
                
                view_choice = input("\nEnter your choice (1 or 2): ")
                
                if view_choice == "1":
                    # Show existing files (original behavior)
                    files = os.listdir(project_dir)
                    print(f"\nFiles in project '{project_name}':")
                    for i, file in enumerate(files, 1):
                        print(f"{i}. {file}")
                        
                    file_choice = int(input("\nSelect a file to view (enter number): ")) - 1
                    if 0 <= file_choice < len(files):
                        file_path = os.path.join(project_dir, files[file_choice])
                        with open(file_path, "r") as f:
                            content = f.read()
                            print(f"\nContent of {files[file_choice]}:")
                            print(content)
                    else:
                        print("Invalid file selection.")
                elif view_choice == "2":
                    # Regenerate the task list using either workflow
                    if workflow_type == "prototype":
                        # Load dependencies
                        with open(existing_files["implementation_plan"], "r") as f:
                            impl_content = f.read()
                        developer_response = AgentResponse('{"command": "pass-on", "content": ' + json.dumps(impl_content) + '}')
                        
                        with open(existing_files["technical_approach"], "r") as f:
                            tech_content = f.read()
                        tech_response = AgentResponse('{"command": "pass-on", "content": ' + json.dumps(tech_content) + '}')
                        
                        # Generate task list
                        task_generator = TaskGenerator()
                        print("\nRegenerating task list...")
                        task_response = task_generator.generate_tasks(developer_response, tech_response)
                        task_file = save_to_markdown(task_response, "engineering_tasks", project_name)
                        print(f"\nUpdated engineering tasks saved to: {task_file}")
                    else:
                        # Load dependencies
                        with open(existing_files["engineering_plan"], "r") as f:
                            eng_content = f.read()
                        engineering_response = AgentResponse('{"command": "pass-on", "content": ' + json.dumps(eng_content) + '}')
                        
                        with open(existing_files["technical_architecture"], "r") as f:
                            tech_content = f.read()
                        tech_response = AgentResponse('{"command": "pass-on", "content": ' + json.dumps(tech_content) + '}')
                        
                        # Generate task list
                        task_generator = TaskGenerator()
                        print("\nRegenerating task list...")
                        task_response = task_generator.generate_tasks(engineering_response, tech_response)
                        task_file = save_to_markdown(task_response, "engineering_tasks", project_name)
                        print(f"\nUpdated engineering tasks saved to: {task_file}")
                else:
                    print("Invalid choice.")
        else:
            print("Invalid project selection.")
    else:
        print("Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    main() 