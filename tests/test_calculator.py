import unittest

from calculator import add


class TestCalculator(unittest.TestCase):
    def test_add_ints(self):
        self.assertEqual(add(1, 2), 3)

    def test_add_floats(self):
        self.assertAlmostEqual(add(1.5, 2.25), 3.75)


if __name__ == "__main__":
    unittest.main()
