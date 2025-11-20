import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from auth.users import User, users_db
from werkzeug.security import check_password_hash


class TestAuth(unittest.TestCase):
    def test_user_exists_in_db(self):
        self.assertIn('admin', users_db)
        self.assertIn('user', users_db)
    
    def test_passwords_are_hashed(self):
        self.assertNotEqual(users_db['admin'], 'admin123')
        self.assertTrue(users_db['admin'].startswith('scrypt:'))
    
    def test_verify_password_correct(self):
        self.assertTrue(User.verify_password('admin', 'admin123'))
        self.assertTrue(User.verify_password('user', 'password123'))
    
    def test_verify_password_incorrect(self):
        self.assertFalse(User.verify_password('admin', 'wrongpassword'))
        self.assertFalse(User.verify_password('user', 'wrong'))
    
    def test_verify_password_nonexistent_user(self):
        self.assertFalse(User.verify_password('nonexistent', 'password'))
    
    def test_get_user_exists(self):
        user = User.get('admin')
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'admin')
        self.assertTrue(user.is_authenticated)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_anonymous)
    
    def test_get_user_not_exists(self):
        user = User.get('nonexistent')
        self.assertIsNone(user)
    
    def test_user_get_id(self):
        user = User('testuser')
        self.assertEqual(user.get_id(), 'testuser')


if __name__ == '__main__':
    unittest.main()