import os
import dotenv
from crewai import Agent, Task, Crew
# Importing crewAI tools
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool
)

# Set up API keys
dotenv.load_dotenv() 

OPENAI_KEY = os.getenv("OPENAI_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_KEY

# Instantiate tools
tool_projects = DirectoryReadTool(directory='/users/luis/Documents/obsvault/Projects/')
tool_meetings = DirectoryReadTool(directory='/users/luis/Documents/obsvault/Meetings/')
file_tool = FileReadTool()


agent_coordinator = Agent(
    role='Technical manager',
    goal='work as technical manager for the project {project}, so use your knowledge to answer questions about it to the other agents, and make a summary of the project, and suggest next steps.',
    backstory='A skilled expert technical manager.',
    verbose=True

)

task_agent_coordinator = Task(
    description='I need your help as a technical manager, investigate about the project {project} and make a summary of its meetings giving more importance to the latest ones, and suggest me next steps',
    expected_output='A summary about the project {project} from the point of view of a technical manager, showing the status of the project, suggest next steps based on action points, what gaps do you see in the documentation of the project, do you miss action points, meeting details?, if you miss details please point it. Ask the other agents about the details, write a 4-paragraph summary formatted in markdown with engaging, informative, and accessible content, avoiding complex jargon.',
    agent=agent_coordinator
)

agent_meetings = Agent(
    role='Project manager specialized in meetings',
    goal='answer questions about the meetings of project {project}',
    backstory='A skilled expert in meetings.',
    tools=[tool_meetings, file_tool],
    verbose=True, 
    manager=agent_coordinator
)

task_agent_meetings = Task(
    description='give to the coordinator a summary of the meetings of project {project}',
    expected_output='A 4-paragraph summary formatted in markdown with engaging, informative, and accessible content, avoiding complex jargon.',
    agent=agent_meetings
)

agent_projects = Agent(
    role='Project manager specialized in projects',
    goal='answer questions about the  of project {project}',
    backstory='A skilled expert in projects.',
    tools=[tool_projects, file_tool],
    verbose=True,
    manager=agent_coordinator
)
    


task_agent_projects = Task(
    description='give to the coordinator a summary of the project he ask for',
    expected_output='A 4-paragraph summary formatted in markdown with engaging, informative, and accessible content, avoiding complex jargon.',
    agent=agent_projects,
    context=[task_agent_coordinator]
)

# Assemble a crew
from crewai.process import Process

crew = Crew(
    agents=[agent_coordinator, agent_meetings, agent_projects],
    tasks=[task_agent_coordinator],
    process=Process.sequential,
    verbose=2,
    share_crew=True
)

# Execute tasks
crew.kickoff(inputs={'project': 'IBERDROLA'})


