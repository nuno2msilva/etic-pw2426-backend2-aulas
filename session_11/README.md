## Session 11: Building GraphQL APIs with Python

**Goal:**
Learn to design and implement a GraphQL API in Python for flexible client data queries.

**Definition:**
GraphQL is a query language that allows clients to request exactly the data they need. In Python, libraries like Strawberry and Graphene simplify building GraphQL APIs. Use cases include mobile and web applications that require efficient and customisable data fetching.

**Documentation Reference:**

- https://graphql.org/learn/
- https://graphene-python.org/
- https://strawberry.rocks/docs/

**Setup:**
```bash
uv sync
```

**Tutorial:**
- Step-by-Step Example:
    - Install Strawberry and FastAPI (handled by `uv sync`).
    - Define types and resolvers.

```py
    import strawberry
    from fastapi import FastAPI
    from strawberry.asgi import GraphQL

    @strawberry.type
    class User:
        id: int
        name: str

    @strawberry.type
    class Query:
        @strawberry.field
        def user(self, id: int) -> User:
            return User(id=id, name="John Doe")

    schema = strawberry.Schema(query=Query)
    graphql_app = GraphQL(schema)

    app = FastAPI()
    app.add_route("/graphql", graphql_app)
```
- Run the full GraphQL server:
```bash
uv run uvicorn main:app --reload
```
- Run the standalone demo (no packages needed):
```bash
uv run python main.py
```
- Explanation: This creates a GraphQL endpoint at /graphql where clients can query for user data.

### Exercise:

Problem: Create a simple GraphQL API that allows querying and updating a user's name.

- Steps to Solve: Extend the schema to include a mutation for updating the user's name.

### Challenge:

Problem: Implement a GraphQL API that supports nested queries and authenticated mutations.
    - Hint: Integrate an authentication check in the resolver.
