from agno.agent import Agent
from agno.tools.yfinance import YFinanceTools
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
from agno.db.sqlite import SqliteDb
import os

load_dotenv()

db = SqliteDb(db_file='./tmp/analist.db')


model = OpenAIChat(id='gpt-5-nano')

agent = Agent(
  name="Analist",
  tools=[YFinanceTools()],
  model=model,
  instructions="Você é um analista financeiro especializado em fornecer cotações de ações e previsões de mercado. Utilize as ferramentas disponíveis para obter as informações mais recentes e precisas.",
  add_history_to_context=True,
  db=db,
  num_history_runs=3,
  enable_user_memories=True,
  add_memories_to_context=True,
  enable_agentic_memory=True
)

agent.print_response("Cotação atual da Magazine Luiza e previsão para os próximos dias.", stream=True, session_id="session_1", user_id="user_1")

agent.print_response("Cotação atual da Alphabet", stream=True, session_id="session_2", user_id="user_1")

agent.print_response("Quais empresas já consultamos?", stream=True, session_id="session_3", user_id="user_2")