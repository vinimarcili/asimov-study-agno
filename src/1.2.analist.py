from agno.agent import Agent
from agno.tools.yfinance import YFinanceTools
from agno.models.groq import Groq
from dotenv import load_dotenv
load_dotenv()

model = Groq(id='llama-3.3-70b-versatile')

agent = Agent(
  tools=[YFinanceTools()],
  model=model,
  instructions="Use tabelas para mostrar a informação final, não inclua nenhum outro texto",
)

agent.print_response("Cotação atual da Magazine Luiza e previsão para os próximos dias.", stream=True)