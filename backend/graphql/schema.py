# backend/graphql/schema.py
import strawberry
from typing import List

@strawberry.type
class Question:
    question: str
    options: List[str]

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello from GraphQL!"

schema = strawberry.Schema(query=Query)