# Session 15: Advanced AI Agents
# Standalone classes illustrate state, weather, and routing — no packages needed.
# Interactive mode is a generative chatbot with memory and a weather tool.

import json
import re
import urllib.parse
import urllib.request
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Tutorial: StatefulAgent
# ---------------------------------------------------------------------------

class StatefulAgent:
    """Keeps a history of all queries and can replay them on demand."""

    def __init__(self, name: str):
        self.name = name
        self.history: list[str] = []

    def respond(self, query: str) -> str:
        self.history.append(query)
        if query.lower() == "history":
            return f"Your queries: {', '.join(self.history)}"
        return f"Echo: {query}"


# ---------------------------------------------------------------------------
# Shared weather helper
# ---------------------------------------------------------------------------

def fetch_weather(city: str) -> str:
    url = f"https://wttr.in/{urllib.parse.quote(city)}?format=j1"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read())
        temp_c = data["current_condition"][0]["temp_C"]
        feels = data["current_condition"][0]["FeelsLikeC"]
        desc  = data["current_condition"][0]["weatherDesc"][0]["value"]
        return f"{city}: {temp_c}°C (feels like {feels}°C), {desc}"
    except Exception as exc:
        return f"Could not fetch weather for {city}: {exc}"


# ---------------------------------------------------------------------------
# Problem: WeatherAgent
# ---------------------------------------------------------------------------

class WeatherAgent(StatefulAgent):
    def respond(self, query: str) -> str:
        self.history.append(query)
        if query.lower().startswith("weather "):
            return fetch_weather(query[8:].strip())
        return super().respond(query)


# ---------------------------------------------------------------------------
# Challenge: SmartAgent — routes by prefix
# ---------------------------------------------------------------------------

class SmartAgent(WeatherAgent):
    def respond(self, query: str) -> str:
        self.history.append(query)
        lower = query.lower()
        if lower.startswith("weather "):
            return fetch_weather(query[8:].strip())
        if lower.startswith("time"):
            return f"Current UTC time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}"
        if lower == "history":
            return f"Queries so far: {', '.join(self.history)}"
        return f"[{self.name}] I don't know how to handle: '{query}'"


# ---------------------------------------------------------------------------
# Generative chatbot config
# ---------------------------------------------------------------------------

_MODEL = "qwen2.5:1.5b"
_SYSTEM = (
    "You are SmartBot, a helpful and concise assistant. "
    "You have access to real-time weather data and the current time — "
    "when relevant information is provided in the conversation, use it naturally in your reply. "
    "Keep answers brief."
)


def _ollama_running() -> bool:
    try:
        urllib.request.urlopen("http://localhost:11434", timeout=2)
        return True
    except Exception:
        return False


def _extract_city(text: str) -> str | None:
    """Pull a city name from a weather question, e.g. 'weather in Lisbon' → 'Lisbon'."""
    m = re.search(r"weather\s+(?:in\s+|for\s+)?([a-zA-Z\s\-]+)", text, re.IGNORECASE)
    if m:
        return m.group(1).strip().title()
    return None


def _tool_context(query: str) -> str:
    """Return pre-fetched data strings to inject before the user's message."""
    parts: list[str] = []
    city = _extract_city(query)
    if city:
        parts.append(f"[weather data] {fetch_weather(city)}")
    if re.search(r"\btime\b", query, re.IGNORECASE):
        parts.append(f"[current time] {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Interactive REPL
# ---------------------------------------------------------------------------

def interactive():
    print("\n" + "─" * 56)

    try:
        import ollama
        has_ollama = True
    except ImportError:
        has_ollama = False

    use_llm = has_ollama and _ollama_running()

    if use_llm:
        print(f"SmartBot — {_MODEL} via Ollama  (streaming, memory + weather tool)")
        print("Try: 'weather Lisbon', 'what time is it now', or anything.")
    else:
        if not has_ollama:
            print("SmartBot — standalone  (run 'uv sync' to install ollama)")
        else:
            print("SmartBot — standalone  (Ollama not running at :11434)")
        print("Try: 'weather <city>', 'time', 'history'")
        print("See root README for Ollama setup instructions.")

    print("Type 'quit' to exit.\n")

    messages = [{"role": "system", "content": _SYSTEM}]
    standalone = SmartAgent("SmartBot")

    while True:
        try:
            query = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not query:
            continue
        if query.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        if use_llm:
            ctx = _tool_context(query)
            # Inject tool data as context before the user message so the model sees it
            user_content = f"{ctx}\n\nUser: {query}" if ctx else query
            messages.append({"role": "user", "content": user_content})
            print("Bot: ", end="", flush=True)
            reply_parts: list[str] = []
            for chunk in ollama.chat(model=_MODEL, messages=messages, stream=True):
                piece = chunk["message"]["content"]
                print(piece, end="", flush=True)
                reply_parts.append(piece)
            print("\n")
            messages.append({"role": "assistant", "content": "".join(reply_parts)})
        else:
            print(f"Bot: {standalone.respond(query)}\n")


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main():
    print("Tutorial — StatefulAgent:")
    a = StatefulAgent("StatefulAgent")
    print(" ", a.respond("query"))
    print(" ", a.respond("history"))

    print("\nProblem — WeatherAgent:")
    w = WeatherAgent("WeatherBot")
    print(" ", w.respond("weather Lisbon"))

    print("\nChallenge — SmartAgent:")
    s = SmartAgent("SmartBot")
    for q in ["weather Porto", "time", "history"]:
        print(f"  Q: {q!r}  →  {s.respond(q)}")

    interactive()


if __name__ == "__main__":
    main()
