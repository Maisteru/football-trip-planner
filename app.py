from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from services.cached_football_api import CachedFootballAPIService
from services.cached_flight_api import CachedFlightAPIService
from services.cached_hotel_api import CachedHotelAPIService
from services.calculator import CostCalculator
from config import Config
from auth.users import User
from models.cache import db, APICache, RequestLog

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cache.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app, resources={r"/*": {"origins": "*"}})

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

with app.app_context():
    db.create_all()

football_service = CachedFootballAPIService(app.config['FOOTBALL_API_KEY'])
flight_service = CachedFlightAPIService(app.config['AMADEUS_API_KEY'], app.config['AMADEUS_API_SECRET'])
hotel_service = CachedHotelAPIService(app.config['BOOKING_API_KEY'])
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
    RequestLog.log_request('/api/leagues', current_user.username)
    leagues = football_service.get_top_leagues()
    return jsonify(leagues)

@app.route('/api/teams/<int:league_id>', methods=['GET'])
@login_required
def get_teams(league_id):
    cache_key = f"teams_league_{league_id}"
    cache_hit = APICache.get_cached(cache_key) is not None
    RequestLog.log_request(f'/api/teams/{league_id}', current_user.username, cache_hit)
    
    teams = football_service.get_teams_by_league(league_id)
    return jsonify(teams)

@app.route('/api/matches', methods=['POST'])
@login_required
def get_matches():
    data = request.json
    team_id = data.get('team_id')
    match_type = data.get('match_type')
    
    cache_key = f"matches_{team_id}_{match_type}"
    cache_hit = APICache.get_cached(cache_key) is not None
    RequestLog.log_request('/api/matches', current_user.username, cache_hit)
    
    matches = football_service.get_upcoming_matches(team_id, match_type)
    return jsonify(matches)

@app.route('/api/calculate-trip', methods=['POST'])
@login_required
def calculate_trip():
    data = request.json
    match_id = data.get('match_id')
    origin_city = data.get('origin_city')
    
    RequestLog.log_request('/api/calculate-trip', current_user.username)
    
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

@app.route('/api/admin/cache/stats', methods=['GET'])
@login_required
def cache_stats():
    if current_user.username != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    request_stats = RequestLog.get_stats()
    cache_count = APICache.query.count()
    
    return jsonify({
        'cache_entries': cache_count,
        'request_stats': request_stats
    })

@app.route('/api/admin/cache/clear', methods=['POST'])
@login_required
def clear_cache():
    if current_user.username != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    count = APICache.clear_all()
    return jsonify({'message': f'Cleared {count} cache entries'})

@app.route('/api/admin/cache/clear-expired', methods=['POST'])
@login_required
def clear_expired_cache():
    if current_user.username != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    count = APICache.clear_expired()
    return jsonify({'message': f'Cleared {count} expired cache entries'})

if __name__ == '__main__':
    app.run(debug=True)