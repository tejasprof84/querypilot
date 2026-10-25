import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv() #load groq_api from .env to environment variable

llm = ChatGroq(model=os.environ["GROQ_MODEL"], temperature=0)

question  = "write a Postgresql query to count orders per month from a" \
"table orders(order_id,order_purchase_timestamp). "

response = llm.invoke(question)

print(response.content)