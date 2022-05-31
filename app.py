# Import Library yang dibutuhkanimport MySQLdb
from datetime import timedelta
import MySQLdb
from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = '@#$123456&*()'

# Session Lifetime
app.permanent_session_lifetime = timedelta(minutes=60)

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
    if 'nama_user' in session: 
        if session['status'] == "CLIENT":
            return render_template('client/berandaClient.html')
        elif session['status'] == "ADMIN":
            return render_template('admin/berandaAdmin.html')

    return redirect('/login')

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# CRUD USER
# ------------------------------------------------------------------------------------------------------------------------------------------------------ 

# DAFTAR USER - ADMIN
@app.route('/daftarUser')
def daftarUser():
    if 'nama_user' in session:
        if session['status'] == "ADMIN":
            try:
                cursor = mysql.connection.cursor()
                cursor.execute('SELECT * FROM user')
                hasil = cursor.fetchall()
            
                cursor.close()
                return render_template('admin/user/daftarUser.html', container = hasil)

            except (MySQLdb.Error) as err:
            # Menangkap error dan menampilkan pesan gagal
                flash('Gagal menampilkan daftar user! %d: %s' % (err.args[0], err.args[1]))
                return redirect('/home')
    
    return redirect('/login')

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# CRUD KAMAR
# ------------------------------------------------------------------------------------------------------------------------------------------------------ 

# DAFTAR KAMAR - ADMIN
@app.route('/daftarKamar')
def daftarKamar():
    if 'nama_user' in session:
        if session['status'] == "ADMIN":
            try: 
                cursor = mysql.connection.cursor()
                cursor.execute('SELECT * FROM kamar')
                hasil = cursor.fetchall()
            
                cursor.close()
                return render_template('admin/kamar/daftarKamar.html', container = hasil)
            except (MySQLdb.Error) as err:
                # Menangkap error dan menampilkan pesan gagal
                flash('Gagal menambahkan kamar! %d: %s' % (err.args[0], err.args[1]))
                return redirect('/home')
    
    return redirect('/login')

@app.route('/tambahKamar', methods=['GET', 'POST'])
def tambahKamar():
    if 'nama_user' in session:
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

                    # Menghubungkan ke database dan melakukan INSERT pada tabel kamar
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

# EDIT KAMAR - ADMIN
@app.route('/editKamar/<kodeKamar>', methods = ['GET', 'POST'])
def editKamar(kodeKamar):
    if 'nama_user' in session:
        if session['status'] == "ADMIN":
            if (request.method == 'POST'):
                try:
                    # Mengambil input dari form
                    kamar = request.form
                    kode_kamar = kamar['kode_kamar']
                    nama_kamar = kamar['nama_kamar']
                    harga_kamar =  kamar['harga_kamar']
                    jumlah_kamar = kamar['jumlah_kamar']
                    kamar_tersedia = kamar['kamar_tersedia']

                    # Menghubungkan ke database dan melakukan UPDATE pada tabel buku
                    cursor = mysql.connection.cursor()
                    cursor.execute('UPDATE kamar SET nama_kamar=%s, harga_kamar=%s, jumlah_kamar=%s, kamar_tersedia=%s WHERE kode_kamar=%s', (nama_kamar, harga_kamar, jumlah_kamar, kamar_tersedia, kode_kamar))
                    mysql.connection.commit()
                    cursor.close()

                    flash('Kamar berhasil diedit!')
                    return redirect('/daftarKamar')
                
                except (MySQLdb.Error) as err:
                    # Menangkap Error dan memberikan pesan gagal
                    flash('Buku gagal diedit! %d: %s' % (err.args[0], err.args[1]))
                    return redirect('/daftarKamar')
            
            # Menghubungkan ke database dan mengambil informasi buku yang akan di edit
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM kamar WHERE kode_kamar=%s', (kodeKamar,))
            hasil = cursor.fetchall()

            cursor.close()
            return render_template('admin/kamar/editKamar.html', container = hasil)
    
    return redirect('/login')

