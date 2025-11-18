from agno.agent import Agent
from agno.tools.yfinance import YFinanceTools
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
from agno.db.sqlite import SqliteDb

from agno.vectordb.chroma import ChromaDb
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.knowledge.chunking.semantic import SemanticChunking
from agno.knowledge.embedder.openai import OpenAIEmbedder
import os

load_dotenv()

db = SqliteDb(db_file='./tmp/analist.db')

vector_db = ChromaDb(
    collection="empresas_relatorios",
    path="tmp/chromadb",
    embedder=OpenAIEmbedder(id="text-embedding-3-small", api_key=os.getenv("OPENAI_API_KEY")),
    persistent_client=True
)

knowledge = Knowledge(
    vector_db=vector_db,
)

knowledge.add_content(
    path="./src/files/PETR/",
    reader=PDFReader(
        chunck_strategy=SemanticChunking()
    ),
    metadata={
        "company": "Petrobras",
        "sector": "Petróleo e Gás",
        "country": "Brazil",
    },
    skip_if_exists=True
)

knowledge.add_content(
    path="./src/files/VALE/",
    reader=PDFReader(
        chunck_strategy=SemanticChunking()
    ),
    metadata={
        "company": "Vale",
        "sector": "Mineração",
        "country": "Brazil",
    },
    skip_if_exists=True
)

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
  enable_agentic_memory=True,
  add_knowledge_to_context=True,
  knowledge=knowledge
)

agent.print_response("Ola, qual foi o lucro liquido da petrobras em 2T25?", session_id="petrobras_session_4", user_id="analista_petrobras")
agent.print_response("Ola, o que foi comentado sobre o CapEx da vale no 2T25?", session_id="vale_session_5", user_id="analista_vale")