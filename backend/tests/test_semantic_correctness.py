import os
import sys
import unittest
from unittest.mock import patch


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from generators.custom_generators import generate_question  # noqa: E402
from generators.mcq_generator import _make_distractors  # noqa: E402


class TestSemanticCorrectness(unittest.TestCase):
    def test_four_operations_addition_semantics(self):
        with patch("generators.custom_generators.random.choice", return_value="+"), \
             patch("generators.custom_generators.random.randint", side_effect=[12, 7]):
            q = generate_question("four-operations", "medium")
        self.assertEqual(q["question"], "Calculate: 12 + 7 = ?")
        self.assertEqual(q["answer"], "19")

    def test_mental_arithmetic_compensation_semantics(self):
        with patch("generators.custom_generators.random.choice", side_effect=["compensation", 19]), \
             patch("generators.custom_generators.random.randint", return_value=30):
            q = generate_question("mental-arithmetic", "medium")
        self.assertIn("30 + 19", q["question"])
        self.assertEqual(q["answer"], "49")

    def test_speed_calculation_addition_semantics(self):
        with patch("generators.custom_generators.random.choice", return_value="+"), \
             patch("generators.custom_generators.random.randint", side_effect=[8, 5]):
            q = generate_question("speed-based-calculation", "easy")
        self.assertEqual(q["question"], "Quick! 8 + 5 = ?")
        self.assertEqual(q["answer"], "13")

    def test_english_semantics_deterministic_first_items(self):
        expected_answers = {
            "english-cem": "fast",
            "grammar": "asleep",
            "punctuation": "After lunch, we went to the park and played football.",
            "synonyms": "fast",
            "antonyms": "shrink",
            "comprehension": "She checked the weather first.",
            "creative-writing": "The wind howled as the old gate creaked open.",
            "narrative-writing": "he saw the broken vase on the floor.",
            "non-chronological-report": "What Owls Eat",
        }
        with patch("generators.custom_generators.random.choice", side_effect=lambda seq: seq[0]):
            for module_id, expected in expected_answers.items():
                q = generate_question(module_id, "medium")
                self.assertEqual(q["answer"], expected, msg=f"{module_id} expected {expected} got {q['answer']}")

    def test_non_verbal_semantics_deterministic_first_items(self):
        expected_answers = {
            "non-verbal-reasoning": "Octagon",
            "nvr-cem-pattern-matrices": "Octagon",
            "nvr-cem-rotations-reflections": "Down",
            "nvr-cem-odd-one-out": "Scalene triangle (0 lines of symmetry)",
            "nvr-cem-3d-nets": "Faces that never touch",
        }
        with patch("generators.custom_generators.random.choice", side_effect=lambda seq: seq[0]):
            for module_id, expected in expected_answers.items():
                q = generate_question(module_id, "medium")
                self.assertEqual(q["answer"], expected, msg=f"{module_id} expected {expected} got {q['answer']}")

    def test_computer_semantics_deterministic_first_items(self):
        expected_answers = {
            "intro-it-safety": "Blue!Tiger92",
            "spreadsheets-basics": "=SUM(A1:A5)",
            "scratch-programming": "Loop",
            "block-programming": "To reuse code and reduce repetition",
            "binary-systems": "1010",
            "binary-shifts": "0110",
            "logic-gates": "0",
            "circuit-design": "To reduce complexity and cost",
            "python-basics": "my_score",
            "python-control": "for",
            "python-functions": "Sends value back to caller",
            "python-data-structures": "Dictionary",
            "computer-architecture": "Fetch-Decode-Execute",
            "memory-storage": "SSD",
            "data-representation": "More pixels",
            "input-output": "Keyboard",
            "db-basics": "Primary key",
            "db-sql-queries": "SELECT",
            "os-basics": "Manage hardware and software resources",
            "network-basics": "Local Area Network",
            "internet-protocols": "Translate domain names to IP addresses",
            "web-basics": "Secure communication",
            "ds-arrays-lists": "0",
            "ds-stack-queue": "LIFO",
            "algo-searching": "Sorted",
            "algo-sorting": "Adjacent items are compared and swapped if needed",
        }
        with patch("generators.custom_generators.random.choice", side_effect=lambda seq: seq[0]):
            for module_id, expected in expected_answers.items():
                q = generate_question(module_id, "medium")
                self.assertEqual(q["answer"], expected, msg=f"{module_id} expected {expected} got {q['answer']}")

    def test_volume_distractors_keep_units(self):
        distractors = _make_distractors("64 cm³", "volumes")
        self.assertEqual(len(distractors), 3)
        for d in distractors:
            self.assertTrue(d.endswith("cm³"), msg=f"Expected unit suffix in distractor: {d}")


if __name__ == "__main__":
    unittest.main()
