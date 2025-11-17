from agno.models.groq import Groq
from agno.models.message import Message

from dotenv import load_dotenv
load_dotenv()

model = Groq(id='llama-3.3-70b-versatile')

msg = Message(
  role="user",
  content=[{
    "type": "text",
    "text": "Olá, meu nome é Vinícius"
  }]
)

assistant_msg = Message(
  role="assistant",
  content=[{
    "type": "text",
    "text": ""
  }]
)

response = model.invoke([msg], assistant_msg)

print(response.content)