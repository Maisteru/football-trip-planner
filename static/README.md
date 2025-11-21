# Static

This folder contains static assets (CSS, JavaScript) for the Football Trip Planner web application.

## Overview

The static folder is organized into subdirectories for different asset types and serves client-side resources that enhance the user interface and provide dynamic functionality.

## CSS (`css/style.css`)

Custom stylesheet that extends Bootstrap 5 with application-specific styling.

**Key Styles:**

### Global Styles
- **Body**: Purple gradient background (#667eea to #764ba2), minimum viewport height
- **Container**: Max-width of 900px for optimal readability
- **H1**: White color with text shadow for contrast against gradient

### Component Styles
- **Cards**: 15px border radius, no border for modern look
- **Primary Buttons**: 
  - Gradient background matching body theme
  - Bold font weight
  - Hover effect with upward translation and shadow
  
### Interactive Elements
- **Match Cards** (`#matchesSection .card`):
  - Smooth transform transition (0.2s)
  - Hover effect: lifts up 5px with enhanced shadow
  
### Typography
- **Total Cost Row** (`.table-success`): Enlarged font (1.2em) for emphasis

**Design Philosophy:**
- Consistent purple gradient theme throughout
- Smooth transitions and hover effects
- Card-based layouts with rounded corners
- Enhanced shadows for depth

## JavaScript (`js/main.js`)

Client-side application logic for dynamic content loading and user interactions.
