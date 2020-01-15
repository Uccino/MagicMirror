from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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
