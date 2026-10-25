from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq() # reads GROQ_API_KEY from the environment


for model in client.models.list().data:
    print(model.id)
