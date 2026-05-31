import pytest
from datetime import date

from myapp.models import BlogPost, Item


# ---------------------------------------------------------------------------
# Tutorial: Item model
# ---------------------------------------------------------------------------
@pytest.mark.django_db
def test_item_creation():
    item = Item.objects.create(name="Test", value=10)
    assert item.name == "Test"
    assert item.value == 10


# ---------------------------------------------------------------------------
# Problem: BlogPost model
# ---------------------------------------------------------------------------
@pytest.mark.django_db
def test_blogpost_creation():
    post = BlogPost.objects.create(
        title="Hello World",
        content="This is a test post with some content.",
        published_date=date(2024, 1, 1),
    )
    assert post.title == "Hello World"
    assert post.id is not None


@pytest.mark.django_db
def test_blogpost_retrieval():
    BlogPost.objects.create(
        title="Hello World",
        content="Content here.",
        published_date=date(2024, 1, 1),
    )
    results = BlogPost.objects.filter(title="Hello World")
    assert results.count() == 1


@pytest.mark.django_db
def test_blogpost_summary():
    post = BlogPost.objects.create(
        title="Test",
        content="A" * 200,
        published_date=date(2024, 1, 1),
    )
    assert len(post.summary()) == 100


@pytest.mark.django_db
def test_blogpost_is_published():
    post = BlogPost.objects.create(
        title="Old Post",
        content="Content.",
        published_date=date(2024, 1, 1),
    )
    assert post.is_published() is True


# ---------------------------------------------------------------------------
# Challenge: API endpoint test suite with fixtures and parametrization
# ---------------------------------------------------------------------------
@pytest.fixture
def sample_posts(db):
    BlogPost.objects.create(title="Post A", content="...", published_date=date(2024, 1, 1))
    BlogPost.objects.create(title="Post B", content="...", published_date=date(2024, 6, 1))


@pytest.mark.django_db
def test_list_returns_all_posts(sample_posts):
    assert BlogPost.objects.count() == 2


@pytest.mark.django_db
def test_empty_database():
    assert BlogPost.objects.count() == 0


@pytest.mark.parametrize("title,content,expected_summary_len", [
    ("Short", "Hello", 5),
    ("Long", "X" * 200, 100),
])
@pytest.mark.django_db
def test_summary_parametrized(title, content, expected_summary_len):
    post = BlogPost.objects.create(
        title=title,
        content=content,
        published_date=date(2024, 1, 1),
    )
    assert len(post.summary()) == expected_summary_len
