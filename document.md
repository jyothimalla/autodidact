# Testing Guide (Backend + Frontend)

This document explains:
- how to run backend and frontend tests
- how to write new backend unit tests for module/question generators
- a quick checklist for future changes

## 1. Run Backend Tests

Use the Python 3.11 backend venv (important for current syntax/features):

```bash
cd /Users/jyothi/projects/autodidact
backend/venv-py311/bin/python -m unittest backend.tests.test_computer_generators backend.tests.test_all_module_generators backend.tests.test_semantic_correctness -v
```

Run only one file:

```bash
backend/venv-py311/bin/python -m unittest backend.tests.test_all_module_generators -v
```

### What success looks like
- each test ends with `... ok`
- final summary ends with `OK`

## 2. Run Frontend Tests

From frontend folder:

```bash
cd /Users/jyothi/projects/autodidact/frontend
npm test -- --watch=false --browsers=ChromeHeadless
```

Alternative (project default):

```bash
npm test
```

## 3. How to Write Backend Generator Tests

Create a new test file in:

`backend/tests/test_<feature_name>.py`

Template:

```python
import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from generators.custom_generators import MODULE_GENERATORS
from generators.mcq_generator import generate_questions_for_module


def assert_valid_mcq(tc, q):
    tc.assertTrue(isinstance(q["question"], str) and q["question"].strip())
    tc.assertEqual(set(q["options"].keys()), {"A", "B", "C", "D"})
    tc.assertIn(q["correct_option"], {"A", "B", "C", "D"})
    tc.assertEqual(q["options"][q["correct_option"]].strip(), str(q["correct_answer"]).strip())
    tc.assertTrue(isinstance(q["explanation"], str) and q["explanation"].strip())


class TestMyModule(unittest.TestCase):
    def test_registered(self):
        self.assertIn("my-module-id", MODULE_GENERATORS)

    def test_generates_valid_output(self):
        qs = generate_questions_for_module("my-module-id", num_questions=3, difficulty="mixed")
        self.assertEqual(len(qs), 3)
        for i, q in enumerate(qs, start=1):
            self.assertEqual(q["question_number"], i)
            self.assertEqual(q["question_id"], f"q{i}")
            assert_valid_mcq(self, q)

    def test_difficulty_modes(self):
        for d in ("easy", "medium", "hard"):
            qs = generate_questions_for_module("my-module-id", num_questions=2, difficulty=d)
            self.assertEqual(len(qs), 2)
```

Run:

```bash
backend/venv-py311/bin/python -m unittest backend.tests.test_<feature_name> -v
```

## 4. Existing Key Test Files

- `backend/tests/test_computer_generators.py`
- `backend/tests/test_all_module_generators.py`
- `backend/tests/test_semantic_correctness.py`
- `frontend/src/app/components/practice/practice.component.spec.ts`

## 5. Quick Checklist When Adding New Module/Subtopic

1. Add generator mapping in `backend/generators/custom_generators.py`.
2. Add Practice support ID in `frontend/src/app/components/practice/practice.component.ts`.
3. Add/extend test list in backend tests.
4. Run backend tests.
5. Run frontend tests.
6. Fix failures before merging.

## 6. Troubleshooting

### `No module named pytest`
Current backend tests here are written with built-in `unittest`, so use:

```bash
backend/venv-py311/bin/python -m unittest ...
```

### Python version errors (e.g., type syntax issues)
Use Python 3.11 venv command exactly:

```bash
backend/venv-py311/bin/python
```

### Frontend headless browser issues
Try:

```bash
npm test -- --watch=false
```

or install a compatible Chrome/Chromium if needed for `ChromeHeadless`.
