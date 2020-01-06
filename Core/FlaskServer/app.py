import flask_models
from flask import Flask, request, render_template, flash, redirect, jsonify, session
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
import logging
import sys

# Flask setup
app = Flask(
    __name__,
    template_folder='./templates',
    static_folder='./static'
)

app.secret_key = 'SUPERSECRETKEYSKRKT'

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news_site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# We import the models **AFTER** initializing the database
# Starts the server


def StartServer(ip, port, debugValue=False):
    # Set the logging value according to the debug settings
    log = logging.getLogger('werkzeug')

    if debugValue:
        log.setLevel(logging.DEBUG)
    else:
        logging.getLogger('werkzeug').disabled = True
        logging.disable = True
        log.setLevel(logging.FATAL)
    app.run(debug=debugValue, host=ip, port=port)


def login_required(f):
    """[Decorator to check if an user has been logged in]

    Arguments:
        f {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Login to acces the news page")
            return redirect('/news/login')

    return wrap

# Flask app routes are defined here
@app.route('/news/')
@login_required
def index():
    all_posts = flask_models.Post.query.all()
    return render_template('index.html', data=all_posts)

# Route for the login page
@app.route('/news/login', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        if 'logged_in' in session:
            return redirect('/news')
        return render_template('login.html')
    else:
        username = request.form["username"]
        password = request.form["password"]

        user = flask_models.User.query.filter_by(
            username=username, password=password).first()
        if user is not None:
            session["logged_in"] = True
            return redirect('/news')
        else:
            return redirect('/news/login')

# Route for creating a new post
@app.route('/news/sendnews', methods=["POST"])
@login_required
def sendnews():
    postTitle = request.form['post_title']
    postContent = request.form['post_content']
    newPost = flask_models.Post(title=postTitle, content=postContent)
    db.session.add(newPost)
    db.session.commit()
    flash("Post created succesfully!")
    return redirect('/news')

# Route for getting the latest news
@app.route('/news/getnews', methods=["GET"])
def getnews():
    all_posts = flask_models.Post.query.limit(5).all()
    return jsonify(posts=[
        i.serialize() for i in all_posts
    ])


@app.route('/news/delete', methods=["POST"])
def deleteitem():
    item_id = request.form["deletebutton"]
    flask_models.Post.query.filter_by(id=item_id).delete()
    return redirect('/news')


@app.route("/mirror")
def mirror():
    return render_template("mirror.html")


# This only gets used when we start the webserver.py via shell
if __name__ == '__main__':
    StartServer(sys.argv[1], sys.argv[2], True)
