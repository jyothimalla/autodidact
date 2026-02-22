import os
import sys
import unittest


# Ensure local backend package imports resolve when running from repo root.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from generators.custom_generators import MODULE_GENERATORS  # noqa: E402
from generators.mcq_generator import generate_exam, generate_questions_for_module  # noqa: E402


def _assert_valid_question(test_case: unittest.TestCase, q: dict, expected_module_id: str | None = None):
    if expected_module_id is not None:
        test_case.assertEqual(q["module_id"], expected_module_id)
    test_case.assertTrue(isinstance(q["question"], str) and q["question"].strip())

    options = q["options"]
    test_case.assertEqual(set(options.keys()), {"A", "B", "C", "D"})
    for label in ("A", "B", "C", "D"):
        test_case.assertTrue(isinstance(options[label], str) and options[label].strip())

    test_case.assertIn(q["correct_option"], {"A", "B", "C", "D"})
    selected_value = options[q["correct_option"]].strip()
    test_case.assertEqual(selected_value, str(q["correct_answer"]).strip())
    test_case.assertTrue(isinstance(q["explanation"], str) and q["explanation"].strip())


class TestAllModuleGenerators(unittest.TestCase):
    def test_all_registered_modules_generate_valid_mcqs(self):
        module_ids = sorted(MODULE_GENERATORS.keys())
        self.assertTrue(module_ids, "MODULE_GENERATORS is empty")

        for module_id in module_ids:
            questions = generate_questions_for_module(
                module_id=module_id,
                num_questions=3,
                difficulty="mixed",
            )
            self.assertEqual(len(questions), 3)

            for idx, q in enumerate(questions, start=1):
                self.assertEqual(q["question_number"], idx)
                self.assertEqual(q["question_id"], f"q{idx}")
                _assert_valid_question(self, q, expected_module_id=module_id)

    def test_all_registered_modules_support_easy_medium_hard(self):
        for module_id in sorted(MODULE_GENERATORS.keys()):
            for difficulty in ("easy", "medium", "hard"):
                questions = generate_questions_for_module(
                    module_id=module_id,
                    num_questions=2,
                    difficulty=difficulty,
                )
                self.assertEqual(len(questions), 2)
                for q in questions:
                    _assert_valid_question(self, q, expected_module_id=module_id)

    def test_exam_generation_styles(self):
        # Standard style
        standard = generate_exam(num_questions=20, difficulty="mixed", exam_style="standard")
        self.assertEqual(len(standard), 20)
        for idx, q in enumerate(standard, start=1):
            self.assertEqual(q["question_number"], idx)
            self.assertEqual(q["question_id"], f"q{idx}")
            _assert_valid_question(self, q)

        # CEM style
        cem = generate_exam(num_questions=20, difficulty="mixed", exam_style="cem")
        self.assertEqual(len(cem), 20)
        for idx, q in enumerate(cem, start=1):
            self.assertEqual(q["question_number"], idx)
            self.assertEqual(q["question_id"], f"q{idx}")
            self.assertIn("section_name", q)
            self.assertIn("section_minutes", q)
            _assert_valid_question(self, q)

        # English style
        english = generate_exam(num_questions=20, exam_style="english", target_year="year4")
        self.assertEqual(len(english), 20)
        for idx, q in enumerate(english, start=1):
            self.assertEqual(q["question_number"], idx)
            self.assertEqual(q["question_id"], f"q{idx}")
            self.assertIn("section_name", q)
            self.assertIn("section_minutes", q)
            _assert_valid_question(self, q)


if __name__ == "__main__":
    unittest.main()
