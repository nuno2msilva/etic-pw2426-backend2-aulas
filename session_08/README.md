## Session 8: Introduction to Testing in Python with pytest

**Goal:**
Learn the basics of writing and running tests using pytest to improve code reliability.

**Definition:**
Testing ensures that code behaves as expected. pytest is a powerful testing framework that simplifies writing tests and offers rich features like fixtures and parametrization. It is used for unit testing, integration tests, and continuous integration pipelines to catch errors early in development.

**Documentation Reference:**

- https://docs.pytest.org/en/stable/getting-started.html
- https://realpython.com/pytest-python-testing/
- https://docs.python.org/3/library/unittest.html

**Setup:**
```bash
uv sync
```

**Tutorial:**

- Create a simple function (e.g., addition).
```py
# app.py
def add(a, b):
    return a + b
```
- Write a test for the function.
```py
# test_app.py
from app import add

def test_add():
    assert add(2, 3) == 5
```

- Run tests using:
```bash
uv run pytest
```

### Exercise:

- Problem: Write a Python function that multiplies two numbers and create a corresponding pytest test.

### Challenge:

- Problem: Write tests for a recursive factorial function using pytest parametrization.
    - Hint: Use the @pytest.mark.parametrize decorator.
