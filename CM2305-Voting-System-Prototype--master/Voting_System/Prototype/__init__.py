from flask import Flask
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import mysql.connector
import mysql
import os
import urllib.parse

app = Flask(__name__)
app.config['SECRET_KEY'] = 'de7f35de261b964a421d1f296a151bf76ecffe5207861827'

db_url = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url if db_url else 'mysql+pymysql://root:PASSWORD@localhost:3306/votedb'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

if db_url:
    clean_url = db_url.replace("mysql+pymysql://", "mysql://")
    parsed_url = urllib.parse.urlparse(clean_url)
    votedb = mysql.connector.connect(
        host=parsed_url.hostname,
        user=parsed_url.username,
        password=parsed_url.password,
        port=parsed_url.port or 3306,
        database=parsed_url.path[1:]
    )
else:
    votedb = mysql.connector.connect(
        host="localhost",
        user="root",
        port=3306,
        auth_plugin='mysql_native_password',
        passwd='root',
        database='votedb'
    )

mail_settings = {
    "MAIL_SERVER": '://gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'vote.prototype@gmail.com',
    "MAIL_PASSWORD": 'xkazmyfdWdyXJ9p'
}

mail = Mail(app)

from Prototype import routes
