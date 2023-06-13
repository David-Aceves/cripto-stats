from flask_mysqldb import MySQL
from flask import Flask

def setup_mysql(app):
    # MySQL Connection
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'criptos_binance'
    mysql = MySQL(app)
    return mysql

def setup_app():
    app = Flask(__name__)
    app.secret_key = 'mysecretkey'
    return app
