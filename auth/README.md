# Auth

This folder contains authentication and user management functionality for the Football Trip Planner application.

## Overview

The auth module provides a simple in-memory user authentication system using Flask-Login and Werkzeug's security utilities. It handles user credentials, password hashing, and session management.

## Files

### users.py

Core authentication module containing user database and User class implementation.

## Components

### User Database (`users_db`)

In-memory dictionary storing username-password pairs with hashed passwords.

**Default Users:**
```python
{
    'admin': 'admin123',        # Admin user
    'user': 'password123'       # Test user
}
```

### Security:

- Passwords are hashed using Werkzeug's generate_password_hash()
- Uses PBKDF2 algorithm with salt
- Passwords never stored in plain text