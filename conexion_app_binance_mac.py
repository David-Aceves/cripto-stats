from flask import Flask, render_template, request, url_for, redirect, flash
from flaskext.mysql import MySQL
from flask_mysqldb import MySQL

mysql = MySQL()
app = Flask(__name__)

# MySQL Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'Cripto'

#Iniciar la app
mysql.init_app(app)

# Settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM registros')
    data = cur.fetchall()
    print(data)
    return render_template('index.html', registros = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        open = request.form['open']
        high = request.form['high']
        low = request.form['low']
        close = request.form['close']
        price = request.form['price']
        
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO registros (open, high, low, close, price) VALUES (%s, %s, %s, %s, %s)',(open,high,low,price,close))
        mysql.connection.commit()
        flash('Registro anadido correctamente')
        return redirect(url_for('Index'))

@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM registros WHERE id = %s',(id))
    data = cur.fetchall()
    print(data)
    flash('Editado correctamente')
    return render_template('edit-contact.html', registro = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        open = request.form['open']
        high = request.form['high']
        low = request.form['low']
        close = request.form['close']
        price = request.form['price']
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE registros
        SET open = %s,
            high = %s,
            low = %s,
            close = %s,
            price = %s
        WHERE id = %s
    """,(open,high,low,close,price,id))
    mysql.connection.commit()
    flash('Registro acutalizado correctamente')
    return redirect(url_for('Index'))
    

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM registros WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Registro elimindo correctamente')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port=3000,debug=True)