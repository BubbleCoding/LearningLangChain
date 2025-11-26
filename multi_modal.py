from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model

model = init_chat_model('gpt-4.1-mini', temperature=0.3)

message = {
    "role": "user",
    "content": [
        {"type": "text", "text": "What is this image?"},
        {"type": "image", "url": "https://oldschool.runescape.wiki/images/thumb/Gnome_scarf_detail.png/260px-Gnome_scarf_detail.png?5e19c"}
    ]
}

response = model.invoke([message])
print(response.content)