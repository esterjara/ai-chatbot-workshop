try:
    from langchain.agents import initialize_agent, Tool
    from langchain.agents import AgentType
    from langchain.tools import Tool as LC_Tool
    from langchain import LLMChain
    has_langchain = True
except Exception:
    has_langchain = False

from src.chatbot.chatbot import Chatbot
from src.chatbot.langchain_adapter import LocalLLM


def search_tool(query: str) -> str:
    return f"[search] simulated results for: {query}"


def main():
    if not has_langchain:
        print("LangChain is not installed. Install it with `pip install langchain` to run this example.")
        return

    bot = Chatbot()
    llm = LocalLLM(bot)

    # Wrap the python function as a LangChain tool
    tools = [Tool(name="search", func=search_tool, description="Search the web (simulated)")]

    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    print("LangChain agent ready. Ask something or 'exit'.")
    while True:
        q = input("You: ")
        if q.strip().lower() in ("exit", "quit"):
            break
        result = agent.run(q)
        print("Agent:", result)


if __name__ == "__main__":
    main()
