
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
from agno.team.team import Team
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

model = OpenAIChat(id='gpt-5-nano', api_key=os.getenv("OPENAI_API_KEY"))

analista_team = Team(
    name="Team Analista",
    model=model,
    instructions=[
        "Você deve entender as informações solicitadas pelo usuário e fornecer uma resposta adequada.",
        "Para obter informações sobre balanço e DRE, utilize o analista_relatorios.",
        "Para obter informações sobre cotações, utilize o analista_cotacoes.",
        "Para obter informações sobre notícias, utilize o analista_noticias."
    ],
    db=db,
    add_history_to_context=True,
    num_history_runs=3,
    show_members_responses=True,
    get_member_information_tool=True,
    add_datetime_to_context=True,
    markdown=True,
    members=[
        Agent(
            name="analista_noticias",
            model=model,
            instructions="Use suas tools de busca para encontrar informações na web sobre empresas listadas na B3.",
            markdown=True,
        ),
        Agent(
            name="analista_cotacoes",
            model=model,
            tools=[YFinanceTools()],
            instructions="Você é um analista de cotações de empresas listadas na B3.",
            markdown=True,
        ),
        Agent(
            name="analista_relatorios",
            model=model,
            instructions="Você é um analista de relatórios de empresas listadas na B3.",
            knowledge=knowledge,
            add_knowledge_to_context=True,
            markdown=True,
        ),
    ]
)

# analista_team.print_response("Ola, qual foi o lucro liquido da petrobras em 2T25?", session_id="petrobras_session_4", user_id="analista_petrobras")
# analista_team.print_response("Ola, o que foi comentado sobre o CapEx da vale no 2T25?", session_id="vale_session_5", user_id="analista_vale")

analista_team.print_response("Qual a cotação da petrobras e quais noticias podem ter movimentado a cotação nos ultimos 10 dias? me traga alguma info rapido", session_id="petrobras_session_10", user_id="analista_petrobras")