from flask import Flask
import logging

app = Flask(__name__)

def StartServer():
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    app.run(debug=False)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/login')
def login():
    return "Login"

@app.route('/sendnews')
def sendnews():
    return "Update the news!"

@app.route('/getnews')
def getnews():
    return "Get the news!"