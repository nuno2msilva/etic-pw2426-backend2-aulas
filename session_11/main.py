from __future__ import annotations

import strawberry
from fastapi import FastAPI
from graphql import GraphQLError
from strawberry.asgi import GraphQL

# ---------------------------------------------------------------------------
# In-memory data store
# ---------------------------------------------------------------------------

_users: dict[int, dict] = {
    1: {"id": 1, "name": "Alice"},
    2: {"id": 2, "name": "Bob"},
}

_posts: dict[int, list[dict]] = {
    1: [{"id": 10, "title": "Alice's first post"}],
    2: [{"id": 20, "title": "Bob's article"}],
}

# ---------------------------------------------------------------------------
# Schema types
# ---------------------------------------------------------------------------

@strawberry.type
class Post:
    id: int
    title: str


@strawberry.type
class User:
    id: int
    name: str


@strawberry.type
class UserWithPosts:
    id: int
    name: str
    posts: list[Post]


# ---------------------------------------------------------------------------
# Tutorial: queries
# ---------------------------------------------------------------------------

@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: int) -> User | None:
        return User(**_users[id]) if id in _users else None

    # Problem: list all users
    @strawberry.field
    def users(self) -> list[User]:
        return [User(**u) for u in _users.values()]

    # Challenge: nested query with auth guard
    @strawberry.field
    def user_with_posts(self, id: int, token: str) -> UserWithPosts | None:
        if token != "valid-token":   # replace with real JWT check in production
            raise GraphQLError("Unauthorized")
        if id not in _users:
            return None
        return UserWithPosts(**_users[id], posts=[Post(**p) for p in _posts.get(id, [])])


# ---------------------------------------------------------------------------
# Problem: mutation
# ---------------------------------------------------------------------------

@strawberry.type
class Mutation:
    @strawberry.mutation
    def update_user_name(self, id: int, new_name: str) -> User | None:
        if id not in _users:
            return None
        _users[id]["name"] = new_name
        return User(**_users[id])


schema = strawberry.Schema(query=Query, mutation=Mutation)
app = FastAPI()
app.add_route("/graphql", GraphQL(schema))   # GraphiQL UI at /graphql


# ---------------------------------------------------------------------------
# Standalone demo — execute queries directly against the schema
# ---------------------------------------------------------------------------

def main():
    import logging
    # strawberry logs every resolver exception to stderr even when handled — silence it for the demo
    logging.getLogger("strawberry.execution").setLevel(logging.CRITICAL)

    print("Tutorial — query user(id: 1):")
    result = schema.execute_sync("{ user(id: 1) { id name } }")
    print(" ", result.data)

    print("\nProblem — query all users:")
    result = schema.execute_sync("{ users { id name } }")
    print(" ", result.data)

    print("\nProblem — mutation updateUserName(id: 2, newName: 'Charlie'):")
    result = schema.execute_sync('mutation { updateUserName(id: 2, newName: "Charlie") { id name } }')
    print(" ", result.data)

    print("\nChallenge — userWithPosts(id: 1, token: 'valid-token'):")
    result = schema.execute_sync('{ userWithPosts(id: 1, token: "valid-token") { id name posts { title } } }')
    print(" ", result.data)

    print("\nChallenge — userWithPosts with bad token:")
    result = schema.execute_sync('{ userWithPosts(id: 1, token: "wrong") { id name } }')
    print("  errors:", [e.message for e in result.errors])

    print("\nFull GraphQL server: uv run uvicorn main:app --reload")
    print("  then open http://localhost:8000/graphql for GraphiQL")


if __name__ == "__main__":
    main()
