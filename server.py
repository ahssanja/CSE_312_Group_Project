import flask
from pymongo import MongoClient
import html
import re
import bcrypt
import os
import hashlib
import base64
import secrets
import random
import time



salt_size = 10
app = flask.Flask(__name__, template_folder='templates')

players_waiting = []
ongoinggames = []

mongo_client = MongoClient('mongo')
db = mongo_client['cse312Team']
user_collection = db["users"]
lobby_db = db["lobby"]


def generateGameId():
    timestamp = int(time.time())  # get the current timestamp as an integer
    random_str = ''.join(random.choices('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*', k=8))
    return str(timestamp) + '_' + random_str  # combine the timestamp and random string with a hyphen

# templates
@app.route('/', methods=['GET', 'POST'])
def loginhtml():
    return flask.send_file('templates/LoginPage.html')


@app.route('/HTML/RegisterPage.html', methods=['GET', 'POST'])
def registerhtml():
    return flask.send_file('templates/RegisterPage.html')


# Javascript
@app.route('/Server/TheGame.js', methods=['GET', 'POST'])
def jsfile():
    return flask.send_file('Scripts/TheGame.js')


# CSS
@app.route('/CSS/LoginPage.css', methods=['GET', 'POST'])
def logincss():
    return flask.send_file('CSS/LoginPage.css')


@app.route('/CSS/RegisterPage.css', methods=['GET', 'POST'])
def registercss():
    return flask.send_file('CSS/RegisterPage.css')



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

    return flask.send_file('templates/LoginPage.html')


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


                if hashed_password == hashed:
                    token_unfurbished = secrets.token_bytes(32)
                    token = base64.b64encode(token_unfurbished).decode('utf-8')
                    session_token = hashlib.sha256(token.encode()).hexdigest()

                    user_collection.update_one({'email': email}, {'$set': {'session_token': session_token}})


                    response = flask.make_response(flask.render_template('LandingPage.html', username=item['username']))
                    response.set_cookie('session_token', session_token)

                    return response



                else:
                    return flask.make_response('Invalid details entered', 400)

    return flask.make_response("Invalid method", 400)


@app.route('/join-lobby', methods=['POST'])
def join_lobby():

    playerid = flask.request.json['player_id']
    lobby_db.insert_one({'player':playerid})

    players_waiting = list(lobby_db.find({}))

    if len(players_waiting) >= 2:

        the_ids = []
        for player in lobby_db.find({}):
            the_ids.append(player['_id'])
            lobby_db.delete_one({'_id': player['_id']})

        player1_id = the_ids.pop(0)
        player2_id = the_ids.pop(0)

        game_id = generateGameId()
        ongoinggames.append(game_id)

        player_ids = f'{player1_id},{player2_id}'
        base_url = flask.url_for('gamePg', _external=True)
        game_url = f"{base_url}?id={game_id}&player_ids={player_ids}"

        return flask.render_template(game_url)

    return '', 200





if __name__ == '__main__':
    app.run()
