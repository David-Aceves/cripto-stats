from flask import render_template, request, url_for, redirect, flash
from plotly.offline import plot
import plotly.express as px
import plotly.graph_objs as go
from main import client
import pandas as pd

def index():
    return render_template('index.html')

def index_btc(mysql):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM registros')
    data = cur.fetchall()
    print(data)
    return render_template('index-btc.html', registros=data)

def index_eth(mysql):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM registros_eth')
    data = cur.fetchall()
    print(data)
    return render_template('index-eth.html', registros=data)

# Agrega las otras funciones para los demás índices...

def add_register_btc(request, client, mysql):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM registros')
    data = cur.fetchall()
    if request.method == 'POST':
        precio_actual = client.get_avg_price(symbol='BTCUSDT')
        precio_actual = float(precio_actual.get('price'))
        lista_precios = []
        lista_precios.append(precio_actual)
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO registros (price) VALUES (%s)', lista_precios)
        mysql.connection.commit()
        flash('Registro añadido correctamente')
        return render_template('index-btc.html', registros=data)

# Agrega las otras funciones para agregar registros...

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
    fig.write_html("./static/grafico_30_btc.html")
    return redirect(url_for('Index_btc'))
