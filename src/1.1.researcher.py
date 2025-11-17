from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.models.groq import Groq
from dotenv import load_dotenv
load_dotenv()

model = Groq(id='llama-3.3-70b-versatile')

agent = Agent(
  tools=[TavilyTools()],
  model=model,
  debug_mode=True
)

agent.print_response("Use sua ferramentas para pesquisar sobre a história da inteligência artificial.")