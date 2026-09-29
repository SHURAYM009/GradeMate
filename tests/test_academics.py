import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from main import grade


class GradeTests(unittest.TestCase):
    def test_grade_boundaries(self):
        self.assertEqual(grade(90), "A")
        self.assertEqual(grade(80), "B")
        self.assertEqual(grade(70), "C")
        self.assertEqual(grade(60), "D")
        self.assertEqual(grade(50), "E")
        self.assertEqual(grade(49.99), "F")


if __name__ == "__main__":
    unittest.main()
