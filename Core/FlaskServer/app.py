from flask import Flask, request, render_template, flash, redirect, jsonify, session
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from settings import app, Flask, db
import logging
import sys
import flask_models


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
            flash("Log in om de nieuwswebsite te bekijken")
            return redirect('/news/login')

    return wrap


@app.route('/news/')
@login_required
def index():
    all_posts = flask_models.Post.query.filter_by(active=1).all()
    return render_template('index.html', data=all_posts, admin=session.get("admin"))

# Route for the login page
@app.route('/news/login', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        if 'logged_in' in session:
            return redirect('/news')
        return render_template('login.html', session=session.get("logged_in"))
    else:
        username = request.form["username"]
        password = request.form["password"]

        user = flask_models.User.query.filter_by(
            username=username, password=password).first()

        if user is not None:
            if user.admin == 1:
                session["admin"] = True
            session["user_id"] = user.id
            session["logged_in"] = True
            return redirect('/news')
        else:
            return redirect('/news/login')


@app.route('/news/logout')
def logout():
    session.clear()
    return redirect("/news/login")


@app.route('/news/create', methods=["POST"])
@login_required
def createpost():
    postTitle = request.form['post_title']
    postContent = request.form['post_content']
    newPost = flask_models.Post(title=postTitle, content=postContent)
    db.session.add(newPost)
    db.session.commit()
    flash("Nieuwsbericht succesvol aangemaakt")
    return redirect('/news')

# Route for getting the latest news
@app.route('/news/get', methods=["GET"])
def getnews():
    all_posts = flask_models.Post.query.limit(5).all()

    return jsonify(posts=[
        i.serialize() for i in all_posts
    ])


@app.route('/news/delete', methods=["POST"])
def deletenews():
    post_id = request.form["deletebutton"]
    post = flask_models.Post.query.filter_by(id=post_id).first()
    post.active = 0

    db.session.commit()

    return redirect("/news")


@app.route('/news/users/add', methods=["POST", "GET"])
def addusers():
    if request.method == "GET":
        return render_template('adduser.html', admin=session.get("admin"))
    else:
        username = request.form['username']
        password = request.form['password']

        newuser = flask_models.User(username=username, password=password)
        db.session.add(newuser)
        db.session.commit()

        flash("Gebruiker succesvol toegevoegd")
        return redirect('/news')


@app.route('/news/users/manage', methods=["POST", "GET"])
def deleteusers():
    if request.method == "GET":
        users = flask_models.User.query.all()
        return render_template("users.html", users=users, admin=session.get("admin"))
    else:
        if "adminbutton" in request.form:
            user_id = request.form["adminbutton"]
            user = flask_models.User.query.filter_by(id=user_id).first()
            user.admin = 1
            db.session.commit()
            flash(
                f"Gebruiker {user.username} succesvol toegevoegd aan beheerders!")
        elif "deletebutton" in request.form:
            user_id = request.form["deletebutton"]
            if str(user_id) == str(session["user_id"]):
                flash("Je kan niet jezelf verwijderen!")
                return redirect("/news/users/manage")
            user = flask_models.User.query.filter_by(id=user_id).first()
            db.session.delete(user)
            db.session.commit()
            flash(f"Gebruiker {user.username} succesvol verwijderd!")
    return redirect("/news/users/manage", admin=session.get("admin"))


@app.route("/mirror")
def mirror():
    return render_template("mirror.html")


# This only gets used when we start the webserver.py via shell
if __name__ == '__main__':
    StartServer(sys.argv[1], sys.argv[2], True)