# HAPUS KAMAR - ADMIN
@app.route('/hapusKamar/<kodeKamar>', methods = ['GET', 'POST'])
def hapusKamar(kodeKamar):
    if 'nama_user' in session:
        if session['status'] == "ADMIN":
            try:
                cursor = mysql.connection.cursor()
                cursor.execute('DELETE FROM kamar WHERE kode_kamar=%s', (kodeKamar,))
                mysql.connection.commit()        
                cursor.close()
                
                flash('Kamar berhasil dihapus!')
                return redirect('/daftarKamar')

            except (MySQLdb.Error) as err:
                # Menangkap error dan memberikan pesan gagal
                flash('Kamar gagal dihapus! %d: %s' % (err.args[0], err.args[1]))
                return redirect('/daftarKamar')

    return redirect('/login')

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# CRUD RESERVASI
# ------------------------------------------------------------------------------------------------------------------------------------------------------    

# DAFTAR RESERVASI - ADMIN
@app.route('/daftarReservasi')
def daftarReservasi():
    if 'nama_user' in session:
        if session['status'] == "ADMIN":
            try:
                cursor = mysql.connection.cursor()
                cursor.execute('SELECT * FROM reservasi')
                reservasi = cursor.fetchall()

                cursor.execute('SELECT * FROM statuscheck')
                status = cursor.fetchall()
                cursor.close()

                hasil = []

                for x in range(len(reservasi)):
                    hasil.append(reservasi[x] + status[x])

                return render_template('admin/reservasi/daftarReservasi.html', container = hasil)
            
            except (MySQLdb.Error) as err:
                # Menangkap error dan memberikan pesan gagal
                flash('Gagal menampilkan daftar reservasi! %d: %s' % (err.args[0], err.args[1]))
                return redirect('/home')

    return redirect('/login')

# TAMBAH RESERVASI - ADMIN
@app.route('/tambahReservasi', methods=['GET', 'POST'])
def tambahReservasi():
    if 'nama_user' in session:
        if session['status'] == "ADMIN":
            if (request.method == 'POST'):
                hasil = request.form
                kodeReservasi = hasil['kode_reservasi']
                kodeUser = hasil['kode_user']
                kodeKamar = hasil['kode_kamar']
                tglCheckin = hasil['tglCheckin']
                jumlahMalam = hasil['jumlah_malam']

                return redirect('/konfirmasiReservasi/{}/{}/{}/{}/{}'.format(kodeReservasi, kodeUser, kodeKamar, tglCheckin, jumlahMalam))

            try: 
                cursor = mysql.connection.cursor()
                cursor.execute('SELECT * FROM kamar')
                kamar = cursor.fetchall()

                cursor.execute('SELECT * FROM user WHERE status="CLIENT"')
                user = cursor.fetchall()
                cursor.close()

                return render_template('admin/reservasi/tambahReservasi.html', container = [user, kamar])

            except (MySQLdb.Error) as err:
                # Menangkap error dan memberikan pesan gagal
                flash('Gagal menampilkan data! %d: %s' % (err.args[0], err.args[1]))
                return redirect('/daftarReservasi')
        
        elif session['status'] == "CLIENT":
            if (request.method == 'POST'):
                hasil = request.form
                kodeReservasi = hasil['kode_reservasi']
                kodeUser = hasil['kode_user']
                kodeKamar = hasil['kode_kamar']
                tglCheckin = hasil['tglCheckin']
                jumlahMalam = hasil['jumlah_malam']

                return redirect('/konfirmasiReservasi/{}/{}/{}/{}/{}'.format(kodeReservasi, kodeUser, kodeKamar, tglCheckin, jumlahMalam))

            try: 
                cursor = mysql.connection.cursor()
                cursor.execute('SELECT * FROM kamar')
                kamar = cursor.fetchall()

                cursor.execute('SELECT * FROM user WHERE kode_user="%s"', (session['kode_user'],))
                user = cursor.fetchall()
                cursor.close()

                return render_template('client/reservasi/tambahReservasi.html', container = [user, kamar])
            
            except (MySQLdb.Error) as err:
                # Menangkap error dan memberikan pesan gagal
                flash('Gagal menampilkan data! %d: %s' % (err.args[0], err.args[1]))
                return redirect('/home')
    
    return redirect('/login')

