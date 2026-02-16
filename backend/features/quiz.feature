Feature: Quiz question generation

    Scenario: User fetches FMC questions
        Given the quiz API is running
        When the user requests 40 FMC questions
        Then they should receive exactly 40 questions
