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

if db_url:
    if not db_url.startswith("mysql://") and not db_url.startswith("mysql+pymysql://"):
        parse_target = "mysql://" + db_url
    else:
        parse_target = db_url.replace("mysql+pymysql://", "mysql://")
        
    parsed_url = urllib.parse.urlparse(parse_target)
    safe_password = urllib.parse.quote_plus(parsed_url.password) if parsed_url.password else ""
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{parsed_url.username}:{safe_password}@{parsed_url.hostname}:{parsed_url.port or 3306}{parsed_url.path}"
    
    votedb = mysql.connector.connect(
        host=parsed_url.hostname,
        user=parsed_url.username,
        password=parsed_url.password,
        port=parsed_url.port or 3306,
        database=parsed_url.path[1:] if parsed_url.path else "defaultdb"
    )
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:PASSWORD@localhost:3306/votedb'
    votedb = mysql.connector.connect(
        host="localhost",
        user="root",
        port=3306,
        auth_plugin='mysql_native_password',
        passwd='root',
        database='votedb'
    )

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

mail_settings = {
    "MAIL_SERVER": '://gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'vote.prototype@gmail.com',
    "MAIL_PASSWORD": 'xkazmyfdWdyXJ9p'
}

app.config.update(mail_settings)
mail = Mail(app)

from Prototype import routes
