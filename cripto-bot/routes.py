from app import app, mysql
from flask import render_template

@app.route('/')
def Index():
    return render_template('index.html')

@app.route('/index-btc')
def Index_btc():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM registros')
    data = cur.fetchall()
    print(data)
    return render_template('index-btc.html', registros=data)

@app.route('/index-eth')
def Index_eth():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM registros_eth')
    data = cur.fetchall()
    print(data)
    return render_template('index-eth.html', registros=data)

@app.route('/index-ada')
def Index_ada():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM registros_ada')
    data = cur.fetchall()
    print(data)
    return render_template('index-ada.html', registros=data)

@app.route('/index-doge')
def Index_doge():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM registros_doge')
    data = cur.fetchall()
    print(data)
    return render_template('index-doge.html', registros=data)

@app.route('/index-matic')
def Index_matic():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM registros_matic')
    data = cur.fetchall()
    print(data)
    return render_template('index-matic.html', registros=data)
