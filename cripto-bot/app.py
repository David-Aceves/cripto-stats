from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL
from binance.client import Client
import pandas as pd
import matplotlib as plt
import plotly.graph_objs as go
import plotly.offline as pyo
from plotly.offline import plot
from config import api_key, api_secret


# Cliente y contras binance
client = Client(api_key, api_secret)
print(client)
print('logged in')

# Obtiene el precio del bitcoin
precio_actual = client.get_avg_price(symbol='BTCUSDT')
precio_actual = float(precio_actual.get('price'))

app = Flask(__name__)

# MySQL Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'criptos_binance'
mysql = MySQL(app)

# Settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    return render_template('index.html')

@app.route('/index-btc')
def Index_btc():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM registros')
    data = cur.fetchall()
    print(data)
    return render_template('index-btc.html', registros = data)

@app.route('/index-btc-candle')
def Index_btc_candle():
    return render_template('index-btc-candle.html')

@app.route('/add_register_btc', methods=['POST'])
def add_register_btc():
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

@app.route('/show_candle_30_btc', methods=['POST'])
def show_candle_30_btc():
    klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_30MINUTE, "1 day ago UTC")

    ohlc_data = []
    for kline in klines:
        time, open, high, low, close = kline[:5]
        ohlc_data.append([time, float(open), float(high), float(low), float(close)])

    df = pd.DataFrame(klines, columns=["Timestamp","Open","High","Low","Close","6","7","8","9","10","11","12"])
    df['Timestamp']=pd.to_datetime(df['Timestamp']/1000)
    print(df.head())

    candle = go.Candlestick(
        x=[x[0] for x in ohlc_data],
        open=[x[1] for x in ohlc_data],
        high=[x[2] for x in ohlc_data],
        low=[x[3] for x in ohlc_data],
        close=[x[4] for x in ohlc_data]
    )

    data = [candle]
    layout = go.Layout(title='Gráfico de velas BTC/USDT',xaxis=dict(title='Time'),yaxis=dict(title='Precio'))
    fig = go.Figure(data=data, layout=layout)

    pyo.plot(fig, filename='grafico.html')
    #plot(fig)
    return redirect(url_for('Index_btc'))

@app.route('/show_candle_15_btc', methods=['POST'])
def show_candle_15_btc():
    klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "1 day ago UTC")

    ohlc_data = []
    for kline in klines:
        time, open, high, low, close = kline[:5]
        ohlc_data.append([time, float(open), float(high), float(low), float(close)])

    df = pd.DataFrame(klines, columns=["Timestamp","Open","High","Low","Close","6","7","8","9","10","11","12"])
    #df['Timestamp']=pd.to_datetime(df['Timestamp'])
    print(df.head())

    candle = go.Candlestick(
        x=[x[0] for x in ohlc_data],
        open=[x[1] for x in ohlc_data],
        high=[x[2] for x in ohlc_data],
        low=[x[3] for x in ohlc_data],
        close=[x[4] for x in ohlc_data]
    )

    data = [candle]
    layout = go.Layout(title='Gráfico de velas BTC/USDT',xaxis=dict(title='Time'),yaxis=dict(title='Precio'))
    fig = go.Figure(data=data, layout=layout)

    pyo.plot(fig, filename='grafico.html')
    #plot(fig)
    return redirect(url_for('Index_btc'))

@app.route('/show_candle_1_btc', methods=['POST'])
def show_candle_1_btc():
    klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

    ohlc_data = []
    for kline in klines:
        time, open, high, low, close = kline[:5]
        ohlc_data.append([time, float(open), float(high), float(low), float(close)])

    df = pd.DataFrame(klines, columns=["Timestamp","Open","High","Low","Close","6","7","8","9","10","11","12"])
    #df['Timestamp']=pd.to_datetime(df['Timestamp'])
    print(df.head())

    candle = go.Candlestick(
        x=[x[0] for x in ohlc_data],
        open=[x[1] for x in ohlc_data],
        high=[x[2] for x in ohlc_data],
        low=[x[3] for x in ohlc_data],
        close=[x[4] for x in ohlc_data]
    )

    data = [candle]
    layout = go.Layout(title='Gráfico de velas BTC/USDT',xaxis=dict(title='Time'),yaxis=dict(title='Precio'))
    fig = go.Figure(data=data, layout=layout)

    pyo.plot(fig, filename='grafico.html')
    #plot(fig)
    return redirect(url_for('Index_btc'))

