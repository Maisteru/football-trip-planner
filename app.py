from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from services.football_api import FootballAPIService
from services.flight_api import FlightAPIService
from services.hotel_api import HotelAPIService
from services.calculator import CostCalculator
from config import Config
from auth.users import User

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
CORS(app, resources={r"/*": {"origins": "*"}})

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

football_service = FootballAPIService(app.config['FOOTBALL_API_KEY'])
flight_service = FlightAPIService(app.config['AMADEUS_API_KEY'], app.config['AMADEUS_API_SECRET'])
hotel_service = HotelAPIService(app.config['BOOKING_API_KEY'])
calculator = CostCalculator()

@login_manager.user_loader
def load_user(username):
    return User.get(username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.verify_password(username, password):
            user = User.get(username)
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/api/leagues', methods=['GET'])
@login_required
def get_leagues():
    leagues = football_service.get_top_leagues()
    return jsonify(leagues)

@app.route('/api/teams/<int:league_id>', methods=['GET'])
@login_required
def get_teams(league_id):
    teams = football_service.get_teams_by_league(league_id)
    return jsonify(teams)

@app.route('/api/matches', methods=['POST'])
@login_required
def get_matches():
    data = request.json
    team_id = data.get('team_id')
    match_type = data.get('match_type')
    matches = football_service.get_upcoming_matches(team_id, match_type)
    return jsonify(matches)

@app.route('/api/calculate-trip', methods=['POST'])
@login_required
def calculate_trip():
    data = request.json
    match_id = data.get('match_id')
    origin_city = data.get('origin_city')
    
    match_details = football_service.get_match_details(match_id)
    
    flight_data = flight_service.get_flight_price(
        origin_city,
        match_details['city'],
        match_details['date']
    )
    
    hotel_data = hotel_service.get_hotel_price(
        match_details['city'],
        match_details['date']
    )
    
    ticket_cost = calculator.estimate_ticket_price(
        match_details['league'],
        match_details['home_team'],
        match_details['away_team']
    )
    
    total_cost = calculator.calculate_total(flight_data['price'], hotel_data['price'], ticket_cost)
    
    return jsonify({
        'match': match_details,
        'costs': {
            'flight': flight_data['price'],
            'hotel': hotel_data['price'],
            'ticket': ticket_cost,
            'total': total_cost
        },
        'links': {
            'flight': flight_data['link'],
            'hotel': hotel_data['link']
        }
    })

if __name__ == '__main__':
    app.run(debug=True)