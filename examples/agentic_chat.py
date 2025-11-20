from src.chatbot.chatbot import Chatbot
from src.chatbot.agent import Agent


def fake_search_tool(query: str) -> str:
    return f"[search results for '{query}']: example result"


def main():
    agent = Agent(tools={"search": fake_search_tool})
    bot = Chatbot(agent=agent)
    print("Agentic chat example (use 'search: your query' to invoke tool)")
    while True:
        msg = input("You: ")
        if msg.strip().lower() in ("exit", "quit"):
            break
        reply = bot.chat_once(msg)
        print("Bot:", reply)


if __name__ == "__main__":
    main()
