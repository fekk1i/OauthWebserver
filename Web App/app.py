from flask import Flask, redirect, request, render_template, session, url_for
import requests

app = Flask(__name__)
app.secret_key = '123'  # Set your secret key for session management

ALIELFEKKI_CLIENT_ID = 'HqEvhWblLfwqdFBoyZsxIw'
ALIELFEKKI_CLIENT_SECRET = 'wKlWYeowER7zqw-JYBUZjmiM7tZ9fm_oCZhzZOBX2WY'
ALIELFEKKI_REDIRECT_URI = 'http://localhost:5000/callback'

# Your implementation for alielfekki server endpoints

def get_alielfekki_user_name(access_token):
    # Implement your logic to get the user's name from alielfekki server
    # Replace this with your actual implementation
    # Make sure to return the user's name or None if not available
    pass


@app.route('/')
def index():
    if 'logged_in_user' in session:
        return redirect(url_for('main_html'))
    
    # Generate the authorization URL for alielfekki server
    alielfekki_authorization_url = 'http://localhost:5000/authorize'
    # Replace 'YOUR_AUTHORIZATION_URL' with the actual URL for alielfekki authorization

    return render_template('login.html', alielfekki_authorization_url=alielfekki_authorization_url)


@app.route('/callback')
def callback():
    code = request.args.get('code')

    # Step 2: Exchange the authorization code for an access token
    token_url = 'http://localhost:5000/token'
    # Replace 'YOUR_TOKEN_URL' with the actual URL for your token endpoint

    token_data = {
        'client_id': ALIELFEKKI_CLIENT_ID,
        'client_secret': ALIELFEKKI_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': ALIELFEKKI_REDIRECT_URI,
        'scope': 'identify'  # Update with the actual scope required by your server
    }

    response = requests.post(token_url, data=token_data)
    print("Token Response:", response.json())  # Debugging statement

    token_data = response.json()
    access_token = token_data.get('access_token')

    if access_token:
        # Get the logged-in user's name from alielfekki server
        user_name = get_alielfekki_user_name(access_token)
        print("Logged-in User Name:", user_name)  # Debugging statement

        # Save the user information in session
        session['logged_in_user'] = user_name if user_name else 'Unknown User'
        return redirect(url_for('main_html'))

    return 'Access Token not received'


@app.route('/main')
def main():
    if not session.get('logged_in_user'):
        return redirect(url_for('index'))

    return render_template('main.html')


@app.route('/main.html')
def main_html():
    logged_in_user = session.get('logged_in_user', 'Unknown User')
    return render_template('main.html', logged_in_user=logged_in_user)


@app.route('/about')
def about():
    logged_in_user = session.get('logged_in_user', 'Unknown User')
    return render_template('about.html', logged_in_user=logged_in_user)


@app.route('/contact')
def contact():
    logged_in_user = session.get('logged_in_user', 'Unknown User')
    return render_template('contact.html', logged_in_user=logged_in_user)


@app.route('/logout')
def logout():
    session.pop('logged_in_user', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=8000, debug=True)
