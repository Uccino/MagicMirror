from flask import Flask
from flask import render_template
import logging

app = Flask(
    __name__,
    template_folder='./flask/templates',    
    static_folder='./flask/static'
)

def main():
    StartServer(True)

def StartServer(debugValue = False):
    log = logging.getLogger('werkzeug')
    
    if debugValue == True:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.ERROR)

    app.run(debug=debugValue)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/sendnews')
def sendnews():
    return "Update the news!"

@app.route('/getnews')
def getnews():
    return "Get the news!"

if __name__ == '__main__':
    main()
