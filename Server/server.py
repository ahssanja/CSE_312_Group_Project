import flask
from pymongo import MongoClient

app = flask.Flask(__name__)


mongo_client = MongoClient('mongo')
db = mongo_client['cse312Team']
chat_collection = db["users"]

@app.route('/' ,methods=['GET', 'POST'])
def login():

    return flask.send_file('../HTML/LoginPage.html')

@app.route('/HTML/RegisterPage.html', methods=['GET', 'POST'])
def register():
    return flask.send_file('../HTML/RegisterPage.html')


if __name__ == '__main__':
    app.run()