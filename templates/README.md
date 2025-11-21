# Templates

This folder contains Jinja2 HTML templates for the Football Trip Planner web application.

## Overview

The templates use Bootstrap 5 for responsive design and styling, with custom CSS and JavaScript for enhanced functionality. All templates follow a consistent design pattern with gradient backgrounds and card-based layouts.

## Templates

### login.html

User authentication page with a centered login form.

**Features:**
- Centered card layout with gradient purple background
- Username and password input fields
- Flash message support for error/success notifications
- Responsive design (max-width: 400px)
- Bootstrap 5 styling with custom CSS

**Form Fields:**
- `username` - Text input (required, autofocus)
- `password` - Password input (required)

**Routes:**
- POST to `{{ url_for('login') }}`

**Flash Messages:**
- Displays categorized alerts (success, danger, warning, info)
- Auto-dismissible with close button

### index.html

Main application page for planning football trips.

**Features:**
- Header with logout button
- Multi-step form for trip planning
- Dynamic match selection
- Cost breakdown display with booking links
- Responsive layout (col-md-8 centered)

**Form Sections:**

1. **Trip Planning Form** (`#tripForm`)
   - `originCity` - User's departure city (text input)
   - `league` - League selection dropdown (dynamically populated)
   - `team` - Team selection dropdown (enabled after league selection)
   - `matchType` - Radio buttons (home/away/all)
   - Submit button to find matches

2. **Matches Section** (`#matchesSection`)
   - Hidden by default
   - Displays list of upcoming matches
   - Populated dynamically via JavaScript

3. **Results Section** (`#resultsSection`)
   - Hidden by default
   - Shows selected match information
   - Cost breakdown table with:
     - ✈️ Flights (Round Trip) with booking link
     - 🏨 Accommodation (2 nights) with booking link
     - 🎫 Match Ticket (estimated)
     - 💰 Total Cost (highlighted in green)

**Routes:**
- GET/POST to main application route
- Logout via `{{ url_for('logout') }}`

**Assets:**
- CSS: `static/css/style.css`
- JavaScript: `static/js/main.js`
- Bootstrap 5.3.0 (CDN)

## Template Engine

All templates use **Jinja2** templating syntax:
- `{{ variable }}` - Variable output
- `{% for %}` - Loops
- `{% if %}` - Conditionals
- `{{ url_for('route') }}` - URL generation
- `{% with messages = get_flashed_messages() %}` - Flash messages

## Styling

**Common Design Elements:**
- Bootstrap 5.3.0 framework
- Gradient backgrounds (purple theme)
- Card-based layouts with shadows
- Responsive grid system
- Custom CSS overrides in `static/css/style.css`

**Color Scheme:**
- Primary: Purple gradient (#667eea to #764ba2)
- Success: Green (for total cost display)
- Buttons: Bootstrap primary/danger/outline variants

## JavaScript Integration

Both templates include Bootstrap's JavaScript bundle for:
- Alert dismissal
- Form validation
- Responsive components

The `index.html` additionally includes `main.js` for:
- Dynamic form population (leagues, teams)
- AJAX requests to backend APIs
- Match selection and display
- Cost calculation and display
- Show/hide sections based on user interaction