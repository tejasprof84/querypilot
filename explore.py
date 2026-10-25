from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq()

# 1. What does the client have?
print([name for name in dir(client) if not name.startswith("_")])

# 2. What does client.models have?
print([name for name in dir(client.models) if not name.startswith("_")])

# 3. What does the result look like?
result = client.models.list()
print(type(result))
print(result.data[0])