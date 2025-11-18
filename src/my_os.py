from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.os import AgentOS

from dotenv import load_dotenv
load_dotenv()

assistant = Agent(
    name="Assistant",
    model=OpenAIChat(id="gpt-5-nano", reasoning_effort="low"),
    instructions=["You are a helpful AI assistant."],
    markdown=True,
)

agent_os = AgentOS(
    id="my-first-os",
    description="My first AgentOS",
    agents=[assistant],
)

app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="my_os:app", reload=True)