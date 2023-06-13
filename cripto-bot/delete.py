from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL
from binance.client import Client
import pandas as pd
import matplotlib as plt
import plotly.express as px
import plotly.graph_objs as go
import plotly.offline as pyo
from plotly.offline import plot
from config import api_key, api_secret


# App
app = Flask(__name__)

# MySQL Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'criptos_binance'
mysql = MySQL(app)

# Settings
app.secret_key = 'mysecretkey'

@app.route('/delete/btc/<string:id>')
def delete_btc(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM registros WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Registro eliminado correctamente')
    # Cerrar la conexión con Binance
    return redirect(url_for('Index_btc'))

@app.route('/delete/eth/<string:id>')
def delete_eth(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM registros_eth WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Registro eliminado correctamente')
    return redirect(url_for('Index_eth'))

@app.route('/delete/ada/<string:id>')
def delete_ada(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM registros_ada WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Registro eliminado correctamente')
    return redirect(url_for('Index_ada'))

@app.route('/delete/doge/<string:id>')
def delete_doge(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM registros_doge WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Registro eliminado correctamente')
    return redirect(url_for('Index_doge'))

@app.route('/delete/matic/<string:id>')
def delete_matic(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM registros_matic WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Registro eliminado correctamente')
    return redirect(url_for('Index_matic'))
    data = cur.fetchall()
    print(data)
    return render_template('index-matic-candle.html', registros = data)