# KONFIRMASI RESERVASI - ADMIN & CLIET
@app.route('/konfirmasiReservasi/<kodeReservasi>/<kodeUser>/<kodeKamar>/<tglCheckin>/<jumlahMalam>', methods=['GET', 'POST'])
def konfirmasiReservasi(kodeReservasi, kodeUser, kodeKamar, tglCheckin, jumlahMalam):
    if 'nama_user' in session:
        if (request.method == "POST"):
            hasil = request.form
            kodeReservasi = hasil['kode_reservasi']
            kodeUser = hasil['kode_user']
            kodeKamar = hasil['kode_kamar']
            tglCheckin = hasil['tglCheckin']
            jumlahMalam = hasil['jumlahMalam']
            tglCheckout = hasil['tglCheckout']
            totalBiaya = hasil['totalBiaya']

            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM kamar WHERE kode_kamar="{}"'.format(kodeKamar))
            kamar = cursor.fetchall()
            cursor.close()

            if (int(kamar[0][4]) >= 1):
                try:
                    cursor = mysql.connection.cursor()
                    cursor.execute('INSERT INTO reservasi(kode_reservasi, kode_user, kode_kamar, tgl_checkin, tgl_checkout, jumlah_malam, total_biaya) VALUES(%s, %s, %s, %s, %s, %s, %s)', (kodeReservasi, kodeUser, kodeKamar, tglCheckin, tglCheckout, jumlahMalam, totalBiaya))
                    cursor.execute('INSERT INTO statuscheck(kode_reservasi, isCheckin, isCheckout) VALUES(%s, %s, %s)', (kodeReservasi, "NO", "NO"))
                    cursor.execute('UPDATE kamar SET kamar_tersedia=%s WHERE kode_kamar=%s', (int(kamar[0][4] - 1), kamar[0][0]))
                    mysql.connection.commit()
                    cursor.close()
                    flash('Berhasil melakukan reservasi!')

                except (MySQLdb.Error) as err:
                    # Menangkap error dan memberikan pesan gagal
                    flash('Gagal melakukan reservasi! %d: %s' % (err.args[0], err.args[1]))
                    return redirect('/home')

            else:
                flash('Gagal melakukan Reservasi, kamar tidak tersedia!')
                        
            return redirect('/home')

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM kamar WHERE kode_kamar="{}"'.format(kodeKamar))
        kamar = cursor.fetchall()
        cursor.close()

        hargaMalam = kamar[0][2]

        data = [kodeReservasi, kodeUser, kodeKamar, tglCheckin, jumlahMalam, hargaMalam]
        return render_template('admin/reservasi/konfirmasiReservasi.html', container = data)
    
    return redirect('/login')

# HAPUS RESERVASI - ADMIN
@app.route('/hapusReservasi/<kodeReservasi>', methods=['GET', 'POST'])
def hapusReservasi(kodeReservasi):   
    if 'nama_user' in session:
        if session['status'] == "ADMIN":
            try: 
                cursor = mysql.connection.cursor()
                cursor.execute('DELETE FROM statuscheck WHERE kode_reservasi=%s', (kodeReservasi,))
                cursor.execute('DELETE FROM reservasi WHERE kode_reservasi=%s', (kodeReservasi,))
                mysql.connection.commit()
                cursor.close()
                flash('Berhasil menghapus reservasi!')

            except (MySQLdb.Error) as err:
                # Menangkap error dan memberikan pesan gagal
                flash('Gagal menghapus reservasi! %d: %s' % (err.args[0], err.args[1]))
            
            return redirect('/daftarReservasi')

    return redirect('/login')

# RESERVASI CHECKIN - ADMIN
@app.route('/checkin/<kodeReservasi>', methods=['GET', 'POST'])
def checkin(kodeReservasi):   
    if 'nama_user' in session:
        if session['status'] == "ADMIN":
            try :
                cursor = mysql.connection.cursor()
                cursor.execute('UPDATE statuscheck SET isCheckin=%s WHERE kode_reservasi=%s', ("YES", kodeReservasi))
                mysql.connection.commit()

            except (MySQLdb.Error) as err:
                # Menangkap error dan memberikan pesan gagal
                flash('Gagal checkin! %d: %s' % (err.args[0], err.args[1]))

            return redirect('/daftarReservasi')

    return redirect('/login')

