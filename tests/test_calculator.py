import unittest
from services.calculator import CostCalculator


class TestCostCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = CostCalculator()
    
    def test_estimate_ticket_price_top_team(self):
        price = self.calculator.estimate_ticket_price('Premier League', 'Manchester City', 'Brighton')
        self.assertEqual(price, 80)
    
    def test_estimate_ticket_price_mid_team(self):
        price = self.calculator.estimate_ticket_price('Premier League', 'Brighton', 'Wolves')
        self.assertEqual(price, 60)
    
    def test_estimate_ticket_price_unknown_league(self):
        price = self.calculator.estimate_ticket_price('Unknown League', 'Team A', 'Team B')
        self.assertEqual(price, 50)
    
    def test_estimate_ticket_price_away_top_team(self):
        price = self.calculator.estimate_ticket_price('La Liga', 'Valencia', 'Barcelona')
        self.assertEqual(price, 70)
    
    def test_calculate_total(self):
        total = self.calculator.calculate_total(200, 150, 80)
        self.assertEqual(total, 430)
    
    def test_calculate_total_zero(self):
        total = self.calculator.calculate_total(0, 0, 0)
        self.assertEqual(total, 0)


if __name__ == '__main__':
    unittest.main()