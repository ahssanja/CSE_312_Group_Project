import flask
from pymongo import MongoClient

app = flask.Flask(__name__)


mongo_client = MongoClient('mongo')
db = mongo_client['cse312Team']
chat_collection = db["users"]


@app.route('/' ,methods=['GET', 'POST'])
def login():
    return flask.send_file('../HTML/LoginPage.html')

@app.route('/CSS/LoginPage.css' ,methods=['GET', 'POST'])
def logincss():
    return flask.send_file('../CSS/LoginPage.css')

@app.route('/HTML/RegisterPage.html', methods=['GET', 'POST'])
def register():
    return flask.send_file('../HTML/RegisterPage.html')
@app.route('/CSS/RegisterPage.css' ,methods=['GET', 'POST'])
def registercss():
    return flask.send_file('../CSS/RegisterPage.css')

if __name__ == '__main__':
    app.run()