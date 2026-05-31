## Session 13: Python Web Development Best Practices with Django and FastAPI

**Goal:**
Learn how to structure and optimise web applications using Django and FastAPI effectively.

**Definition:**
Web development best practices include clear code organisation, proper error handling, security measures, and performance optimisation. By following framework-specific guidelines and industry standards, you ensure scalable and maintainable code. This session compares Django's monolithic approach with FastAPI's asynchronous design, highlighting key strategies for each.

**Documentation Reference:**

- https://docs.djangoproject.com/en/5.0/
- https://fastapi.tiangolo.com/
- https://realpython.com/django-best-practices/

**Setup:**
```bash
uv sync
```

**Tutorial:**

- Step-by-Step Example:
    - Create a simple Django project and a FastAPI app.
    - Highlight differences in project structure, middleware usage, and error handling.

```py
# Django: views.py example
from django.http import JsonResponse

def index(request):
    return JsonResponse({"message": "Hello from Django"})

    # FastAPI: main.py example
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/")
    async def index():
        return {"message": "Hello from FastAPI"}
```
- Run the FastAPI server:
```bash
uv run uvicorn main:app --reload
```
- Run the standalone demo (stdlib only, no packages needed):
```bash
uv run python main.py
```

### Exercise:

- Problem: Create a minimal Django project and a FastAPI application that serve a simple "Hello World" endpoint following best practices.
    - Steps to Solve:
        - Set up both projects with proper directory structure.
        - Implement and test the endpoints.

### Challenge:

- Problem: Refactor an existing web application to improve error handling, logging, and performance optimisation.
    - Hint: Consider integrating middleware and asynchronous processing where possible.
