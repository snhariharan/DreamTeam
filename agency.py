import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import FileReadTool, DirectoryReadTool

# Import the model providers
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

# ==========================================
# 1. API KEYS & ENVIRONMENT SETUP
# ==========================================
# Set these in your terminal, or replace the strings here (not recommended for production)
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "your-openai-key")
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY", "your-anthropic-key")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "your-google-key")

# ==========================================
# 2. CONFIGURE THE LATEST FRONTIER MODELS
# ==========================================
# Manager: Claude Opus 4.6 (Best for adaptive thinking and managing parallel agent workflows)
manager_llm = ChatAnthropic(model_name="claude-3-opus", temperature=0.2)

# Architect: Gemini 3.1 Pro (Massive context window for reading massive code repositories)
architect_llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.2)

# Developer: GPT-5 (State-of-the-art coding and agentic tool execution)
developer_llm = ChatOpenAI(model="gpt-4", temperature=0.1)

# Reviewer/Tester: Claude Sonnet 4.6 (Perfect balance of extreme speed and intelligence)
reviewer_llm = ChatAnthropic(model_name="claude-3-sonnet", temperature=0.1)


# ==========================================
# 3. ASSIGN SKILLS (TOOLS)
# ==========================================
# Leaving these empty allows the agents to dynamically choose which files/folders to read
read_dir_tool = DirectoryReadTool()
read_file_tool = FileReadTool()


# ==========================================
# 4. DEFINE THE ROLES (AGENTS)
# ==========================================

architect = Agent(
    role='Software Architect',
    goal='Analyze the current source code and design the system architecture for new tasks.',
    backstory='You are a Staff-level Software Architect. You read existing codebases and plan safe, scalable integrations.',
    tools=[read_dir_tool, read_file_tool],
    llm=architect_llm,
    allow_delegation=False,
    verbose=True
)

developer = Agent(
    role='Senior Developer',
    goal='Write clean, efficient Python code based on the tasks and architectural design.',
    backstory='You are a 10x Senior Software Engineer. You write DRY, SOLID code using GPT-5 capabilities.',
    tools=[read_dir_tool, read_file_tool],
    llm=developer_llm,
    allow_delegation=False,
    verbose=True
)

reviewer = Agent(
    role='Principal Code Reviewer',
    goal='Review the Developer\'s code against the original task list and existing codebase context.',
    backstory='You are a strict Principal Engineer. You reject code that breaks existing functionality.',
    tools=[read_dir_tool, read_file_tool],
    llm=reviewer_llm,
    allow_delegation=False,
    verbose=True
)


# ==========================================
# 5. DEFINE DYNAMIC TASKS
# ==========================================
# Notice the {placeholders}. We will inject the source code path and task list at runtime.

analysis_task = Task(
    description='Read the task list located at {task_file}. Then, explore the existing codebase in the {source_directory} folder. Draft a technical implementation plan.',
    expected_output='A markdown document detailing the files to change and the architecture to use.',
    agent=architect
)

coding_task = Task(
    description='Using the Architect\'s plan, implement the requested features. You may read the files in {source_directory} to ensure compatibility.',
    expected_output='The final Python source code files updated with the new features.',
    agent=developer
)

review_task = Task(
    description='Review the newly written code against the original requirements in {task_file}.',
    expected_output='A final review report. Pass the code if it is perfect, or fail it with specific fix instructions.',
    agent=reviewer
)


# ==========================================
# 6. ASSEMBLE AND KICKOFF
# ==========================================

SOURCE_DIRECTORY = './src'

software_agency = Crew(
    agents=[architect, developer, reviewer],
    tasks=[analysis_task, coding_task, review_task],
    process=Process.hierarchical,
    manager_llm=manager_llm, # Claude Opus 4.6 handles the delegation
    verbose=True
)

if __name__ == "__main__":
    print("🚀 Booting up Multi-Model AI Agency...")

    # Define your inputs dynamically here
    project_inputs = {
        'task_file': './project_tasks.md',
        'source_directory': SOURCE_DIRECTORY
    }

    # Ensure dummy files exist for this example to run without crashing
    if not os.path.exists(SOURCE_DIRECTORY):
        os.makedirs(SOURCE_DIRECTORY)
    with open('./project_tasks.md', 'w') as f:
        f.write("Task 1: Add a health check endpoint to the existing API.")

    final_result = software_agency.kickoff(inputs=project_inputs)

    print("\n\n========================================")
    print("🏆 FINAL DELIVERABLE")
    print("========================================")
    print(final_result)