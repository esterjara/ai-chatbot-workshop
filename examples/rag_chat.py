from src.chatbot.chatbot import Chatbot
from src.chatbot.rag import SimpleRetriever, RAG


SAMPLE_DOCS = [
    ("doc1", "Python is a programming language that is widely used for AI."),
    ("doc2", "Retrieval-augmented generation (RAG) augments prompts with relevant docs."),
    ("doc3", "Agents can call tools to perform tasks beyond text generation."),
]


def main():
    retriever = SimpleRetriever(SAMPLE_DOCS)
    rag = RAG(retriever)
    bot = Chatbot()
    print("RAG demo. Type a question (or 'exit')")
    while True:
        q = input("You: ")
        if q.strip().lower() in ("exit", "quit"):
            break
        prompt = bot.build_prompt(q)
        augmented = rag.augment(prompt, q)
        # Use model directly for this demo
        if bot.model is None:
            print("Bot:", bot.generate_response(q))
        else:
            try:
                out = bot.model.create(prompt=augmented, max_tokens=256)
                if isinstance(out, dict) and "choices" in out:
                    print("Bot:", out["choices"][0]["text"]) 
                else:
                    print("Bot (raw):", out)
            except Exception:
                print("Bot:", bot.generate_response(q))


if __name__ == "__main__":
    main()
