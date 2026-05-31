# Session 14: Introduction to AI Agents
# Standalone classes illustrate agent concepts without any packages.
# Interactive mode is a real generative chatbot (ollama + qwen2.5:1.5b).

import urllib.request

# ---------------------------------------------------------------------------
# Tutorial: simple Agent (mirrors CrewAI's Agent interface)
# ---------------------------------------------------------------------------

class Agent:
    """Minimal agent that echoes a fixed response."""

    def __init__(self, name: str):
        self.name = name

    def respond(self, query: str) -> str:
        return f"Hello! I am {self.name}. You asked: '{query}'"


# ---------------------------------------------------------------------------
# Problem: agent with predefined response for a specific trigger
# ---------------------------------------------------------------------------

class GreetingAgent(Agent):
    """Returns a fixed greeting when the trigger phrase is matched."""

    TRIGGER = "hello"
    FIXED_REPLY = "Hi there! How can I help you today?"

    def respond(self, query: str) -> str:
        if query.strip().lower() == self.TRIGGER:
            return self.FIXED_REPLY
        return super().respond(query)


# ---------------------------------------------------------------------------
# Challenge: keyword-routing agent
# ---------------------------------------------------------------------------

class KeywordAgent(Agent):
    """Maps keywords to canned responses; falls back to a default reply."""

    def __init__(self, name: str, responses: dict[str, str], default: str = "I don't understand."):
        super().__init__(name)
        self._responses = {k.lower(): v for k, v in responses.items()}
        self._default = default

    def respond(self, query: str) -> str:
        lower = query.lower()
        for keyword, reply in self._responses.items():
            if keyword in lower:
                return reply
        return self._default


_SUPPORT_BOT = KeywordAgent(
    name="SupportBot",
    responses={
        "price":   "Our pricing starts at €9.99/month.",
        "refund":  "Refunds are processed within 5 business days.",
        "contact": "Email us at support@example.com.",
        "hello":   "Hi there! How can I help you today?",
    },
    default="I'm not sure — try asking about price, refund, or contact.",
)

# ---------------------------------------------------------------------------
# Generative chatbot config
# ---------------------------------------------------------------------------

_MODEL = "qwen2.5:1.5b"
_SYSTEM = (
    "You are SupportBot, a concise and friendly customer support assistant. "
    "Key facts: pricing starts at €9.99/month, refunds take 5 business days, "
    "contact is support@example.com. "
    "Keep replies short — two or three sentences at most."
)


def _ollama_running() -> bool:
    try:
        urllib.request.urlopen("http://localhost:11434", timeout=2)
        return True
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Interactive REPL
# ---------------------------------------------------------------------------

def interactive():
    print("\n" + "─" * 52)

    try:
        import ollama
        has_ollama = True
    except ImportError:
        has_ollama = False

    use_llm = has_ollama and _ollama_running()

    if use_llm:
        print(f"Chatbot — {_MODEL} via Ollama  (streaming)")
    else:
        if not has_ollama:
            print("Chatbot — keyword fallback  (run 'uv sync' to install ollama)")
        else:
            print("Chatbot — keyword fallback  (Ollama not running at :11434)")
        print("See root README for Ollama setup instructions.")

    print("Type 'quit' to exit.\n")

    messages = [{"role": "system", "content": _SYSTEM}]

    while True:
        try:
            query = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not query:
            continue
        if query.lower() in ("quit", "exit", "q", "bye"):
            print("Goodbye!")
            break

        if use_llm:
            messages.append({"role": "user", "content": query})
            print("Bot: ", end="", flush=True)
            reply_parts: list[str] = []
            for chunk in ollama.chat(model=_MODEL, messages=messages, stream=True):
                piece = chunk["message"]["content"]
                print(piece, end="", flush=True)
                reply_parts.append(piece)
            print("\n")
            messages.append({"role": "assistant", "content": "".join(reply_parts)})
        else:
            print(f"Bot: {_SUPPORT_BOT.respond(query)}\n")


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main():
    print("Tutorial — basic Agent:")
    agent = Agent(name="SimpleAgent")
    print(" ", agent.respond("Hello"))

    print("\nProblem — GreetingAgent:")
    greeter = GreetingAgent(name="Greeter")
    print(" ", greeter.respond("hello"))
    print(" ", greeter.respond("goodbye"))

    print("\nChallenge — KeywordAgent (SupportBot):")
    for q in ["What is the price?", "I need a refund", "How do I contact support?", "Tell me about yourself"]:
        print(f"  Q: {q!r}")
        print(f"  A: {_SUPPORT_BOT.respond(q)}")

    interactive()


if __name__ == "__main__":
    main()
