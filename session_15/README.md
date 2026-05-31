## Session 15: Advanced AI Agent Development with CrewAI

**Goal:**
Deepen your knowledge in AI agent development by integrating state management and external API data into CrewAI agents.

**Definition:**
Advanced AI agents not only respond to queries but also maintain context and learn from interactions. Integrating state management and external API calls allows agents to deliver dynamic, personalised responses. Use cases include chatbots that track user history and recommendation engines that adjust responses based on real-time data.

**Documentation Reference:**

- https://crew.ai/docs/advanced
- https://github.com/crew-ai/crewai-python
- https://en.wikipedia.org/wiki/Artificial_intelligence

**Setup:**
```bash
# Run standalone (no packages required — uses built-in StatefulAgent class):
uv run python main.py

# Install CrewAI to use the real framework:
uv add crewai
```

**Tutorial:**
- Step-by-Step Example:
    - Extend the basic agent to store conversation history.
    ```py
    from crewai import Agent

    class StatefulAgent(Agent):
        def __init__(self, name):
            super().__init__(name)
            self.history = []

        def respond(self, query):
            self.history.append(query)
            if query.lower() == "history":
                return f"Your queries: {', '.join(self.history)}"
            return f"Echo: {query}"

    agent = StatefulAgent("StatefulAgent")
    print(agent.respond(query="query"))
    ```
- Explanation: This agent keeps track of previous queries and can respond with the history.

### Exercise

- Problem: Create an AI agent that fetches real-time weather data from an external API and responds with the current temperature.
    - Steps to Solve:
        - Integrate an API call within the agent's response logic.

### Challenge

- Problem: Develop an AI agent that can handle complex queries and respond with relevant information, possibly using external APIs for data enrichment.
    - Hint: Implement a more sophisticated response logic that can parse and respond to structured queries.

---

## Session 16: Building CI/CD Pipelines for Python Projects with GitHub Actions

**Goal:**
Learn how to automate testing, building, and deploying your Python projects using GitHub Actions.

**Definition:**
CI/CD stands for Continuous Integration and Continuous Deployment. It automates testing and deployment so that every code change is verified and delivered seamlessly. In Python projects, CI/CD pipelines help run tests (using pytest), build the application, and deploy to a target environment without manual intervention. This process reduces errors and accelerates development cycles.

**Documentation Reference:**

- https://docs.github.com/en/actions
- https://docs.github.com/en/actions/learn-github-actions/introduction-to-github-actions
- https://docs.pytest.org/en/stable/

**Tutorial:**

- Create Workflow Directory: In your repository, create a folder named .github/workflows.
- Create Workflow File: Add a file named ci.yml with the following content:
```yaml
    name: CI Pipeline
    on: [push, pull_request]
    jobs:
      test:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - name: Install uv
            uses: astral-sh/setup-uv@v4
          - name: Run tests
            run: uv run pytest
```
- Commit and Push: Commit the file and push to GitHub to trigger the workflow. Explanation: This workflow checks out your code, installs uv, and runs tests.

### Exercise:

- Problem: Create a GitHub Actions workflow that tests your project on multiple Python versions.
    - Steps to Solve: Modify the YAML file to include a matrix strategy for Python versions.

### Challenge:

- Problem: Extend the CI/CD pipeline to include a deployment step that runs only when code is pushed to the main branch.
    - Hint: Use conditional steps and job dependencies.
