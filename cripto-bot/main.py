from mymodule import *
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL
from binance_client import client
from config import api_key, api_secret

app = Flask(__name__)

# MySQL Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'criptos_binance'
mysql = MySQL(app)

# Settings
app.secret_key = 'mysecretkey'


if __name__ == "__main__":
    app.run()