# RESERVASI CHECKOUT - ADMIN
@app.route('/checkout/<kodeReservasi>/<kodeKamar>', methods=['GET', 'POST'])
def checkout(kodeReservasi, kodeKamar):   
    if 'nama_user' in session:
        if session['status'] == "ADMIN":
            try:
                cursor = mysql.connection.cursor()
                cursor.execute('SELECT * FROM kamar WHERE kode_kamar="{}"'.format(kodeKamar))
                kamar = cursor.fetchall()
        
                cursor.execute('UPDATE statuscheck SET isCheckout=%s WHERE kode_reservasi=%s', ("YES", kodeReservasi))
                cursor.execute('UPDATE kamar SET kamar_tersedia=%s WHERE kode_kamar=%s', (int(kamar[0][4] + 1), kamar[0][0]))

                mysql.connection.commit()
                cursor.close()
            
            except (MySQLdb.Error) as err:
                # Menangkap error dan memberikan pesan gagal
                flash('Gagal checkout! %d: %s' % (err.args[0], err.args[1]))

            return redirect('/daftarReservasi')

    return redirect('/login')


# ------------------------------------------------------------------------------------------------------------------------------------------------------
# LOGIN, LOGOUT & REGISTER
# ------------------------------------------------------------------------------------------------------------------------------------------------------

# LOGIN - ADMIN & CLIENT
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if (request.method == "POST"):
        # Mengambil input form login
        datalogin = request.form
        email = datalogin['email'].lower().strip()
        password = datalogin['password']

        # Melakukan SELECT untuk memeriksa apakah username dan password ada dalam database
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM user WHERE email=%s AND password=%s', (email, password))
            hasil = cursor.fetchall()

        except (MySQLdb.Error) as err:
                # Menangkap error dan memberikan pesan gagal
                flash('Gagal checkin! %d: %s' % (err.args[0], err.args[1]))
                return redirect('/login')
            
        if (len(hasil) > 0):
            # Apabila terdapat data username dan password, verifikasi berhasil
            
            session.permanent = True
            session['kode_user'] = hasil[0][0]
            session['nama_user'] = hasil[0][1]
            session['status'] = hasil[0][5]
        
            flash('Login Berhasil! Welcome %s!' % hasil[0][1])
            return redirect('/login')
        else:
            # Apabila tidak ada data username dan password, verfikasi gagal
            flash('Username atau Password salah!')
            return render_template('login.html')
    
    else:
        if 'nama_user' in session:
            return redirect('/home')

    return render_template('login.html')

# REGISTER
@app.route('/register', methods = ['GET', 'POST'])
def register():
    if (request.method == 'POST'):
        try:
            # Menangambil input form
            user = request.form
            kodeUser = user['kode_user'].lower().strip()
            nama = user['nama'].title().strip()
            no_telepon = user['notelp'].strip()
            email = user['email'].lower().strip()
            password = user['password']
            status = 'CLIENT'

            # Menghubungkan ke database dan melakukan INSERT pada tabel anggota
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO user(kode_user, nama, no_telepon, email, password, status) VALUES(%s, %s, %s, %s, %s, %s)', (kodeUser, nama, no_telepon, email, password, status))
            mysql.connection.commit()
            cursor.close()
            
            flash('Berhasil Registrasi!')
            return redirect('/login')
        
        except (MySQLdb.Error) as err:
            # Menangkap error dan menampilkan pesan gagal
            flash('Gagal melakukan Registrasi! %d: %s' % (err.args[0], err.args[1]))
            return redirect('/register')
    
    else:
        if 'nama_user' in session:
            return redirect('/home')

    return render_template('register.html')

# LOGOUT
@app.route('/logout')
def logout():
    session.pop('_flashes', None)
    session.pop('kode_user', None)
    session.pop('nama_user', None)
    session.pop('status', None)
    return redirect(url_for('index'))

# ------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug = True)