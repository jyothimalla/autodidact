import pytest
from httpx import AsyncClient, ASGITransport
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from graphql_api import app
from routers import fmc_routes

transport = ASGITransport(app=app)



@pytest.mark.asyncio
async def test_hello_graphql():
    query = {
        "query": """
            query {
                hello
            }
        """
    }

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/graphql", json=query)

    assert response.status_code == 200
    assert response.json()["data"]["hello"] == "Hello, Jyothi!"
    
@pytest.mark.asyncio
async def test_get_fmc_questions_graphql():
    query = {
        "query": """
    query {
        get_fmc_questions(level: 0) {
            question
            answer
            explanation
        }
    }
        """
    }

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/graphql", json=query)

    data = response.json()
    assert response.status_code == 200
    assert "data" in data
    assert "getFmcQuestions" in data["data"]
    assert len(data["data"]["getFmcQuestions"]) == 40