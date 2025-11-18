# Agno Study Project - AI Agent Instructions

This is a learning repository for the Azimov Academy course focused on **Agno** (v2.x), a framework for building AI agents with LLMs. The codebase contains practical examples organized by learning modules.

## Project Architecture

### Repository Structure
- **`src/`**: Core examples demonstrating basic Agno patterns (LLM calls, agents, custom tools, AgentOS)
- **`guides/modules/`**: Structured learning modules with progressive complexity
  - `one/`: Foundation - Basic agents, tools, PDF processing, memory, teams
  - `two/`: Advanced - Financial analysis with RAG (Petrobras/Vale reports), multi-agent teams
  - `three/`: Deployment - FastAPI integration and production patterns
- **`src/agent-ui/`**: Next.js chat interface for AgentOS instances (separate frontend)

### Key Framework Patterns

**Agent Creation (Standard Pattern)**
```python
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.tavily import TavilyTools

agent = Agent(
    model=Groq(id='llama-3.3-70b-versatile'),
    tools=[TavilyTools()],
    instructions="Your specific instructions here",
    debug_mode=True  # Common for learning examples
)
agent.print_response("query", stream=True)
```

**AgentOS Pattern** (for serving agents via API):
```python
from agno.os import AgentOS
agent_os = AgentOS(id="my-os", agents=[agent])
app = agent_os.get_app()
# Serve: agent_os.serve(app="module:app", reload=True)
```

**RAG with Knowledge Base**:
- Vector DB: ChromaDb (persistent, collection-based) stored in `tmp/chromadb/`
- Knowledge: PDFKnowledgeBase or Knowledge class with PDFReader
- Pattern: `knowledge.load(recreate=True)` before use, `search_knowledge=True` on agent
- See: `guides/modules/one/21_pdf_agent.py`, `guides/modules/two/17_team_analista.py`

**Memory Pattern**:
```python
from agno.memory.v2.memory import Memory
from agno.memory.v2.db.sqlite import SqliteMemoryDb

memory = Memory(
    model=OpenAIChat(id="gpt-4.1-mini"),
    db=SqliteMemoryDb(table_name="user_memories", db_file="tmp/agent.db")
)
agent = Agent(memory=memory, enable_agentic_memory=True, ...)
```

**Team Pattern** (multi-agent routing):
- Mode: `"route"` (router selects appropriate agent based on query)
- Members: List of specialized agents
- See: `guides/modules/one/41_teams.py` (language routing), `guides/modules/two/17_team_analista.py` (financial analysis team)

## Development Workflows

### Environment Setup
- Python: 3.14+ (specified in `pyproject.toml`)
- Dependencies: Managed via project `pyproject.toml` (not Poetry/pip-tools)
- Environment: `.env` file required (not tracked) with API keys:
  - `OPENAI_API_KEY`, `GROQ_API_KEY`, `TAVILY_API_KEY`

### Running Examples
**Python agents**: `python src/1.1.researcher.py` or module files directly
**AgentOS with Playground**: 
```python
from agno.playground import Playground, serve_playground_app
app = Playground(agents=[agent]).get_app()
serve_playground_app("module:app", reload=True)
```

**Agent UI (Next.js)**:
```bash
cd src/agent-ui
pnpm dev  # Runs on port 3000
# Connects to AgentOS backend via endpoints in store
```

### Storage Conventions
- SQLite DBs: `tmp/agent.db`, `tmp/data.db` (session storage, memory)
- ChromaDB: `tmp/chromadb/` with named collections
- File uploads: `files/PETR/`, `files/VALE/` (PDF reports for RAG examples)

## Project-Specific Conventions

### Model Selection Patterns
- **Groq**: `llama-3.3-70b-versatile` (fast inference, common in examples)
- **OpenAI**: `gpt-5-nano` (cost-effective), `gpt-4.1-mini`, `gpt-4o` (capabilities)
- Models wrapped: `Groq(id=...)`, `OpenAIChat(id=...)`

### Portuguese Language Context
- All instructions and prompts are in **Brazilian Portuguese**
- Example: `"Você é um pesquisador. Responda sempre chamando o usuário de senhor."`
- File names use English, but code comments and agent instructions are Portuguese

### Custom Tools Pattern
Functions become tools by adding docstrings with proper Args/Returns format:
```python
def celsius_to_fahrenheit(celsius: float) -> float:
    """Converts Celsius to Fahrenheit.
    Args: celsius (float): Temperature in Celsius.
    Returns: float: Temperature in Fahrenheit.
    """
    return (celsius * 9/5) + 32
# Pass directly to Agent: tools=[celsius_to_fahrenheit]
```

### Knowledge Base Metadata
When adding content to RAG systems, include contextual metadata:
```python
knowledge.add_content(
    path="files/PETR/",
    metadata={"company": "Petrobras", "sector": "Petróleo e Gás", "country": "Brazil"},
    skip_if_exists=True
)
```

## Agent UI Integration

The `src/agent-ui/` is a **standalone Next.js app** that connects to AgentOS backends:
- State: Zustand store (`src/store.ts`) with persistence
- API: Routes defined in `src/api/routes.ts` (health, agents, teams, sessions)
- Auth: Optional `NEXT_PUBLIC_OS_SECURITY_KEY` for secured endpoints
- Components: Chat interface with streaming support, tool calls visualization

## Common Tasks

**Add a new example**: Create numbered file in appropriate `guides/modules/` folder following existing pattern (e.g., `22_new_feature.py`)

**Switch LLM providers**: Import different model class and update `Agent(model=...)` - ensure API key in `.env`

**Test RAG locally**: Run module 2 examples after ensuring PDF files exist in `files/` directories

**Deploy agent as API**: Follow module 3 patterns - wrap agent in FastAPI, use `uvicorn.run()` with reload

**Debug agent behavior**: Set `debug_mode=True` on Agent to see tool calls and reasoning steps
