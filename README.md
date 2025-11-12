# Cyber Innovation Hub Client Project

## Overview

At Bedtest™, we offer highly customised software solutions for industrial clients. This project covers a user interface for interaction with our client (Cyber Innovation hub) and their cutting edge supercomputer which simulates various attacks both physical and cyber, before demonstrating on real world models what exactly would happen once the attack has taken place. Our solution offers a stylised landing page, login system, booking system and device graphing system, as well as storage of user history and bookings associated with each user.

## Prerequisites

Before running this project, ensure you have the following installed:

- **Python 3.7+** - [Download Python](https://www.python.org/downloads/)
- **Node.js and npm** - [Download Node.js](https://nodejs.org/) (for frontend dependencies)
- **pip** - Python package manager (usually comes with Python)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd cyberinnovationhub_Client_Project
```

### 2. Install Python Dependencies

Create a virtual environment (recommended):

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

Install required Python packages:

```bash
pip install flask flask-cors bcrypt requests
```

Alternatively, if you prefer to install dependencies manually:
- `flask` - Web framework
- `flask-cors` - Cross-Origin Resource Sharing support
- `bcrypt` - Password hashing
- `requests` - HTTP library for API calls

### 3. Install Frontend Dependencies

Install Node.js dependencies:

```bash
npm install
```

This will install:
- `chartjs-adapter-date-fns` - Chart.js date adapter
- `date-fns` - Date utility library

### 4. Database Setup

The project uses SQLite databases that will be created automatically when you first run the application. However, if you need to initialize the database schema manually:

```bash
# The DemoRequests database schema is defined in DemoRequests.sql
# The application will create the necessary tables automatically on first run
```

**Note:** The application requires two SQLite databases:
- `credentialDatabase.db` - Stores user and admin credentials
- `DemoRequests.db` - Stores booking requests

These will be created automatically when the application runs for the first time.

## Running the Project

### Start the Flask Server

Run the main server file:

```bash
python masterServer.py
```

Or:

```bash
python3 masterServer.py
```

The Flask application will start in debug mode and be available at:

**http://localhost:5000**

### Access the Application

Once the server is running, you can access the application in your web browser:

- **Home/Landing Page**: http://localhost:5000/
- **Login Page**: http://localhost:5000/loginPage or http://localhost:5000/yes
- **Catalog Page**: http://localhost:5000/catalog
- **Booking History**: http://localhost:5000/bookingHistory
- **Moderator Page**: http://localhost:5000/moderator

### Development Mode

The application runs in debug mode by default (as configured in `masterServer.py`). This means:
- The server will automatically reload when code changes are detected
- Detailed error messages will be displayed in the browser
- Debug information is printed to the console

To disable debug mode, edit `masterServer.py` and change:
```python
app.run(debug=True)
```
to:
```python
app.run(debug=False)
```

## Project Structure

```
cyberinnovationhub_Client_Project/
├── masterServer.py          # Main Flask application server
├── loginPageFlask.py        # Alternative login server (if needed)
├── moderator_page.py        # Moderator page functionality
├── templates/               # HTML templates
│   ├── index.html
│   ├── Loginpage.html
│   ├── catalog_page.html
│   ├── bookingPageLoad.html
│   ├── historyPage.html
│   ├── moderator_page.html
│   └── ...
├── static/                  # Static assets (CSS, JS, images)
│   ├── assets/
│   ├── *.css
│   └── *.js
├── credentialDatabase.db    # User/admin credentials database
├── DemoRequests.db          # Booking requests database
├── DemoRequests.sql         # Database schema
└── package.json             # Node.js dependencies
```

## API Endpoints

The application provides several API endpoints:

- `GET /` - Landing page
- `GET /loginPage` - Login page
- `POST /backendVerification` - User authentication
- `GET /catalog` - Device catalog page
- `POST /save` - Save booking request
- `GET /moderator` - Moderator dashboard
- `GET /moderator/accept/<bookingID>` - Accept booking request
- `GET /moderator/deny/<bookingID>` - Deny booking request
- `GET /bedtest/<userName>` - User booking page
- `GET /history_page/<username>` - User history page
- `POST /historyPage` - Get device history from external API

## External API

The application integrates with an external API:
- **CSIL API**: `https://csil-api.onrender.com/device/history/{device}`
- API key is configured in the `headers` dictionary in `masterServer.py`

## Troubleshooting

### Port Already in Use

If port 5000 is already in use, you can change the port in `masterServer.py`:

```python
app.run(debug=True, port=5001)  # Use a different port
```

### Database Errors

If you encounter database errors:
- Ensure SQLite is installed (usually comes with Python)
- Check that the application has write permissions in the project directory
- Delete existing database files and let the application recreate them

### Module Not Found Errors

If you get "Module not found" errors:
- Ensure your virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt` (if you create one)
- Check that all required packages are installed

## Goals left to achieve:

