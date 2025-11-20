from src.chatbot.chatbot import Chatbot


def main():
    bot = Chatbot()
    print("Simple example: type a message (or 'exit')")
    while True:
        msg = input("You: ")
        if msg.strip().lower() in ("exit", "quit"):
            break
        reply = bot.chat_once(msg)
        print("Bot:", reply)


if __name__ == "__main__":
    main()
