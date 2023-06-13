from app import app, mysql, client
from flask import request, flash, redirect, url_for

@app.route('/add_register_btc', methods=['POST'])
def add_register_btc():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM registros')
    data = cur.fetchall()
    if request.method == 'POST':
        precio_actual = client.get_avg_price(symbol='BTCUSDT')
        precio_actual = float(precio_actual.get('price'))
        lista_precios = []
        lista_precios.append(precio_actual)
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO registros (price) VALUES (%s)',lista_precios)
        mysql.connection.commit()
        flash('Registro añadido correctamente')
        return redirect(url_for('Index_btc'))

@app.route('/add_register_eth', methods=['POST'])
def add_register_eth():
    if request.method == 'POST':
        precio_actual = client.get_avg_price(symbol='ETHUSDT')
        precio_actual = float(precio_actual.get('price'))
        lista_precios = []
        lista_precios.append(precio_actual)
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO registros_eth (price) VALUES (%s)',lista_precios)
        mysql.connection.commit()
        flash('Registro añadido correctamente')
        return redirect(url_for('Index_eth'))

@app.route('/add_register_ada', methods=['POST'])
def add_register_ada():
    if request.method == 'POST':
        precio_actual = client.get_avg_price(symbol='ADAUSDT')
        precio_actual = float(precio_actual.get('price'))
        lista_precios = []
        lista_precios.append(precio_actual)
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO registros_ada (price) VALUES (%s)',lista_precios)
        mysql.connection.commit()
        flash('Registro añadido correctamente')
        return redirect(url_for('Index_ada'))

@app.route('/add_register_doge', methods=['POST'])
def add_register_doge():
    if request.method == 'POST':
        precio_actual = client.get_avg_price(symbol='DOGEUSDT')
        precio_actual = float(precio_actual.get('price'))
        lista_precios = []
        lista_precios.append(precio_actual)
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO registros_doge (price) VALUES (%s)',lista_precios)
        mysql.connection.commit()
        flash('Registro añadido correctamente')
        return redirect(url_for('Index_doge'))
    
@app.route('/add_register_matic', methods=['POST'])
def add_register_matic():
    if request.method == 'POST':
        precio_actual = client.get_avg_price(symbol='MATICUSDT')
        precio_actual = float(precio_actual.get('price'))
        lista_precios = []
        lista_precios.append(precio_actual)
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO registros_matic (price) VALUES (%s)',lista_precios)
        mysql.connection.commit()
        flash('Registro añadido correctamente')
        return redirect(url_for('Index_matic'))
