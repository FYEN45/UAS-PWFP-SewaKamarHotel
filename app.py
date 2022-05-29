# Import Library yang dibutuhkanimport MySQLdb
from datetime import timedelta
import MySQLdb
from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = '@#$123456&*()'

# Session Lifetime
app.permanent_session_lifetime = timedelta(minutes=10)

# Koneksi MYSQL (Tanpa SQLAlchemy)
# Mempersiapkan koneksi dengan server mysql.
# Menentukan HOST, USER, PASSWORD, dan DATABASE yang akan diakses
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sewakamarhotel_db'

mysql = MySQL(app)

# Routing website ke halaman Home (index.html)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tentangKami')
def tentangKami():
    return render_template('tentangKami.html')

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# BERANDA ADMIN / USER
# ------------------------------------------------------------------------------------------------------------------------------------------------------ 
@app.route('/home')
def home():
    if 'user' in session: 
        if session['status'] == "CLIENT":
            return render_template('client/berandaClient.html')
        elif session['status'] == "ADMIN":
            return render_template('admin/berandaAdmin.html')

    return redirect('/login')

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# CRUD USER
# ------------------------------------------------------------------------------------------------------------------------------------------------------ 
@app.route('/daftarUser', methods = ['GET', 'POST'])
def daftarUser():
    if 'user' in session:
        if session['status'] == "ADMIN":
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM user')
            hasil = cursor.fetchall()
        
            cursor.close()
            return render_template('admin/user/daftarUser.html', container = hasil)
    
    return redirect('/login')

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# CRUD KAMAR
# ------------------------------------------------------------------------------------------------------------------------------------------------------ 
@app.route('/daftarKamar', methods = ['GET', 'POST'])
def daftarKamar():
    if 'user' in session:
        if session['status'] == "ADMIN":
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM kamar')
            hasil = cursor.fetchall()
        
            cursor.close()
            return render_template('admin/kamar/daftarKamar.html', container = hasil)
    
    return redirect('/login')

@app.route('/tambahKamar', methods=['GET', 'POST'])
def tambahKamar():
    if 'user' in session:
        if session['status'] == "ADMIN":
            if (request.method == 'POST'):
                try:
                    # Menangambil input form
                    kamar = request.form
                    kode_kamar = kamar['kode_kamar']
                    nama_kamar = kamar['nama_kamar']
                    harga_kamar =  kamar['harga_kamar']
                    jumlah_kamar = kamar['jumlah_kamar']
                    kamar_tersedia = jumlah_kamar

                    # Menghubungkan ke database dan melakukan INSERT pada tabel anggota
                    cursor = mysql.connection.cursor()
                    cursor.execute('INSERT INTO kamar(kode_kamar, nama_kamar, harga_kamar, jumlah_kamar, kamar_tersedia) VALUES(%s, %s, %s, %s, %s)', (kode_kamar, nama_kamar, harga_kamar, jumlah_kamar, kamar_tersedia))
                    mysql.connection.commit()
                    cursor.close()
                    
                    flash('Berhasil menambahkan kamar!')
                    return redirect('/daftarKamar')
                
                except (MySQLdb.Error) as err:
                    # Menangkap error dan menampilkan pesan gagal
                    flash('Gagal menambahkan kamar! %d: %s' % (err.args[0], err.args[1]))
                    return redirect('/daftarKamar')

            return render_template('admin/kamar/tambahKamar.html')

    return redirect('/login')

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# LOGIN, LOGOUT & REGISTER
# ------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if (request.method == "POST"):
        # Mengambil input form login
        datalogin = request.form
        email = datalogin['email'].lower().strip()
        password = datalogin['password']

        # Melakukan SELECT untuk memeriksa apakah username dan password ada dalam database
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE email=%s AND password=%s', (email, password))
        hasil = cursor.fetchall()
        
        if (len(hasil) > 0):
            # Apabila terdapat data username dan password, verifikasi berhasil
            
            session.permanent = True
            session['user'] = hasil[0][1]
            session['status'] = hasil[0][5]
        
            flash('Login Berhasil! Welcome %s!' % hasil[0][1])
            return redirect('/login')
        else:
            # Apabila tidak ada data username dan password, verfikasi gagal
            flash('Username atau Password salah!')
            return render_template('login.html')
    
    else:
        if 'user' in session:
            return redirect('/home')

    return render_template('login.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if (request.method == 'POST'):
        try:
            # Menangambil input form
            user = request.form
            nama = user['nama'].title().strip()
            no_telepon = user['notelp'].strip()
            email = user['email'].lower().strip()
            password = user['password']
            status = 'CLIENT'

            # Menghubungkan ke database dan melakukan INSERT pada tabel anggota
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO user(nama, no_telepon, email, password, status) VALUES(%s, %s, %s, %s, %s)', (nama, no_telepon, email, password, status))
            mysql.connection.commit()
            cursor.close()
            
            flash('Berhasil Registrasi!')
            return redirect('/login')
        
        except (MySQLdb.Error) as err:
            # Menangkap error dan menampilkan pesan gagal
            flash('Gagal melakukan Registrasi! %d: %s' % (err.args[0], err.args[1]))
            return redirect('/register')
    
    else:
        if 'user' in session:
            return redirect('/home')

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('status', None)
    return redirect(url_for('index'))

# ------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug = True)