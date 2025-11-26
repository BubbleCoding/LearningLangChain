import tools

from dataclasses import dataclass
import requests
from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver

#OSRS API
from osrs_api import Hiscores
osrs_wiki_url = "https://oldschool.runescape.wiki/api.php"

@dataclass
class Context:
    user_name: str
    item: str

@dataclass
class ResponseFormat:
    summary: str
    usage: str
    usability: str
    advice: str

@tool('get_highscore_stats', description="Get highscore statistics for a character", return_direct=False)
def get_highscore_stats(runtime: ToolRuntime[Context]):
    """Get highscore statistics for a character"""
    if tools.check_if_user_exists(runtime.context.user_name) is False:
        return("User does not exist.")
    response = Hiscores(runtime.context.user_name)
    return(response.skills)

@tool('find_item_information', description="Return item information", return_direct=False)
def find_item_information(runtime: ToolRuntime[Context]):
    """Return item information from the OSRS wiki"""
    params = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "titles": runtime.context.item,
        "rvslots": "main",
        "rvprop": "content"
    }
    response = requests.get(osrs_wiki_url, params=params)
    data = response.json()
    return(data)

model = init_chat_model('gpt-4.1-mini', temperature=0.3)

checkpointer = InMemorySaver()

agent = create_agent(
    model = model,
    tools = [find_item_information, get_highscore_stats],
    system_prompt = "You are a helpful assistant that provides information about Old School RuneScape item usage related to someone character stats.",
    context_schema=Context,
    response_format=ResponseFormat,
    checkpointer=checkpointer
)

config = {"configurable": {"thread_id": 1}}


response = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "Tell me about the usability of the given item."}
        ]
    },
    config=config,
    context=Context(user_name="Bubble IM", item="Dragon scimitar")
)

print(response['messages'][-1].content)

response = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "What would be a better item for me to use?"}
        ]
    },
    config=config,
    context=Context(user_name="Bubble IM", item="Dragon scimitar")
)

print(response['messages'][-1].content)