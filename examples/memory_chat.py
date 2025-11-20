from src.chatbot.chatbot import Chatbot


def main():
    bot = Chatbot()
    print("Memory chat example: conversation will include rolling memory.")
    for _ in range(3):
        msg = input("You: ")
        if msg.strip().lower() in ("exit", "quit"):
            break
        reply = bot.chat_once(msg)
        print("Bot:", reply)
    print("Conversation history:", bot.memory.get())


if __name__ == "__main__":
    main()
