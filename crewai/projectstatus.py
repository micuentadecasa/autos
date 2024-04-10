import os
import dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import DirectoryReadTool, DirectorySearchTool, FileReadTool, PDFSearchTool, TXTSearchTool, CSVSearchTool

# Set up API keys
dotenv.load_dotenv() 

OPENAI_KEY = os.getenv("OPENAI_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_KEY

# Dummy folder paths - replace these with your actual paths
projects_folder = "/users/luis/Documents/obsvault/Projects/"
meetings_folder = "/users/luis/Documents/obsvault/Meetings/"
people_folder = "/users/luis/Documents/obsvault/People/"
one_on_ones_folder = "/users/luis/Documents/obsvault/1on1/"

# Initialize tools capable of searching and reading .md files
directory_search_tool = DirectorySearchTool()
file_read_tool = FileReadTool(file_types=['.md'])

tool_projects = DirectoryReadTool(directory='/users/luis/Documents/obsvault/Projects/')
tool_meetings = DirectoryReadTool(directory='/users/luis/Documents/obsvault/Meetings/')
tool_1on1 = DirectoryReadTool(directory='/users/luis/Documents/obsvault/1on1/')
tool_People = DirectoryReadTool(directory='/users/luis/Documents/obsvault/People/')


# Define Agents
project_manager_agent = Agent(
    role='Project Manager',
    goal='answer questions about the project {project_name}',
    backstory="Experienced in leading technical projects from conception to completion, ensuring all aspects of the projects align with organizational goals and client expectations.",
    tools=[tool_projects, file_read_tool],
    verbose=True,
    memory=True
)

meeting_coordinator_agent = Agent(
    role='Project manager specialized in meetings',
    goal='answer questions about the meetings of project {project_name}',
    backstory='A skilled expert in meetings.',
    tools=[tool_meetings, file_read_tool],
    verbose=True,
    memory=True
)

human_resources_agent = Agent(
    role='Human Resources',
    goal='Manage personnel records and 1on1 meeting notes.',
    backstory="Experienced in 1on1 facilitation, ensuring all 1on1 meetings are held according to the organization's guidelines.",
    tools=[tool_1on1, file_read_tool],
    verbose=True,
    memory=True
)

solutions_architect_agent = Agent(
    role='Solutions Architect',
    goal='Provide cloud development and design insights.',
    backstory="Experienced in cloud development and design, ensuring all cloud solutions are built according to the organization's guidelines.",
    verbose=True,
    memory=True
)

technical_manager_agent = Agent(
    role='Technical manager',
    goal='work as technical manager for the project {project_name}, so use your knowledge to answer questions about it to the other agents, and make a summary of the project, and suggest next steps.',
    backstory="Experienced in technical management, ensuring all projects are managed according to the organization's guidelines.",
    verbose=True
)

# Assuming each agent's task outputs are stored or passed in a manner that the Technical Manager can access
summarize_project_info_task = Task(
    description='I need your help as a technical manager, investigate about the project {project_name} and make a summary of its meetings giving more importance to the latest ones, and suggest me next steps',
    expected_output='A summary about the project {project_name} from the point of view of a technical manager, showing the status of the project, suggest next steps based on action points, what gaps do you see in the documentation of the project, do you miss action points, meeting details?, if you miss details please point it. Ask the other agents about the details, write a 4-paragraph summary formatted in markdown with engaging, informative, and accessible content, avoiding complex jargon.',
    agent=technical_manager_agent,
    async_execution=False
)



# Assembling the crew with the defined agents and a placeholder for the tasks
crew = Crew(
    agents=[
        project_manager_agent,
        meeting_coordinator_agent,
        human_resources_agent,
        solutions_architect_agent,
        technical_manager_agent
    ],
    tasks=[ summarize_project_info_task],  # You'll need to create and add specific tasks for each agent
    process=Process.sequential,
    share_crew=True
)

# Example of kicking off the crew for a specific project
project_name = "ENDESA"
result = crew.kickoff(inputs={'project_name': project_name})
print(result)