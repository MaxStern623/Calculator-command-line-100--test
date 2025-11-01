import unittest
import sys
from pathlib import Path

# Ensure project root is on sys.path for imports when running tests directly
# `tests` is at <repo>/calculator/tests, so go two levels up to reach repo root
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import calculator.core as core


class TestCoreFunctions(unittest.TestCase):
    def test_add_ints(self):
        self.assertEqual(core.add(2, 3), 5)

    def test_add_floats(self):
        self.assertAlmostEqual(core.add(2.5, 0.5), 3.0)

    def test_subtract(self):
        self.assertEqual(core.subtract(10, 4), 6)
        self.assertEqual(core.subtract(-1, -1), 0)

    def test_multiply(self):
        self.assertEqual(core.multiply(3, 4), 12)
        self.assertEqual(core.multiply(3, 0), 0)

    def test_divide(self):
        self.assertEqual(core.divide(10, 2), 5)
        self.assertAlmostEqual(core.divide(7, 2), 3.5)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            core.divide(1, 0)


if __name__ == "__main__":
    unittest.main()
