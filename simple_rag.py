# Retrieval-Augmented Generation or RAG is a way to include data which the model can use to respond to questions. This can be very useful when working with lots of data which the model is not trained on.

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.tools import tool
from langchain.agents import create_agent

embeddings = OpenAIEmbeddings(model ="text-embedding-3-small")

texts = [
    "Bandos is a great fight!",
    "The Dragon scimitar is a popular weapon among mid-level players.",
    "I think the grazi rapier is the best stab weapon in the game.",
    "The scythe is the very good for cutting grass.",
    "A rake is a great gardening tool.",
    "Compost is a very helpful to grow plants faster.",
    "Volcanic ash is used to make ultra compost."
]

vectorstore = FAISS.from_texts(texts, embedding=embeddings) #This is a vertorized database of the texts provided.

retriever = vectorstore.as_retriever(search_kwargs={"k":3}) #This is an object which langchain will use to search the vector database.

@tool("kb_search", description="Search the data base for information about Old School RuneScape items and tools.")
def kb_search(query: str):
    return retriever.invoke(query)

llm = ChatOpenAI(model='gpt-4o-mini')
agent = create_agent(
    llm,
    tools = [kb_search],
    system_prompt= "You are a helpful assistant that provides information about Old School RuneScape items using the provided tool. First call the kb_search tool to find relevant information, then use that information to answer the user's question."
)

result = agent.invoke({
    "messages": [
        {"role": "user", "content": "What is the best weapon in OldSchool Runescape?"}
]})

print(result['messages'][-1].content)