@app.route('/plot_price_btc', methods=['POST'])
def plot_price_btc():
    cur = mysql.connection.cursor()
    cur.execute('SELECT price,date FROM registros')
    results = cur.fetchall()
    prices = [row[0] for row in results]
    dates = [row[1] for row in results]

    trace = go.Scatter(x=dates, y=prices,mode='lines',name='Precio BTC')

    layout = go.Layout(title='Grafico - Precio BTCUSDT',
                       xaxis=dict(title='Dates'),
                       yaxis=dict(title='Prices')) 
    
    fig = go.Figure(data=[trace],layout=layout)
    pyo.plot(fig, filename='grafica_precio.html')
    return redirect(url_for('Index_btc'))

@app.route('/delete/<string:id>')
def delete_btc(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM registros WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Registro eliminado correctamente')
    return redirect(url_for('Index_btc'))

@app.route('/index-eth')
def Index_eth():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM registros_eth')
    data = cur.fetchall()
    print(data)
    return render_template('index-eth.html', registros = data)

@app.route('/index-eth-candle')
def Index_eth_candle():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM registros_eth')
    data = cur.fetchall()
    print(data)
    return render_template('index-eth-candle.html', registros = data)

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
    
@app.route('/show_candle_30_eth', methods=['POST'])
def show_candle_30_eth():
    klines = client.get_historical_klines("ETHUSDT", Client.KLINE_INTERVAL_30MINUTE, "1 day ago UTC")

    ohlc_data = []
    for kline in klines:
        time, open, high, low, close = kline[:5]
        ohlc_data.append([time, float(open), float(high), float(low), float(close)])

    df = pd.DataFrame(klines, columns=["Timestamp","Open","High","Low","Close","6","7","8","9","10","11","12"])
    df['Timestamp']=pd.to_datetime(df['Timestamp']/1000)
    print(df.head())

    candle = go.Candlestick(
        x=[x[0] for x in ohlc_data],
        open=[x[1] for x in ohlc_data],
        high=[x[2] for x in ohlc_data],
        low=[x[3] for x in ohlc_data],
        close=[x[4] for x in ohlc_data]
    )

    data = [candle]
    layout = go.Layout(title='Gráfico de velas ETH/USDT',xaxis=dict(title='Time'),yaxis=dict(title='Precio'))
    fig = go.Figure(data=data, layout=layout)

    pyo.plot(fig, filename='grafico.html')
    #plot(fig)
    return redirect(url_for('Index_eth'))

@app.route('/show_candle_15_eth', methods=['POST'])
def show_candle_15_eth():
    klines = client.get_historical_klines("ETHUSDT", Client.KLINE_INTERVAL_15MINUTE, "1 day ago UTC")

    ohlc_data = []
    for kline in klines:
        time, open, high, low, close = kline[:5]
        ohlc_data.append([time, float(open), float(high), float(low), float(close)])

    df = pd.DataFrame(klines, columns=["Timestamp","Open","High","Low","Close","6","7","8","9","10","11","12"])
    #df['Timestamp']=pd.to_datetime(df['Timestamp'])
    print(df.head())

    candle = go.Candlestick(
        x=[x[0] for x in ohlc_data],
        open=[x[1] for x in ohlc_data],
        high=[x[2] for x in ohlc_data],
        low=[x[3] for x in ohlc_data],
        close=[x[4] for x in ohlc_data]
    )

    data = [candle]
    layout = go.Layout(title='Gráfico de velas BTC/USDT',xaxis=dict(title='Time'),yaxis=dict(title='Precio'))
    fig = go.Figure(data=data, layout=layout)

    pyo.plot(fig, filename='grafico.html')
    #plot(fig)
    return redirect(url_for('Index_btc'))

@app.route('/show_candle_1_eth', methods=['POST'])
def show_candle_1_eth():
    klines = client.get_historical_klines("ETHUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

    ohlc_data = []
    for kline in klines:
        time, open, high, low, close = kline[:5]
        ohlc_data.append([time, float(open), float(high), float(low), float(close)])

    df = pd.DataFrame(klines, columns=["Timestamp","Open","High","Low","Close","6","7","8","9","10","11","12"])
    #df['Timestamp']=pd.to_datetime(df['Timestamp'])
    print(df.head())

    candle = go.Candlestick(
        x=[x[0] for x in ohlc_data],
        open=[x[1] for x in ohlc_data],
        high=[x[2] for x in ohlc_data],
        low=[x[3] for x in ohlc_data],
        close=[x[4] for x in ohlc_data]
    )

    data = [candle]
    layout = go.Layout(title='Gráfico de velas ETH/USDT',xaxis=dict(title='Time'),yaxis=dict(title='Precio'))
    fig = go.Figure(data=data, layout=layout)

    pyo.plot(fig, filename='grafico.html')
    #plot(fig)
    return redirect(url_for('Index_btc'))

@app.route('/plot_price_eth', methods=['POST'])
def plot_price_eth():
    cur = mysql.connection.cursor()
    cur.execute('SELECT price,date FROM registros_eth')
    results = cur.fetchall()
    prices = [row[0] for row in results]
    dates = [row[1] for row in results]

    trace = go.Scatter(x=dates, y=prices,mode='lines',name='Precio BTC')

    layout = go.Layout(title='Grafico - Precio ETHUSDT',
                       xaxis=dict(title='Dates'),
                       yaxis=dict(title='Prices')) 
    
    fig = go.Figure(data=[trace],layout=layout)
    pyo.plot(fig, filename='grafica_precio.html')
    return redirect(url_for('Index_eth'))

@app.route('/delete/<string:id>')
def delete_eth(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM registros_eth WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Registro eliminado correctamente')
    return redirect(url_for('Index_eth'))

@app.route('/index-ada')
def Index_ada():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM registros_ada')
    data = cur.fetchall()
    print(data)
    return render_template('index-ada.html', registros = data)

@app.route('/index-ada-candle')
def Index_ada_candle():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM registros_ada')
    data = cur.fetchall()
    print(data)
    return render_template('index-ada-candle.html', registros = data)

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
    
@app.route('/show_candle_30_ada', methods=['POST'])
def show_candle_30_ada():
    klines = client.get_historical_klines("ADAUSDT", Client.KLINE_INTERVAL_30MINUTE, "1 day ago UTC")

    ohlc_data = []
    for kline in klines:
        time, open, high, low, close = kline[:5]
        ohlc_data.append([time, float(open), float(high), float(low), float(close)])

    df = pd.DataFrame(klines, columns=["Timestamp","Open","High","Low","Close","6","7","8","9","10","11","12"])
    df['Timestamp']=pd.to_datetime(df['Timestamp']/1000)
    print(df.head())

    candle = go.Candlestick(
        x=[x[0] for x in ohlc_data],
        open=[x[1] for x in ohlc_data],
        high=[x[2] for x in ohlc_data],
        low=[x[3] for x in ohlc_data],
        close=[x[4] for x in ohlc_data]
    )

    data = [candle]
    layout = go.Layout(title='Gráfico de velas ADA/USDT',xaxis=dict(title='Time'),yaxis=dict(title='Precio'))
    fig = go.Figure(data=data, layout=layout)

    pyo.plot(fig, filename='grafico.html')
    #plot(fig)
    return redirect(url_for('Index_ada'))

@app.route('/show_candle_15_ada', methods=['POST'])
def show_candle_15_ada():
    klines = client.get_historical_klines("ADAUSDT", Client.KLINE_INTERVAL_15MINUTE, "1 day ago UTC")

    ohlc_data = []
    for kline in klines:
        time, open, high, low, close = kline[:5]
        ohlc_data.append([time, float(open), float(high), float(low), float(close)])

    df = pd.DataFrame(klines, columns=["Timestamp","Open","High","Low","Close","6","7","8","9","10","11","12"])
    #df['Timestamp']=pd.to_datetime(df['Timestamp'])
    print(df.head())

    candle = go.Candlestick(
        x=[x[0] for x in ohlc_data],
        open=[x[1] for x in ohlc_data],
        high=[x[2] for x in ohlc_data],
        low=[x[3] for x in ohlc_data],
        close=[x[4] for x in ohlc_data]
    )

    data = [candle]
    layout = go.Layout(title='Gráfico de velas ADA/USDT',xaxis=dict(title='Time'),yaxis=dict(title='Precio'))
    fig = go.Figure(data=data, layout=layout)

    pyo.plot(fig, filename='grafico.html')
    #plot(fig)
    return redirect(url_for('Index_ada'))

@app.route('/show_candle_1_ada', methods=['POST'])
def show_candle_1_ada():
    klines = client.get_historical_klines("ADAUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

    ohlc_data = []
    for kline in klines:
        time, open, high, low, close = kline[:5]
        ohlc_data.append([time, float(open), float(high), float(low), float(close)])

    df = pd.DataFrame(klines, columns=["Timestamp","Open","High","Low","Close","6","7","8","9","10","11","12"])
    #df['Timestamp']=pd.to_datetime(df['Timestamp'])
    print(df.head())

    candle = go.Candlestick(
        x=[x[0] for x in ohlc_data],
        open=[x[1] for x in ohlc_data],
        high=[x[2] for x in ohlc_data],
        low=[x[3] for x in ohlc_data],
        close=[x[4] for x in ohlc_data]
    )

    data = [candle]
    layout = go.Layout(title='Gráfico de velas ADA/USDT',xaxis=dict(title='Time'),yaxis=dict(title='Precio'))
    fig = go.Figure(data=data, layout=layout)

    pyo.plot(fig, filename='grafico.html')
    #plot(fig)
    return redirect(url_for('Index_ada'))

@app.route('/plot_price_ada', methods=['POST'])
def plot_price_ada():
    cur = mysql.connection.cursor()
    cur.execute('SELECT price,date FROM registros_ada')
    results = cur.fetchall()
    prices = [row[0] for row in results]
    dates = [row[1] for row in results]

    trace = go.Scatter(x=dates, y=prices,mode='lines',name='Precio ADA')

    layout = go.Layout(title='Grafico - Precio ADAUSDT',
                       xaxis=dict(title='Dates'),
                       yaxis=dict(title='Prices')) 
    
    fig = go.Figure(data=[trace],layout=layout)
    pyo.plot(fig, filename='grafica_precio.html')
    return redirect(url_for('Index_ada'))

@app.route('/delete/<string:id>')
def delete_ada(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM registros_ada WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Registro eliminado correctamente')
    return redirect(url_for('Index_ada'))

@app.route('/index-doge')
def Index_doge():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM registros_doge')
    data = cur.fetchall()
    print(data)
    return render_template('index-doge.html', registros = data)

@app.route('/index-doge-candle')
def Index_doge_candle():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM registros_doge')
    data = cur.fetchall()
    print(data)
    return render_template('index-doge-candle.html', registros = data)

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
    
@app.route('/show_candle_30_doge', methods=['POST'])
def show_candle_30_doge():
    klines = client.get_historical_klines("DOGEUSDT", Client.KLINE_INTERVAL_30MINUTE, "1 day ago UTC")

    ohlc_data = []
    for kline in klines:
        time, open, high, low, close = kline[:5]
        ohlc_data.append([time, float(open), float(high), float(low), float(close)])

    df = pd.DataFrame(klines, columns=["Timestamp","Open","High","Low","Close","6","7","8","9","10","11","12"])
    df['Timestamp']=pd.to_datetime(df['Timestamp']/1000)
    print(df.head())

    candle = go.Candlestick(
        x=[x[0] for x in ohlc_data],
        open=[x[1] for x in ohlc_data],
        high=[x[2] for x in ohlc_data],
        low=[x[3] for x in ohlc_data],
        close=[x[4] for x in ohlc_data]
    )

    data = [candle]
    layout = go.Layout(title='Gráfico de velas DOGE/USDT',xaxis=dict(title='Time'),yaxis=dict(title='Precio'))
    fig = go.Figure(data=data, layout=layout)

    pyo.plot(fig, filename='grafico.html')
    #plot(fig)
    return redirect(url_for('Index_ada'))

@app.route('/show_candle_15_doge', methods=['POST'])
def show_candle_15_doge():
    klines = client.get_historical_klines("DOGEUSDT", Client.KLINE_INTERVAL_15MINUTE, "1 day ago UTC")

    ohlc_data = []
    for kline in klines:
        time, open, high, low, close = kline[:5]
        ohlc_data.append([time, float(open), float(high), float(low), float(close)])

    df = pd.DataFrame(klines, columns=["Timestamp","Open","High","Low","Close","6","7","8","9","10","11","12"])
    #df['Timestamp']=pd.to_datetime(df['Timestamp'])
    print(df.head())

    candle = go.Candlestick(
        x=[x[0] for x in ohlc_data],
        open=[x[1] for x in ohlc_data],
        high=[x[2] for x in ohlc_data],
        low=[x[3] for x in ohlc_data],
        close=[x[4] for x in ohlc_data]
    )

    data = [candle]
    layout = go.Layout(title='Gráfico de velas DOGE/USDT',xaxis=dict(title='Time'),yaxis=dict(title='Precio'))
    fig = go.Figure(data=data, layout=layout)

    pyo.plot(fig, filename='grafico.html')
    #plot(fig)
    return redirect(url_for('Index_doge'))

@app.route('/show_candle_1_doge', methods=['POST'])
def show_candle_1_doge():
    klines = client.get_historical_klines("DOGEUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

    ohlc_data = []
    for kline in klines:
        time, open, high, low, close = kline[:5]
        ohlc_data.append([time, float(open), float(high), float(low), float(close)])

    df = pd.DataFrame(klines, columns=["Timestamp","Open","High","Low","Close","6","7","8","9","10","11","12"])
    #df['Timestamp']=pd.to_datetime(df['Timestamp'])
    print(df.head())

    candle = go.Candlestick(
        x=[x[0] for x in ohlc_data],
        open=[x[1] for x in ohlc_data],
        high=[x[2] for x in ohlc_data],
        low=[x[3] for x in ohlc_data],
        close=[x[4] for x in ohlc_data]
    )

    data = [candle]
    layout = go.Layout(title='Gráfico de velas DOGE/USDT',xaxis=dict(title='Time'),yaxis=dict(title='Precio'))
    fig = go.Figure(data=data, layout=layout)

    pyo.plot(fig, filename='grafico.html')
    #plot(fig)
    return redirect(url_for('Index_doge'))

@app.route('/plot_price_doge', methods=['POST'])
def plot_price_doge():
    cur = mysql.connection.cursor()
    cur.execute('SELECT price,date FROM registros_doge')
    results = cur.fetchall()
    prices = [row[0] for row in results]
    dates = [row[1] for row in results]

    trace = go.Scatter(x=dates, y=prices,mode='lines',name='Precio ADA')

    layout = go.Layout(title='Grafico - Precio DOGEUSDT',
                       xaxis=dict(title='Dates'),
                       yaxis=dict(title='Prices')) 
    
    fig = go.Figure(data=[trace],layout=layout)
    pyo.plot(fig, filename='grafica_precio.html')
    return redirect(url_for('Index_doge'))

@app.route('/delete/<string:id>')
def delete_doge(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM registros_doge WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Registro eliminado correctamente')
    return redirect(url_for('Index_doge'))

@app.route('/index-matic')
def Index_matic():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM registros_matic')
    data = cur.fetchall()
    print(data)
    return render_template('index-matic.html', registros = data)

@app.route('/index-matic-candle')
def Index_matic_candle():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM registros_matic')
    return render_template('index-matic-candle.html')

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
    
@app.route('/show_candle_30_matic', methods=['POST'])
def show_candle_30_matic():
    klines = client.get_historical_klines("MATICUSDT", Client.KLINE_INTERVAL_30MINUTE, "1 day ago UTC")

    ohlc_data = []
    for kline in klines:
        time, open, high, low, close = kline[:5]
        ohlc_data.append([time, float(open), float(high), float(low), float(close)])

    df = pd.DataFrame(klines, columns=["Timestamp","Open","High","Low","Close","6","7","8","9","10","11","12"])
    df['Timestamp']=pd.to_datetime(df['Timestamp']/1000)
    print(df.head())

    candle = go.Candlestick(
        x=[x[0] for x in ohlc_data],
        open=[x[1] for x in ohlc_data],
        high=[x[2] for x in ohlc_data],
        low=[x[3] for x in ohlc_data],
        close=[x[4] for x in ohlc_data]
    )

    data = [candle]
    layout = go.Layout(title='Gráfico de velas MATIC/USDT',xaxis=dict(title='Time'),yaxis=dict(title='Precio'))
    fig = go.Figure(data=data, layout=layout)

    pyo.plot(fig, filename='grafico.html')
    #plot(fig)
    return redirect(url_for('Index_matic'))

@app.route('/show_candle_15_matic', methods=['POST'])
def show_candle_15_matic():
    klines = client.get_historical_klines("MATICUSDT", Client.KLINE_INTERVAL_15MINUTE, "1 day ago UTC")

    ohlc_data = []
    for kline in klines:
        time, open, high, low, close = kline[:5]
        ohlc_data.append([time, float(open), float(high), float(low), float(close)])

    df = pd.DataFrame(klines, columns=["Timestamp","Open","High","Low","Close","6","7","8","9","10","11","12"])
    #df['Timestamp']=pd.to_datetime(df['Timestamp'])
    print(df.head())

    candle = go.Candlestick(
        x=[x[0] for x in ohlc_data],
        open=[x[1] for x in ohlc_data],
        high=[x[2] for x in ohlc_data],
        low=[x[3] for x in ohlc_data],
        close=[x[4] for x in ohlc_data]
    )

    data = [candle]
    layout = go.Layout(title='Gráfico de velas MATIC/USDT',xaxis=dict(title='Time'),yaxis=dict(title='Precio'))
    fig = go.Figure(data=data, layout=layout)

    pyo.plot(fig, filename='grafico.html')
    #plot(fig)
    return redirect(url_for('Index_matic'))

@app.route('/show_candle_1_matic', methods=['POST'])
def show_candle_1_matic():
    klines = client.get_historical_klines("MATICUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

    ohlc_data = []
    for kline in klines:
        time, open, high, low, close = kline[:5]
        ohlc_data.append([time, float(open), float(high), float(low), float(close)])

    df = pd.DataFrame(klines, columns=["Timestamp","Open","High","Low","Close","6","7","8","9","10","11","12"])
    #df['Timestamp']=pd.to_datetime(df['Timestamp'])
    print(df.head())

    candle = go.Candlestick(
        x=[x[0] for x in ohlc_data],
        open=[x[1] for x in ohlc_data],
        high=[x[2] for x in ohlc_data],
        low=[x[3] for x in ohlc_data],
        close=[x[4] for x in ohlc_data]
    )

    data = [candle]
    layout = go.Layout(title='Gráfico de velas MATIC/USDT',xaxis=dict(title='Time'),yaxis=dict(title='Precio'))
    fig = go.Figure(data=data, layout=layout)

    pyo.plot(fig, filename='grafico.html')
    #plot(fig)
    return redirect(url_for('Index_matic'))

@app.route('/plot_price_matic', methods=['POST'])
def plot_price_matic():
    cur = mysql.connection.cursor()
    cur.execute('SELECT price,date FROM registros_matic')
    results = cur.fetchall()
    prices = [row[0] for row in results]
    dates = [row[1] for row in results]

    trace = go.Scatter(x=dates, y=prices,mode='lines',name='Precio MATIC')

    layout = go.Layout(title='Grafico - Precio MATICUSDT',
                       xaxis=dict(title='Dates'),
                       yaxis=dict(title='Prices')) 
    
    fig = go.Figure(data=[trace],layout=layout)
    pyo.plot(fig, filename='grafica_precio.html')
    return redirect(url_for('Index_matic'))

@app.route('/delete/<string:id>')
def delete_matic(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM registros_matic WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Registro eliminado correctamente')
    return redirect(url_for('Index_matic'))
    data = cur.fetchall()
    print(data)
    return render_template('index-matic-candle.html', registros = data)


if __name__ == '__main__':
    app.run(port=3000,debug=True)