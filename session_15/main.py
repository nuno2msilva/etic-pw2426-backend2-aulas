# Same standalone approach as session 14 — real CrewAI: pip install crewai
# Exercise uses a live weather API (wttr.in — no API key required).
import json
import urllib.request
from datetime import datetime


# ---------------------------------------------------------------------------
# Tutorial: StatefulAgent (mirrors the README example exactly)
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
# Problem: agent that fetches real-time weather from wttr.in (no key needed)
# ---------------------------------------------------------------------------
class WeatherAgent(StatefulAgent):
    """Fetches the current temperature for a city via wttr.in."""

    _API = "https://wttr.in/{city}?format=j1"

    def _fetch_temperature(self, city: str) -> str:
        url = self._API.format(city=urllib.parse.quote(city))
        try:
            with urllib.request.urlopen(url, timeout=5) as resp:
                data = json.loads(resp.read())
            temp_c = data["current_condition"][0]["temp_C"]
            return f"Current temperature in {city}: {temp_c}°C"
        except Exception as exc:
            return f"Could not fetch weather for {city}: {exc}"

    def respond(self, query: str) -> str:
        self.history.append(query)
        if query.lower().startswith("weather "):
            city = query[8:].strip()
            return self._fetch_temperature(city)
        return super().respond(query)


# ---------------------------------------------------------------------------
# Challenge: agent with structured query parsing + external data enrichment
# ---------------------------------------------------------------------------
class SmartAgent(WeatherAgent):
    """
    Parses structured queries of the form:
        weather <city>          → temperature
        time <timezone>         → current UTC offset (stdlib, no network)
        history                 → replay all queries
        <anything else>         → default echo
    """

    def respond(self, query: str) -> str:
        self.history.append(query)
        lower = query.lower()

        if lower.startswith("weather "):
            city = query[8:].strip()
            return self._fetch_temperature(city)

        if lower.startswith("time"):
            now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            return f"Current UTC time: {now}"

        if lower == "history":
            return f"Queries so far: {', '.join(self.history)}"

        return f"[{self.name}] I don't know how to handle: '{query}'"


# urllib.parse is used inside WeatherAgent but imported at module level
import urllib.parse   # noqa: E402  (intentionally placed after class def for clarity)


def main():
    # Tutorial: stateful echo agent
    print("Tutorial — StatefulAgent:")
    agent = StatefulAgent("StatefulAgent")
    print(" ", agent.respond("query"))
    print(" ", agent.respond("history"))

    # Problem: weather agent
    print("\nProblem — WeatherAgent:")
    weather_bot = WeatherAgent("WeatherBot")
    print(" ", weather_bot.respond("weather Lisbon"))

    # Challenge: smart structured-query agent
    print("\nChallenge — SmartAgent:")
    smart = SmartAgent("SmartBot")
    for q in ["weather Porto", "time", "weather Madrid", "history"]:
        print(f"  Q: {q!r}")
        print(f"  A: {smart.respond(q)}")


if __name__ == "__main__":
    main()
