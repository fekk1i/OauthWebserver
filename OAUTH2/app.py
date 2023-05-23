from __future__ import print_function
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import hashlib
import secrets
import json

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this to a secure secret key
db = SQLAlchemy(app)

# Add application context here
app.app_context().push()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    client_id = db.Column(db.String(100), unique=True, nullable=False)
    secret_id = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, username, email, password, client_id, secret_id):
        self.username = username
        self.email = email
        self.password = password
        self.client_id = client_id
        self.secret_id = secret_id

    def check_password(self, password):
        return self.password == hashlib.sha256(password.encode('utf-8')).hexdigest()

def load_user_data():
    try:
        with open('user_data.json', 'r') as file:
            user_data = json.load(file)
    except FileNotFoundError:
        user_data = {}
    return user_data

def save_user_data(user_data):
    with open('user_data.json', 'w') as file:
        json.dump(user_data, file, indent=4)

def generate_access_token(client_id, client_secret):
    # Generate the access token using the client_id and client_secret
    access_token = secrets.token_hex(16)
    
    # Store the access token in the session for later use
    session['access_token'] = access_token

    return access_token

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        # Generate client ID and secret ID
        client_id = secrets.token_urlsafe(16)
        secret_id = secrets.token_urlsafe(32)

        # Create a new user with the form data and generated IDs
        user = User(username=username, email=email, password=hashed_password, client_id=client_id, secret_id=secret_id)
        db.session.add(user)
        db.session.commit()

        # Save user data in JSON file
        user_data = load_user_data()
        user_data[email] = {
            'username': username,
            'password': hashed_password,
            'client_id': client_id,
            'secret_id': secret_id
        }
        save_user_data(user_data)

        return render_template('success.html', client_id=client_id, secret_id=secret_id)

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists and the password is correct
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['client_id'] = user.client_id
            session['secret_id'] = user.secret_id

            # Debugging statements
            print("Session user_id:", session.get('user_id'))
            print("Session client_id:", session.get('client_id'))
            print("Session secret_id:", session.get('secret_id'))

            return redirect(url_for('authorize'))

        return redirect(url_for('error', error='invalid_credentials'))

    return render_template('login.html')


@app.route('/authorize', methods=['GET', 'POST'])
def authorize():
    # Fetch the user ID from the session
    user_id = session.get('user_id')

    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Retrieve the client_id and secret_id from the session
    client_id = session.get('client_id')
    secret_id = session.get('secret_id')

    if request.method == 'POST':
        # Implement your authorization logic here
        # ...

        # Redirect the user to the shopping website
        return redirect('http://localhost:8000/main.html')

    return render_template('authorize.html', client_id=client_id, secret_id=secret_id)


@app.route('/callback', methods=['GET', 'POST'])
def callback():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not authenticated

    if request.method == 'POST':
        # Generate the access token using the client_id and client_secret
        access_token = generate_access_token(session['client_id'], session['secret_id'])
        print("Access Token:", access_token)  # Debugging statement to check if the access token is generated

        # Return the access token
        token_response = {
            'access_token': access_token,
            'token_type': 'bearer',
            'expires_in': 3600
        }
        print("Token Response:", token_response)  # Debugging statement to check the token response
        return redirect('http://localhost:8000/main.html')

    print("Callback route accessed")
    return render_template('callback.html')


@app.route('/success')
def success():
    if 'user_id' in session:
        # Retrieve the user from the database
        user = User.query.get(session['user_id'])
        if user:
            return render_template('success.html', client_id=user.client_id, secret_id=user.secret_id)

    return redirect(url_for('login'))

@app.route('/token', methods=['POST'])
def token():
    if request.method == 'POST':
        # Get the client credentials from the request
        client_id = request.form['client_id']
        client_secret = request.form['client_secret']
        grant_type = request.form['grant_type']
        code = request.form['code']
        redirect_uri = request.form['redirect_uri']

        # Perform the token exchange process
        # ...

        # Return the token response
        token_response = {
            'access_token': 'your-access-token',
            'token_type': 'bearer',
            'expires_in': 3600
        }
        return jsonify(token_response)

    # Handle invalid HTTP method
    return 'Method Not Allowed', 405

@app.route('/error')
def error():
    error_message = request.args.get('error')
    return render_template('error.html', error=error_message)

@app.route('/lookup', methods=['POST'])
def lookup():
    lookup_username = request.form.get('lookup_username')
    lookup_password = request.form.get('lookup_password')

    user_data = load_user_data()
    lookup_result = None

    for email, data in user_data.items():
        if data['username'] == lookup_username and data['password'] == hashlib.sha256(lookup_password.encode('utf-8')).hexdigest():
            lookup_result = {
                'client_id': data['client_id'],
                'secret_id': data['secret_id']
            }
            break

    return render_template('index.html', lookup_result=lookup_result)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
