Feature: GraphQL hello query

  Scenario: User sends hello query
    Given the GraphQL API is running
    When the user sends a hello query
    Then the response should be "Hello Jyothi"
