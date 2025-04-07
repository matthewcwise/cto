import os
import re
from utils.agents import (
    CTO, ProductManager, EngineeringManager, 
    RobustCTO, RobustProductManager, RobustEngineeringManager,
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

def display_questions(agent_response):
    """Display questions from an agent response in a user-friendly format."""
    if agent_response.questions:
        print("\nThe following questions need to be addressed:")
        for i, question in enumerate(agent_response.questions, 1):
            print(f"{i}. {question}")
    else:
        # If no structured questions found but needs followup,
        # display the content which likely contains questions
        print("\nFollowing feedback requires your attention:")
        print(agent_response.content)

def run_prototype_workflow(project_name, project_description):
    """Run the rapid prototype workflow."""
    print("\n--- RAPID PROTOTYPE WORKFLOW ---")
    print("This workflow focuses on quick implementation and minimal viable features.")
    
    # Initialize agents
    technical_advisor = CTO()
    prototype_planner = ProductManager()
    prototype_developer = EngineeringManager()
    
    # Save project description to a file
    os.makedirs(os.path.join("outputs", project_name), exist_ok=True)
    with open(os.path.join("outputs", project_name, "project_description.md"), "w") as f:
        f.write(f"# {project_name}\n\n{project_description}")
    
    # Technical Advisor evaluation
    print("\nTechnical Advisor is suggesting practical technologies for your prototype...")
    tech_response = technical_advisor.evaluate_project(project_description)
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
    
    # Prototype Planner evaluation
    print("\nPrototype Planner is defining core features...")
    planner_response = prototype_planner.evaluate_project(project_description, tech_response)
    planner_file = save_to_markdown(planner_response, "prototype_requirements", project_name)
    print(f"\nPrototype requirements saved to: {planner_file}")
    
    # Loop through Planner follow-up questions if needed
    while planner_response.needs_followup:
        print("\nPrototype Planner has some questions about core functionality:")
        display_questions(planner_response)
            
        additional_info = input("\nPlease provide additional information: ")
        project_description += "\n\nAdditional Feature Information:\n" + additional_info
        planner_response = prototype_planner.evaluate_project(project_description, tech_response)
        planner_file = save_to_markdown(planner_response, "prototype_requirements", project_name)
        print(f"\nUpdated prototype requirements saved to: {planner_file}")
    
    # Prototype Developer implementation plan
    print("\nPrototype Developer is creating a practical implementation plan...")
    developer_response = prototype_developer.create_task_list(planner_response, tech_response)
    developer_file = save_to_markdown(developer_response, "implementation_plan", project_name)
    print(f"\nImplementation plan saved to: {developer_file}")
    
    # Loop through Developer follow-up questions if needed
    while developer_response.needs_followup:
        print("\nPrototype Developer has some implementation questions:")
        display_questions(developer_response)
            
        additional_info = input("\nPlease provide additional information: ")
        project_description += "\n\nAdditional Implementation Information:\n" + additional_info
        developer_response = prototype_developer.create_task_list(planner_response, tech_response)
        developer_file = save_to_markdown(developer_response, "implementation_plan", project_name)
        print(f"\nUpdated implementation plan saved to: {developer_file}")
    
    print(f"\nPrototype plan for '{project_name}' completed!")
    print(f"All outputs saved to: outputs/{project_name}/")
    print(f"\nYour prototype development plan includes:")
    print(f"1. Technical Approach: {tech_file}")
    print(f"2. Prototype Requirements: {planner_file}")
    print(f"3. Implementation Plan: {developer_file}")

def run_cto_workflow(project_name, project_description):
    """Run the CTO workflow for robust, scalable software."""
    print("\n--- CTO WORKFLOW FOR ROBUST SOFTWARE ---")
    print("This workflow focuses on scalability, maintainability, and long-term architecture.")
    
    # Initialize agents
    technical_advisor = RobustCTO()
    product_manager = RobustProductManager()
    engineering_manager = RobustEngineeringManager()
    
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
    
    print(f"\nRobust software plan for '{project_name}' completed!")
    print(f"All outputs saved to: outputs/{project_name}/")
    print(f"\nYour comprehensive development plan includes:")
    print(f"1. Technical Architecture: {tech_file}")
    print(f"2. Product Requirements: {product_file}")
    print(f"3. Engineering Plan: {engineering_file}")

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
            
            # Find the most recent files in the project directory
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
        else:
            print("Invalid project selection.")
    else:
        print("Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    main() 