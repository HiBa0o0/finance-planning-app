import unittest
from src.utils.calculations import calculate_variance, calculate_cumulative_balance

class TestCalculations(unittest.TestCase):

    def test_calculate_variance(self):
        actual = [100, 200, 300]
        expected = [150, 250, 350]
        result = calculate_variance(actual, expected)
        self.assertEqual(result, [50, 50, 50])

    def test_calculate_cumulative_balance(self):
        cash_flows = [1000, -200, -300, 400]
        expected_balance = [1000, 800, 500, 900]
        result = calculate_cumulative_balance(cash_flows)
        self.assertEqual(result, expected_balance)

if __name__ == '__main__':
    unittest.main()