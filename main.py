import requests
from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain.tools import tool

#OSRS API
from osrs_api import Hiscores
osrs_wiki_url = "https://oldschool.runescape.wiki/api.php"

@tool('get_highscore_stats', description="Get highscore statistics for a character", return_direct=False)
def get_highscore_stats(character_name: str):
    """Get highscore statistics for a character"""
    response = Hiscores(character_name)
    return(response.skills)

@tool('find_item_information', description="Return item information", return_direct=False)
def find_item_information(item: str):
    """Return item information from the OSRS wiki"""
    params = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "titles": item,
        "rvslots": "main",
        "rvprop": "content"
    }
    response = requests.get(osrs_wiki_url, params=params)
    data = response.json()
    print(data)
    return(data)


agent = create_agent(
    model = 'gpt-4.1-mini',
    tools = [find_item_information],
    system_prompt = "You are a helpful assistant that provides information about Old School RuneScape items using the provided tool."
)

response = agent.invoke({
    "messages": [
        {"role": "user", "content": "Tell me about the item 'Dragon scimitar'."}
]})

print(response)
print(response['messages'][-1].content)