import flask
from pymongo import MongoClient
import html
import re
import os
import hashlib
import bcrypt
import base64
import secrets
import websockets


app = flask.Flask(__name__)

salt_size = 10

mongo_client = MongoClient('mongo')
db = mongo_client['cse312Team']
user_collection = db["users"]


# HTML
@app.route('/', methods=['GET', 'POST'])
def loginhtml():
    return flask.send_file('../HTML/LoginPage.html')


@app.route('/HTML/RegisterPage.html', methods=['GET', 'POST'])
def registerhtml():
    return flask.send_file('../HTML/RegisterPage.html')


# Javascript
@app.route('/Server/TheGame.js', methods=['GET', 'POST'])
def jsfile():
    return flask.send_file('../Server/TheGame.js')


# CSS
@app.route('/CSS/LoginPage.css', methods=['GET', 'POST'])
def logincss():
    return flask.send_file('../CSS/LoginPage.css')


@app.route('/CSS/RegisterPage.css', methods=['GET', 'POST'])
def registercss():
    return flask.send_file('../CSS/RegisterPage.css')


@app.route('/CSS/LandingPage.css', methods=['GET', 'POST'])
def landingpagecss():
    session_token = flask.request.cookies.get('session_token')
    if session_token:
        user = user_collection.find_one({'session_token': session_token})
        if user:
            template_path = os.path.join('HTML', 'LandingPage.html')
            return flask.render_template(template_path, username=user['username'])
        else:
            # Return error message
            return flask.make_response("Invalid session token", 400)
    else:
        # Return error message
        return flask.make_response("No session token found", 400)


@app.route('/MadeNewAccount', methods=['GET', 'POST'])
def made_new_account():
    if flask.request.method == 'POST':
        entire_data = flask.request.form
        email = entire_data.get('email')
        password = entire_data.get('password')
        username = entire_data.get('username')
        confirmpassword = entire_data.get('confirmpassword')

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return flask.make_response("Invalid email address", 400)

        if password != confirmpassword:
            return flask.make_response("Password and confirm passwords don't match", 400)

        if len(password) < 8:
            return flask.make_response("Password too short. Needs at least 8 characters", 400)

        salt = bcrypt.gensalt()

        password_hash = bcrypt.hashpw(password.encode(), salt)

        store_stuff = {}
        store_stuff['email'] = html.escape(email)
        store_stuff['password'] = [salt , password_hash]
        store_stuff['username'] = html.escape(username)
        store_stuff['wins'] = 0

        user_collection.insert_one(store_stuff)

    return flask.send_file('../HTML/LoginPage.html')


@app.route('/LoggedIn', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        entire_data = flask.request.form

        email = entire_data.get('email')
        password = entire_data.get('password')

        data = user_collection.find({})
        for item in data:
            print(item)
            if item['email'] == email:

                passW = item['password']  # array of salt and hashed password
                salt = passW[0]
                hashed = passW[1]
                hashed_password = bcrypt.hashpw(password.encode(), salt)
                print(hashed_password == hashed)

                if hashed_password == hashed:
                    token_unfurbished = secrets.token_bytes(32)
                    token = base64.b64encode(token_unfurbished).decode('utf-8')
                    session_token = hashlib.sha256(token.encode()).hexdigest()

                    user_collection.update_one({'email': email}, {'$set': {'session_token': session_token}})

                    response = flask.make_response(flask.send_file('../HTML/LandingPage.html'))
                    response.set_cookie('session_token', session_token)

                    return response
                else:
                    return flask.make_response('Invalid details entered', 400)


    return flask.make_response("Invalid method", 400)


@app.websocket('/websocket')
async def websocket(websocket):
    try:
        # Perform the WebSocket handshake
        await websocket.accept()

        # Keep the connection alive
        while True:
            # Wait for incoming messages
            message = await websocket.recv()

            # Do something with the message
            print(f"Received message: {message}")

            # Send a response back
            await websocket.send("Response message")

    except websockets.exceptions.ConnectionClosedOK:
        print("Connection closed")


if __name__ == '__main__':
    app.run()
