from behave import given, when, then
import requests

@given("the quiz API is running")
def step_impl(context):
    context.base_url = "http://localhost:8000"

@when("the user requests 40 FMC questions")
def step_impl(context):
    try:
        response = requests.get(f"{context.base_url}/fmc/questions?level=0")
        context.response = response
        context.questions = response.json()  # assuming API returns a list directly
    except Exception as e:
        print(f"Error fetching questions: {e}")
        raise

@then("they should receive exactly 40 questions")
def step_impl(context):
    print("Response status:", context.response.status_code)
    print("Response body:", context.response.text)

    assert context.response.status_code == 200
    assert isinstance(context.questions, list), "Response is not a list"
    assert len(context.questions) == 40, f"Expected 40, got {len(context.questions)}"
