# Import Library yang dibutuhkanimport MySQLdb
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = '@#$123456&*()'

# Koneksi MYSQL (Tanpa SQLAlchemy)
# Mempersiapkan koneksi dengan server mysql.
# Menentukan HOST, USER, PASSWORD, dan DATABASE yang akan diakses
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'peminjamanbuku_db'

mysql = MySQL(app)

# Routing website ke halaman Home (index.html)
@app.route('/')
def index():
    return render_template('index.html')






# ------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug = True)