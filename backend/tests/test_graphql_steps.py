from behave import given, when, then
import requests

@given("the GraphQL API is running")
def step_impl(context):
    context.url = "http://localhost:8000/graphql"

@when("the user sends a hello query")
def step_impl(context):
    query = {
        "query": """
            query {
                hello
            }
        """
    }
    context.response = requests.post(context.url, json=query)

@then('the response should be "Hello Jyothi"')
def step_impl(context):
    assert context.response.status_code == 200
    data = context.response.json()
    assert data["data"]["hello"] == "Hello Jyothi"
