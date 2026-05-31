## Session 14: Introduction to AI Agents in Python with CrewAI

**Goal:**
Learn the basics of building AI agents using the CrewAI framework to automate tasks and respond intelligently.

**Definition:**
AI agents are autonomous software components that perform tasks based on user input or environmental data. CrewAI simplifies the creation of such agents by providing pre-built modules for conversation, decision-making, and integration with external services. Use cases include chatbots, automated customer support, and data analysis assistants.

**Documentation Reference:**

- https://crew.ai/docs
- https://github.com/crew-ai/crewai-python
- https://en.wikipedia.org/wiki/Intelligent_agent

**Setup:**
```bash
# Run standalone (no packages required — uses built-in Agent class):
uv run python main.py

# Install CrewAI to use the real framework:
uv add crewai
```

**Tutorial:**
- Step-by-Step Example:
    - Create a simple AI agent that responds to a fixed query.
```py
    # Example pseudocode using CrewAI
    from crewai import Agent

    agent = Agent(name="SimpleAgent")
    response = agent.respond("Hello")
    print(response)
```
- Explanation: This example demonstrates initializing an agent and obtaining a response.

### Exercise:

- Problem: Build a simple AI agent that returns a predefined message when given a specific input.
    - Steps to Solve:
        - Initialise the agent.
        - Define a response logic for a specific query.

### Challenge:

- Problem: Enhance the agent to handle multiple queries with different responses based on keywords.
    - Hint: Use conditional statements or a mapping dictionary.
