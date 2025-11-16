class CostCalculator:
    def __init__(self):
        self.ticket_prices = {
            'Premier League': {'top': 80, 'mid': 60, 'low': 50},
            'La Liga': {'top': 70, 'mid': 50, 'low': 40},
            'Serie A': {'top': 60, 'mid': 45, 'low': 35},
            'Bundesliga': {'top': 50, 'mid': 40, 'low': 30},
            'Ligue 1': {'top': 55, 'mid': 40, 'low': 30}
        }
        
        self.top_teams = [
            'Manchester City', 'Liverpool', 'Arsenal', 'Chelsea', 'Manchester United',
            'Real Madrid', 'Barcelona', 'Atletico Madrid',
            'Juventus', 'Inter', 'AC Milan',
            'Bayern Munich', 'Borussia Dortmund',
            'PSG', 'Monaco'
        ]
    
    def estimate_ticket_price(self, league, home_team, away_team):
        if league not in self.ticket_prices:
            return 50
        
        prices = self.ticket_prices[league]
        
        if home_team in self.top_teams or away_team in self.top_teams:
            return prices['top']
        else:
            return prices['mid']
    
    def calculate_total(self, flight, hotel, ticket):
        return flight + hotel + ticket