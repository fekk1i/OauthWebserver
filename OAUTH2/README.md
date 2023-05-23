# README: Local OAuth Server

## Dependencies
To run the OAuth server, you need to have the following dependencies installed:

- Python 3.x
- Flask
- Flask SQLAlchemy

Install the dependencies using the following command:

pip install -r requirements.txt

## Running the OAuth Server
To run the OAuth server, follow these steps:

1. Clone or download the repository containing the OAuth server code.

2. Open a terminal or command prompt and navigate to the directory where the `app.py` file is located.

3. Run the server by executing the following command:

python app.py

4. The OAuth server should now be running on `http://localhost:5000/`.

## Using the OAuth Server
The OAuth server provides the following endpoints:

- `/`: Displays the home page.
- `/register`: Allows users to register by providing a username, email, and password.
- `/login`: Allows users to authenticate by providing a username and password.
- `/authorize`: Displays the authorization page after successful login.
- `/callback`: Handles the callback after authorization and generates an access token.
- `/success`: Displays the success page after successful authentication.
- `/token`: Handles the token exchange process (currently stubbed out).
- `/error`: Displays an error page with an error message.
- `/lookup`: Allows looking up user credentials by providing a username and password (currently stubbed out).

To use the OAuth server, follow these steps:

1. Open a web browser and navigate to `http://localhost:5000/`.

2. Register a new user by providing a username, email, and password.

3. Login with the registered user's credentials.

4. After successful login, you will be redirected to the authorization page (`/authorize`).

5. Click the "Authorize" button to generate an access token.

6. The access token will be displayed on the callback page (`/callback`).

7. You can simulate the token exchange process by sending a POST request to `/token` with the required parameters (client_id, client_secret, grant_type, code, redirect_uri).

8. Use the generated access token to make authenticated requests to protected resources.
