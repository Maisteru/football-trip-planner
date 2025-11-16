from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from services.football_api import FootballAPIService
from services.flight_api import FlightAPIService
from services.hotel_api import HotelAPIService
from services.calculator import CostCalculator
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

football_service = FootballAPIService(app.config['FOOTBALL_API_KEY'])
flight_service = FlightAPIService(app.config['AMADEUS_API_KEY'], app.config['AMADEUS_API_SECRET'])
hotel_service = HotelAPIService(app.config['BOOKING_API_KEY'])
calculator = CostCalculator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/leagues', methods=['GET'])
def get_leagues():
    leagues = football_service.get_top_leagues()
    return jsonify(leagues)

@app.route('/api/teams/<int:league_id>', methods=['GET'])
def get_teams(league_id):
    teams = football_service.get_teams_by_league(league_id)
    return jsonify(teams)

@app.route('/api/matches', methods=['POST'])
def get_matches():
    data = request.json
    team_id = data.get('team_id')
    match_type = data.get('match_type')
    
    matches = football_service.get_upcoming_matches(team_id, match_type)
    return jsonify(matches)

@app.route('/api/calculate-trip', methods=['POST'])
def calculate_trip():
    data = request.json
    match_id = data.get('match_id')
    origin_city = data.get('origin_city')
    
    match_details = football_service.get_match_details(match_id)
    
    flight_cost = flight_service.get_flight_price(
        origin_city,
        match_details['city'],
        match_details['date']
    )
    
    hotel_cost = hotel_service.get_hotel_price(
        match_details['city'],
        match_details['date']
    )
    
    ticket_cost = calculator.estimate_ticket_price(
        match_details['league'],
        match_details['home_team'],
        match_details['away_team']
    )
    
    total_cost = calculator.calculate_total(flight_cost, hotel_cost, ticket_cost)
    
    return jsonify({
        'match': match_details,
        'costs': {
            'flight': flight_cost,
            'hotel': hotel_cost,
            'ticket': ticket_cost,
            'total': total_cost
        }
    })

if __name__ == '__main__':
    app.run(debug=True)