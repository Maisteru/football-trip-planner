from werkzeug.security import generate_password_hash, check_password_hash

users_db = {
    'kris': generate_password_hash('twojastara'),
    'admin': generate_password_hash('admin123'),
    'user': generate_password_hash('password123'),
}

class User:
    def __init__(self, username):
        self.username = username
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
    
    def get_id(self):
        return self.username
    
    @staticmethod
    def get(username):
        if username in users_db:
            return User(username)
        return None
    
    @staticmethod
    def verify_password(username, password):
        if username in users_db:
            return check_password_hash(users_db[username], password)
        return False