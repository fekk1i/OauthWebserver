#Web Shopping App

This project consists of a web shopping app that integrates with the OAuth server for authentication and authorization.

## Prerequisites

- Python 3.x
- pip package manager

## Installation

1. Clone the repository:
git clone https://github.com/fekk1i/Loginwebapp
cd <repository_directory>


2. Install the dependencies for the web app:
cd <directory>
pip install -r requirements.txt

## Usage

1. Start the Web app:
cd <directory>
python app.py


2. Open your web browser and visit `http://localhost:8000` to access the web shopping app.

## Configuration

### OAuth Server Configuration

The OAuth server can be configured by modifying the following variables in `app.py`:

- `app.config['SESSION_COOKIE_SECURE']`: Set to `True` to enable secure session cookies.
- `app.config['SQLALCHEMY_DATABASE_URI']`: Set the URI for the SQLite database file.
- `app.config['SECRET_KEY']`: Set a secure secret key for session management.
- `ALIELFEKKI_CLIENT_ID`: Set the client ID for the web shopping app.
- `ALIELFEKKI_CLIENT_SECRET`: Set the client secret for the web shopping app.
- `ALIELFEKKI_REDIRECT_URI`: Set the redirect URI for the web shopping app.

### Web Shopping App Configuration

The web shopping app can be configured by modifying the following variables in `app.py`:

- `app.secret_key`: Set a secure secret key for session management.
- `ALIELFEKKI_CLIENT_ID`: Set the client ID for the OAuth server.
- `ALIELFEKKI_CLIENT_SECRET`: Set the client secret for the OAuth server.
- `ALIELFEKKI_REDIRECT_URI`: Set the redirect URI for the OAuth server.



