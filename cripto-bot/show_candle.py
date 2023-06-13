from app import app, client
from flask import redirect, url_for
import pandas as pd
import plotly.graph_objs as go
from binance.client import Client
from config import api_key, api_secret

# Cliente y contras binance
client = Client(api_key, api_secret)

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
    fig.write_html("./static/grafico_30_btc.html")
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

    fig.write_html("./static/grafico_15_btc.html")
    #pyo.plot(fig, filename='grafico.html')
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

    fig.write_html("./static/grafico_1_btc.html")
    #pyo.plot(fig, filename='grafico.html')
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
    fig.write_html("./static/grafico_precio_btc.html")
    return redirect(url_for('Index_btc'))


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

    fig.write_html("./static/grafico_30_eth.html")
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

    fig.write_html("./static/grafico_15_eth.html")
    #pyo.plot(fig, filename='grafico.html')
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

    fig.write_html("./static/grafico_1_eth.html")
    #pyo.plot(fig, filename='grafico.html')
    #plot(fig)
    return redirect(url_for('Index_eth'))

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
    fig.write_html("./static/grafico_precio_eth.html")
    #pyo.plot(fig, filename='grafica_precio.html')
    return redirect(url_for('Index_eth'))


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

    fig.write_html("./static/grafico_30_ada.html")
    #pyo.plot(fig, filename='grafico.html')
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

    fig.write_html("./static/grafico_15_ada.html")
    #pyo.plot(fig, filename='grafico.html')
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

    fig.write_html("./static/grafico_1_ada.html")
    #pyo.plot(fig, filename='grafico.html')
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
    fig.write_html("./static/grafico_precio_ada.html")
    pyo.plot(fig, filename='grafica_precio.html')
    return redirect(url_for('Index_ada'))


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
    fig.write_html("./static/grafico_30_doge.html")
    return redirect(url_for('Index_doge'))

@app.route('/show_candle_15_doge', methods=['POST'])
def show_candle_15_doge():
    klines = client.get_historical_klines("DOGEUSDT", Client.KLINE_INTERVAL_15MINUTE, "1 day ago UTC")

    ohlc_data = []
    for kline in klines:
        time, open, high, low, close = kline[:5]
        ohlc_data.append([time, float(open), float(high), float(low), float(close)])

    df = pd.DataFrame(klines, columns=["Timestamp","Open","High","Low","Close","6","7","8","9","10","11","12"])
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

    fig.write_html("./static/grafico_15_doge.html")
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

    fig.write_html("./static/grafico_1_doge.html")
    #pyo.plot(fig, filename='grafico.html')
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
    fig.write_html("./static/grafico_precio_doge.html")
    return redirect(url_for('Index_doge'))


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
    
    fig.write_html("./static/grafico_30_matic.html")
    #pyo.plot(fig, filename='grafico.html')
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

    fig.write_html("./static/grafico_15_matic.html")
    #pyo.plot(fig, filename='grafico.html')
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
    fig.write_html("./static/grafico_1_matic.html")
    #pyo.plot(fig, filename='grafico.html')
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

    fig.write_html("./static/grafico_precio_matic.html")
    #pyo.plot(fig, filename='grafica_precio.html')
    return redirect(url_for('Index_matic'))
