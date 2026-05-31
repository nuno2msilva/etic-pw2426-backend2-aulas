# Standalone simulation using dataclasses + unittest.
# For the real Django project run: uv run pytest tests/ -v

import unittest
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional


# ---------------------------------------------------------------------------
# Simulated Django models — see myapp/models.py for the real ORM equivalents
# ---------------------------------------------------------------------------

# Tutorial model (from the README example)
@dataclass
class Item:
    name: str
    value: int
    id: int = 0   # Django auto-assigns; we fake it here


# Exercise model: BlogPost
@dataclass
class BlogPost:
    title: str
    content: str
    published_date: date
    id: int = 0

    def summary(self) -> str:
        """Return the first 100 characters of content."""
        return self.content[:100]

    def is_published(self) -> bool:
        return self.published_date <= date.today()


# Minimal in-memory "database" to simulate Django's ORM
class FakeDB:
    def __init__(self):
        self._store: dict[str, list] = {}
        self._counter: dict[str, int] = {}

    def create(self, model_class, **kwargs):
        name = model_class.__name__
        self._counter[name] = self._counter.get(name, 0) + 1
        obj = model_class(**kwargs, id=self._counter[name])
        self._store.setdefault(name, []).append(obj)
        return obj

    def all(self, model_class):
        return list(self._store.get(model_class.__name__, []))

    def filter(self, model_class, **kwargs):
        return [
            obj for obj in self.all(model_class)
            if all(getattr(obj, k) == v for k, v in kwargs.items())
        ]


db = FakeDB()


# ---------------------------------------------------------------------------
# Tutorial tests — mirrors @pytest.mark.django_db test_item_creation
# ---------------------------------------------------------------------------
class TestItem(unittest.TestCase):
    def setUp(self):
        # fresh db state for each test (Django uses transactions for isolation)
        global db
        db = FakeDB()

    def test_item_creation(self):
        item = db.create(Item, name="Test", value=10)
        self.assertEqual(item.name, "Test")
        self.assertEqual(item.value, 10)


# ---------------------------------------------------------------------------
# Problem: BlogPost model tests
# ---------------------------------------------------------------------------
class TestBlogPost(unittest.TestCase):
    def setUp(self):
        global db
        db = FakeDB()
        self.post = db.create(
            BlogPost,
            title="Hello World",
            content="This is a test post with some content.",
            published_date=date(2024, 1, 1),
        )

    def test_creation(self):
        self.assertEqual(self.post.title, "Hello World")
        self.assertIsNotNone(self.post.id)

    def test_retrieval(self):
        results = db.filter(BlogPost, title="Hello World")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].content, self.post.content)

    def test_summary(self):
        self.assertLessEqual(len(self.post.summary()), 100)

    def test_is_published(self):
        self.assertTrue(self.post.is_published())   # 2024-01-01 is in the past


# ---------------------------------------------------------------------------
# Challenge: full test suite for a "REST API" (simulated list endpoint)
# ---------------------------------------------------------------------------

# Simulated API response — mirrors myapp/views.py blogpost_list()
def list_blog_posts_endpoint() -> dict:
    posts = db.all(BlogPost)
    return {
        "count": len(posts),
        "results": [
            {"id": p.id, "title": p.title, "published_date": str(p.published_date)}
            for p in posts
        ],
    }


class TestBlogPostAPI(unittest.TestCase):
    """Mirrors a pytest fixture + parametrized API test."""

    def setUp(self):
        global db
        db = FakeDB()
        # fixture: pre-populate some posts
        db.create(BlogPost, title="Post A", content="...", published_date=date(2024, 1, 1))
        db.create(BlogPost, title="Post B", content="...", published_date=date(2024, 6, 1))

    def test_list_returns_all_posts(self):
        response = list_blog_posts_endpoint()
        self.assertEqual(response["count"], 2)

    def test_response_structure(self):
        response = list_blog_posts_endpoint()
        for item in response["results"]:
            self.assertIn("id", item)
            self.assertIn("title", item)
            self.assertIn("published_date", item)

    def test_empty_database(self):
        global db
        db = FakeDB()
        response = list_blog_posts_endpoint()
        self.assertEqual(response["count"], 0)
        self.assertEqual(response["results"], [])


def main():
    # Run the unittest suite inline
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for cls in [TestItem, TestBlogPost, TestBlogPostAPI]:
        suite.addTests(loader.loadTestsFromTestCase(cls))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


if __name__ == "__main__":
    main()
