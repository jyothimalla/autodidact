import os
import sys
import unittest
from unittest.mock import patch


# Ensure local backend package imports resolve when running from repo root.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from generators.custom_generators import MODULE_GENERATORS  # noqa: E402
from generators.mcq_generator import generate_questions_for_module  # noqa: E402


COMPUTER_SUBTOPICS = [
    "intro-it-safety",
    "spreadsheets-basics",
    "scratch-programming",
    "block-programming",
    "binary-systems",
    "binary-shifts",
    "logic-gates",
    "circuit-design",
    "python-basics",
    "python-control",
    "python-functions",
    "python-data-structures",
    "computer-architecture",
    "memory-storage",
    "data-representation",
    "input-output",
    "db-basics",
    "db-sql-queries",
    "os-basics",
    "network-basics",
    "internet-protocols",
    "web-basics",
    "ds-arrays-lists",
    "ds-stack-queue",
    "algo-searching",
    "algo-sorting",
]


class TestComputerGenerators(unittest.TestCase):
    def test_computer_subtopic_generators_are_registered(self):
        missing = [m for m in COMPUTER_SUBTOPICS if m not in MODULE_GENERATORS]
        self.assertFalse(missing, f"Missing generator mappings for: {missing}")

    def test_computer_subtopic_mcq_shape_and_correctness(self):
        for module_id in COMPUTER_SUBTOPICS:
            questions = generate_questions_for_module(
                module_id=module_id,
                num_questions=5,
                difficulty="mixed",
            )
            self.assertEqual(len(questions), 5)

            for idx, q in enumerate(questions, start=1):
                self.assertEqual(q["module_id"], module_id)
                self.assertEqual(q["question_number"], idx)
                self.assertEqual(q["question_id"], f"q{idx}")
                self.assertTrue(isinstance(q["question"], str) and q["question"].strip())

                options = q["options"]
                self.assertEqual(set(options.keys()), {"A", "B", "C", "D"})
                for label in ("A", "B", "C", "D"):
                    self.assertTrue(isinstance(options[label], str) and options[label].strip())

                self.assertIn(q["correct_option"], {"A", "B", "C", "D"})
                selected_value = options[q["correct_option"]].strip()
                self.assertEqual(selected_value, str(q["correct_answer"]).strip())
                self.assertTrue(isinstance(q["explanation"], str) and q["explanation"].strip())

    def test_computer_subtopic_single_difficulty_modes(self):
        for module_id in COMPUTER_SUBTOPICS:
            for difficulty in ("easy", "medium", "hard"):
                questions = generate_questions_for_module(
                    module_id=module_id,
                    num_questions=2,
                    difficulty=difficulty,
                )
                self.assertEqual(len(questions), 2)

    def test_generate_questions_retries_to_avoid_duplicates(self):
        def _fake_mcq(question_text: str) -> dict:
            return {
                "module_id": "python-functions",
                "question": question_text,
                "options": {
                    "A": "Option A",
                    "B": "Option B",
                    "C": "Option C",
                    "D": "Option D",
                },
                "correct_option": "A",
                "correct_answer": "Option A",
                "explanation": "Test explanation",
            }

        side_effect = [
            _fake_mcq("Why use functions?"),
            _fake_mcq("Why use functions?"),  # duplicate candidate for Q2, should be retried
            _fake_mcq("What does a loop do?"),
        ]

        with patch("generators.mcq_generator.random.choice", return_value="medium"), \
             patch("generators.mcq_generator.generate_mcq", side_effect=side_effect) as gen_mock:
            questions = generate_questions_for_module(
                module_id="python-functions",
                num_questions=2,
                difficulty="mixed",
            )

        self.assertEqual(len(questions), 2)
        self.assertEqual(questions[0]["question"], "Why use functions?")
        self.assertEqual(questions[1]["question"], "What does a loop do?")
        self.assertNotEqual(questions[0]["question"], questions[1]["question"])
        self.assertEqual(gen_mock.call_count, 3)


if __name__ == "__main__":
    unittest.main()
