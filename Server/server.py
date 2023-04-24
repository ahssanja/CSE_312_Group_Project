import flask
from pymongo import MongoClient
import html

app = flask.Flask(__name__)




# Create a global list to store games
games = []

# A list of players looking for a game
lobby = []

mongo_client = MongoClient('mongo')
db = mongo_client['cse312Team']
user_collection = db["users"]

#HTML
@app.route('/' ,methods=['GET', 'POST'])
def loginhtml():
    return flask.send_file('../HTML/LoginPage.html')

@app.route('/HTML/RegisterPage.html', methods=['GET', 'POST'])
def registerhtml():
    return flask.send_file('../HTML/RegisterPage.html')


#javascript
@app.route('/Server/TheGame.js' ,methods=['GET', 'POST'])
def jsfile():
    return flask.send_file('../Server/TheGame.js')



#CSS
@app.route('/CSS/LoginPage.css' ,methods=['GET', 'POST'])
def logincss():
    return flask.send_file('../CSS/LoginPage.css')
@app.route('/CSS/RegisterPage.css' ,methods=['GET', 'POST'])
def registercss():
    return flask.send_file('../CSS/RegisterPage.css')

@app.route('/CSS/LandingPage.css' ,methods=['GET', 'POST'])
def landingpagecss():
    return flask.send_file('../CSS/LandingPage.css')


@app.route('/MadeNewAccount' ,methods=['GET', 'POST'])
def made_new_account():
    if flask.request.method == 'POST':
        entire_data = flask.request.form
        email = entire_data.get('email')
        password = entire_data.get('password')
        username = entire_data.get('username')
        confirmpassword = entire_data.get('confirmpassword')

        if password != confirmpassword:
            return "password and confirm passwords don't match"

        if len(password) and len(confirmpassword) < 8:
            return "password too short. Needs at least 8 characters"

        store_stuff = {}
        store_stuff['email'] = html.escape(email)
        store_stuff['password'] = html.escape(password)
        store_stuff['username'] = html.escape(username)
        store_stuff['confirmed'] = html.escape(confirmpassword)
        store_stuff['wins'] = 0

        with open('../HTML/LandingPage.html', 'rb') as b:
            htmlfile = b.read()
            htmlfile = htmlfile.replace(b'{X}', store_stuff['username'].encode())


        #user_collection.insert_one(store_stuff)


    return flask.send_file('../HTML/LandingPage.html')


@app.route('/LoggedIn', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        entire_data = flask.request.form
        email = entire_data.get('email')
        password = entire_data.get('password')

        data = user_collection.find({})

        for item in data:
            if item['email'] == email and item['password'] == password:
                with open('index.html', 'rb') as b:
                    htmlfile = b.read()
                    htmlfile = htmlfile.replace(b'{X}', item['username'].encode())

                return flask.send_file('../HTML/LandingPage.html')
            else:
                return 'Invalid login/password details'


# Handle POST request to "/lookingforplayers"
@app.route('/lookingforplayers', methods=['POST'])
def looking_for_players():
    global lobby #array
    player = flask.request.remote_addr  #NOT SEECURE, NEED TO USE SESSION IDs INSTEAD
    if player not in lobby:
        lobby.append(player)

    return '', 200

# Handle GET request to "/checklobby"


@app.route('/checklobby', methods=['GET'])
def check_lobby():
    global lobby
    global games

    # Check if there are at least two players in the lobby
    if len(lobby) > 1:
        # Create a new game and assign the first two players in the lobby to it
        games.append([lobby[0], lobby[1]])
        lobby = lobby[2:]
        retval_ID = {'game_id': len(games)}

        # Return the game ID to the clients
        return flask.jsonify(retval_ID)
    else:
        return flask.jsonify({'game_id': -1})



if __name__ == '__main__':
    app.run()