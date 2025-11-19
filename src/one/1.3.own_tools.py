from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
load_dotenv()

def celsius_to_fahrenheit(celsius: float) -> float:
  """
    Converts Celsius to Fahrenheit.
    
    Args:
      celsius (float): Temperature in Celsius.
      
    Returns:
      float: Temperature in Fahrenheit.
  """
  return (celsius * 9/5) + 32

def fahrenheit_to_celsius(fahrenheit: float) -> float:
  """
    Converts Fahrenheit to Celsius.
    
    Args:
      fahrenheit (float): Temperature in Fahrenheit.
    
    Returns:
      float: Temperature in Celsius.
  """
  return (fahrenheit - 32) * 5/9


model = OpenAIChat(id='gpt-5-nano')

agent = Agent(
  tools=[TavilyTools(), celsius_to_fahrenheit, fahrenheit_to_celsius],
  model=model,
  debug_mode=True
)

agent.print_response("Use sua ferramentas para pesquisar sobre temperatura em São Paulo amanhã. Mostre em Celsius e Fahrenheit. Responda somente com uma tabela e os resultados", stream=True)