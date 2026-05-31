# The CrewAI API shown in the README is pseudocode; this file implements
# the same interface as a standalone class so the examples run without
# installing the actual framework.
# To use the real CrewAI: pip install crewai


# ---------------------------------------------------------------------------
# Tutorial: simple Agent (mirrors CrewAI's Agent interface)
# ---------------------------------------------------------------------------
class Agent:
    """Minimal Agent that echoes a fixed response — mirrors the tutorial example."""

    def __init__(self, name: str):
        self.name = name

    def respond(self, query: str) -> str:
        return f"Hello! I am {self.name}. You asked: '{query}'"


# ---------------------------------------------------------------------------
# Problem: agent with predefined response for a specific input
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
# Challenge: agent that handles multiple queries via a keyword→response map
# ---------------------------------------------------------------------------
class KeywordAgent(Agent):
    """Maps keywords to canned responses; falls back to a default reply."""

    def __init__(self, name: str, responses: dict[str, str], default: str = "I don't understand."):
        super().__init__(name)
        # keys are lower-cased for case-insensitive matching
        self._responses = {k.lower(): v for k, v in responses.items()}
        self._default = default

    def respond(self, query: str) -> str:
        # check if any registered keyword appears in the query
        lower_query = query.lower()
        for keyword, reply in self._responses.items():
            if keyword in lower_query:
                return reply
        return self._default


def main():
    # Tutorial: basic agent
    print("Tutorial:")
    agent = Agent(name="SimpleAgent")
    print(" ", agent.respond("Hello"))

    # Problem: predefined response
    print("\nProblem:")
    greeter = GreetingAgent(name="Greeter")
    print(" ", greeter.respond("hello"))        # triggers fixed reply
    print(" ", greeter.respond("goodbye"))      # falls back to echo

    # Challenge: keyword routing
    print("\nChallenge:")
    bot = KeywordAgent(
        name="SupportBot",
        responses={
            "price":   "Our pricing starts at €9.99/month.",
            "refund":  "Refunds are processed within 5 business days.",
            "contact": "Email us at support@example.com.",
        },
        default="I'm not sure — try rephrasing your question.",
    )
    queries = [
        "What is the price?",
        "I need a refund please",
        "How do I contact support?",
        "Tell me about your company",
    ]
    for q in queries:
        print(f"  Q: {q!r}")
        print(f"  A: {bot.respond(q)}")


if __name__ == "__main__":
    main()
