## Session 9: Advanced Testing Strategies in Django using pytest

**Goal:**
Explore comprehensive testing techniques in Django projects using pytest to ensure robust web application functionality.

**Definition:**
Advanced testing in Django involves creating tests for models, views, and API endpoints using pytest-django. This approach leverages fixtures, parametrization, and a dedicated test database. It is essential for verifying that all components of a Django application work together as expected, from data models to user interfaces.

**Documentation Reference:**

- https://pytest-django.readthedocs.io/en/latest/
- https://docs.djangoproject.com/en/5.0/topics/testing/overview/
- https://realpython.com/django-testing-guide/

**Setup:**
```bash
uv sync
```

**Project structure:**
```
session_09/
├── myproject/       # Django project settings
│   ├── settings.py
│   └── urls.py
├── myapp/           # Django application
│   ├── models.py    # Item and BlogPost models
│   └── views.py
├── tests/
│   └── test_models.py
├── conftest.py      # pytest-django configuration
└── manage.py
```

**Tutorial:**
- Run the standalone simulation (no Django install needed):
```bash
uv run python main.py
```
- Run the real Django test suite:
```bash
uv run pytest tests/
```
- Apply database migrations and start the dev server:
```bash
uv run python manage.py migrate
uv run python manage.py runserver
```
- Step-by-Step Example:
    - Create a simple Django model.
```py
# myapp/models.py
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField()
```
- Write a test to check model creation.
```py
    # tests/test_models.py
    import pytest
    from myapp.models import Item

    @pytest.mark.django_db
    def test_item_creation():
        item = Item.objects.create(name="Test", value=10)
        assert item.name == "Test"
        assert item.value == 10
```
- Explanation: The test uses the Django test database to create and verify an Item instance.

### Exercise:

- Problem: Create a Django model for a BlogPost and write pytest tests to verify its methods.
    - Steps to Solve:
        - Define the BlogPost model with title, content, and published date.
        - Write tests for creating and retrieving BlogPosts.

### Challenge:

- Problem: Develop a full test suite for a Django REST API endpoint (e.g., listing BlogPosts) using pytest fixtures and parametrization.
    - Hint: Create fixtures for BlogPost objects and test the API response structure.
