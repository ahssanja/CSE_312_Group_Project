import flask
from pymongo import MongoClient

app = flask.Flask(__name__)


mongo_client = MongoClient('mongo')
db = mongo_client['cse312Team']
user_collection = db["users"]


@app.route('/' ,methods=['GET', 'POST'])
def loginhtml():
    return flask.send_file('../HTML/LoginPage.html')

@app.route('/CSS/LoginPage.css' ,methods=['GET', 'POST'])
def logincss():
    return flask.send_file('../CSS/LoginPage.css')

@app.route('/HTML/RegisterPage.html', methods=['GET', 'POST'])
def registerhtml():
    return flask.send_file('../HTML/RegisterPage.html')
@app.route('/CSS/RegisterPage.css' ,methods=['GET', 'POST'])
def registercss():
    return flask.send_file('../CSS/RegisterPage.css')


@app.route('/MadeNewAccount' ,methods=['GET', 'POST'])
def made_new_account():
    if flask.request.method == 'POST':
        entire_data = flask.request.form
        email = entire_data.get('email')
        password = entire_data.get('password')
        username = entire_data.get('username')
        confirmpassword = entire_data.get('confirmpassword')

        store_stuff = {}
        store_stuff['email'] = email
        store_stuff['password'] = password
        store_stuff['username'] = username
        store_stuff['confirmed'] = confirmpassword

        user_collection.insert_one(store_stuff)


    return 'You have successfully made an account'


@app.route('/LoggedIn' ,methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        entire_data = flask.request.form
        email = entire_data.get('email')
        password = entire_data.get('password')

        print('Received email:', email)
        print('Received password:', password)

        data = user_collection.find({})

        for item in data:
            if item['email'] == email and item['password'] == password:
                return 'You have successfully logged in'
            else:
                return 'Invalid login/ password details'



if __name__ == '__main__':
    app.run()