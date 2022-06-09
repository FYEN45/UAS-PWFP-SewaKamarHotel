# Import Library yang dibutuhkanimport MySQLdb
from datetime import timedelta
import os
import pdfkit
import MySQLdb
from flask import Flask, make_response, render_template, request, redirect, send_file, session, url_for, flash
from flask_mail import Mail, Message
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

# Config untuk Generate PDF
app.config['PDF_FOLDER'] = os.path.realpath('.') + '/static/document'
app.config['TEMPLATE_FOLDER'] = os.path.realpath('.') + '/templates'

# Config Email
# Untuk mempersiapkan config mengirim email
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'chandrakelvin799@gmail.com' # Email (Tumbal)
app.config['MAIL_PASSWORD'] = 'zlzkyfalsegcvoli' # App Password (Google)
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# HALAMAN UTAMA / TENTANG KAMI
# ------------------------------------------------------------------------------------------------------------------------------------------------------ 

# Routing website ke Halaman Utama (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Routing website ke Halaman Tentang Kami
@app.route('/tentangKami')
def tentangKami():
    return render_template('tentangKami.html')

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# BERANDA ADMIN / USER
# ------------------------------------------------------------------------------------------------------------------------------------------------------ 

# Routing website ke Halaman Beranda
@app.route('/home')
def home():
    if 'nama_user' in session: 
        if session['status'] == "CLIENT":
            # Jika status user CLIENT, render halaman beranda client
            return render_template('client/berandaClient.html')
        elif session['status'] == "ADMIN":
            # Jika status user CLIENT, render halaman beranda admin
            return render_template('admin/berandaAdmin.html')

    return redirect('/login')

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# CRUD USER
# ------------------------------------------------------------------------------------------------------------------------------------------------------ 

# DAFTAR USER - ADMIN
# Menampilkan data user yang terdaftar
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

# HAPUS USER - ADMIN
# Menghapus user yang terdaftar dalam database
@app.route('/hapusUser/<kodeUser>', methods = ['GET', 'POST'])
def hapusUser(kodeUser):
    if 'nama_user' in session:
        if session['status'] == "ADMIN":
            try:
                # Menghubungkan ke database dan melakukan DELETE
                cursor = mysql.connection.cursor()
                cursor.execute('DELETE FROM user WHERE kode_user=%s', (kodeUser,))
                mysql.connection.commit()        
                cursor.close()
                
                # Mengirim pesan berhasil menghapus kamar
                flash('User berhasil dihapus!')
                return redirect('/daftarUser')

            except (MySQLdb.Error) as err:
                # Menangkap error dan memberikan pesan gagal
                flash('User gagal dihapus! %d: %s' % (err.args[0], err.args[1]))
                return redirect('/daftarUser')

    return redirect('/login')

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# CRUD KAMAR
# ------------------------------------------------------------------------------------------------------------------------------------------------------ 

# DAFTAR KAMAR - ADMIN
# Menampilkan daftar kamar yang ada dalam database
@app.route('/daftarKamar')
def daftarKamar():
    if 'nama_user' in session:
        if session['status'] == "ADMIN":
            try: 
                # Menghubungkan ke database dan melakukan SELECT
                cursor = mysql.connection.cursor()
                cursor.execute('SELECT * FROM kamar')
                hasil = cursor.fetchall()
            
                cursor.close()
                return render_template('admin/kamar/daftarKamar.html', container = hasil)
            except (MySQLdb.Error) as err:
                # Menangkap error dan menampilkan pesan gagal
                flash('Gagal menampilkan daftar kamar! %d: %s' % (err.args[0], err.args[1]))
                return redirect('/home')
    
    return redirect('/login')

# TAMBAH KAMAR - ADMIN
# Menambahkan kamar ke dalam database
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
# Mengedit data kamar yang ada dalam database
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
            
            # Menghubungkan ke database dan mengambil informasi kamar yang akan di edit
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM kamar WHERE kode_kamar=%s', (kodeKamar,))
            hasil = cursor.fetchall()

            cursor.close()
            return render_template('admin/kamar/editKamar.html', container = hasil)
    
    return redirect('/login')

# HAPUS KAMAR - ADMIN
# Menghapus kamar yang terdaftar didalam database
@app.route('/hapusKamar/<kodeKamar>', methods = ['GET', 'POST'])
def hapusKamar(kodeKamar):
    if 'nama_user' in session:
        if session['status'] == "ADMIN":
            try:
                # Menghubungkan ke database dan melakukan DELETE
                cursor = mysql.connection.cursor()
                cursor.execute('DELETE FROM kamar WHERE kode_kamar=%s', (kodeKamar,))
                mysql.connection.commit()        
                cursor.close()
                
                # Mengirim pesan berhasil menghapus kamar
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
# Menampilkan daftar reservasi yang ada dalam database
@app.route('/daftarReservasi')
def daftarReservasi():
    if 'nama_user' in session:
        if session['status'] == "ADMIN":
            try:
                # Menghubungkan ke database dan melakukan SELECT pada tabel reservasi
                cursor = mysql.connection.cursor()
                cursor.execute('SELECT * FROM reservasi')
                reservasi = cursor.fetchall()

                # Menghubungkan ke database dan melakukan SELECT pada tabel statuscheck
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
        if (request.method == 'POST'):
                # Mengambil input form
                hasil = request.form
                kodeReservasi = hasil['kode_reservasi']
                kodeUser = hasil['kode_user']
                kodeKamar = hasil['kode_kamar']
                tglCheckin = hasil['tglCheckin']
                jumlahMalam = hasil['jumlah_malam']

                return redirect('/konfirmasiReservasi/{}/{}/{}/{}/{}'.format(kodeReservasi, kodeUser, kodeKamar, tglCheckin, jumlahMalam))

        if session['status'] == "ADMIN":
            try: 
                # Menghubungkan ke database dan melakukan Select pada tabel kamar
                cursor = mysql.connection.cursor()
                cursor.execute('SELECT * FROM kamar')
                kamar = cursor.fetchall()

                # Menghubungkan ke database dan melakukan Select pada tabel user
                cursor.execute('SELECT * FROM user WHERE status="CLIENT"')
                user = cursor.fetchall()
                cursor.close()

                return render_template('admin/reservasi/tambahReservasi.html', container = [user, kamar])

            except (MySQLdb.Error) as err:
                # Menangkap error dan memberikan pesan gagal
                flash('Gagal menampilkan data! %d: %s' % (err.args[0], err.args[1]))
                return redirect('/daftarReservasi')
        
        elif session['status'] == "CLIENT":
            try: 
                # Menghubungkan ke database dan melakukan Select pada tabel kamar
                cursor = mysql.connection.cursor()
                cursor.execute('SELECT * FROM kamar')
                kamar = cursor.fetchall()

                # Menghubungkan ke database dan melakukan Select pada tabel user yang dipilih
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
# Melakukan konfirmasi pemesanan
# Pada halaman ini, total biaya menginap akan ditampilkan
@app.route('/konfirmasiReservasi/<kodeReservasi>/<kodeUser>/<kodeKamar>/<tglCheckin>/<jumlahMalam>', methods=['GET', 'POST'])
def konfirmasiReservasi(kodeReservasi, kodeUser, kodeKamar, tglCheckin, jumlahMalam):
    if 'nama_user' in session:
        if (request.method == "POST"):
            # Mengambil input form
            hasil = request.form
            kodeReservasi = hasil['kode_reservasi']
            kodeUser = hasil['kode_user']
            kodeKamar = hasil['kode_kamar']
            tglCheckin = hasil['tglCheckin']
            jumlahMalam = hasil['jumlahMalam']
            tglCheckout = hasil['tglCheckout']
            totalBiaya = hasil['totalBiaya']

            # Menghubungkan ke database dan melakukan SELECT pada tabel kamar
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM kamar WHERE kode_kamar="{}"'.format(kodeKamar))
            kamar = cursor.fetchall()
            cursor.close()

            
            if (int(kamar[0][4]) >= 1):
                # Jika kamar tersedia,
                # Memasukan data reservasi ke dalam database
                # Mengurangi jumlah kamar tersedia dalam database
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

        # Menghubungkan ke database dan melakukan SELECT pada tabel kamar
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM kamar WHERE kode_kamar="{}"'.format(kodeKamar))
        kamars = cursor.fetchall()
        cursor.close()
    
        # Mengambil harga kamar per malam dalam database
        hargaMalam = kamars[0][2] # NOTE : Muncul error pada console, tetapi tidak merusak program...
        
        data = [kodeReservasi, kodeUser, kodeKamar, tglCheckin, jumlahMalam, hargaMalam]
        return render_template('admin/reservasi/konfirmasiReservasi.html', container = data)
    
    return redirect('/login')

# HAPUS RESERVASI - ADMIN
# Menghapus reservasi yang ada dalam database
@app.route('/hapusReservasi/<kodeReservasi>', methods=['GET', 'POST'])
def hapusReservasi(kodeReservasi):   
    if 'nama_user' in session:
        if session['status'] == "ADMIN":
            try: 
                # Menghubungkan ke database dan melakukan DELETE pada tabel statuscheck dan reservasi
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
# Melakukan CHECKIN pada kamar yang ada dalam tabel reservasi
@app.route('/checkin/<kodeReservasi>', methods=['GET', 'POST'])
def checkin(kodeReservasi):   
    if 'nama_user' in session:
        if session['status'] == "ADMIN":
            try :
                # Menghubungkan ke database dan mengubah status CHECKIN dalam tabel statuscheck
                cursor = mysql.connection.cursor()
                cursor.execute('UPDATE statuscheck SET isCheckin=%s WHERE kode_reservasi=%s', ("YES", kodeReservasi))
                mysql.connection.commit()

            except (MySQLdb.Error) as err:
                # Menangkap error dan memberikan pesan gagal
                flash('Gagal checkin! %d: %s' % (err.args[0], err.args[1]))

            return redirect('/daftarReservasi')

    return redirect('/login')

# RESERVASI CHECKOUT - ADMIN
# Melakukan CHECKOUT pada kamar yang ada dalam tabel reservasi
@app.route('/checkout/<kodeReservasi>/<kodeKamar>', methods=['GET', 'POST'])
def checkout(kodeReservasi, kodeKamar):   
    if 'nama_user' in session:
        if session['status'] == "ADMIN":
            try:
                # Menghubungkan ke database dan mengubah status CHECKIN dalam tabel statuscheck
                cursor = mysql.connection.cursor()
                cursor.execute('SELECT * FROM kamar WHERE kode_kamar="{}"'.format(kodeKamar))
                kamar = cursor.fetchall()
        
                # Menghubungkan ke database dan mengubah status CHECKOUT dalam tabel statuscheck
                # Juga, Mengembalikan jumlah kamar yang dikurangi saat melakukan konfirmasi reservasi
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
# GENERATE LAPORAN
# ------------------------------------------------------------------------------------------------------------------------------------------------------
# Membuat laporan berdasarkan data reservasi dan mengirim kepada ADMIN untuk di download.
@app.route('/generateLaporan')
def generateLaporan():
    if 'nama_user' in session:
        if session['status'] == "ADMIN":
            try:
                # Menghubungkan ke database dan mengambil data reservasi
                cursor = mysql.connection.cursor()
                cursor.execute('SELECT * FROM reservasi')
                reservasi = cursor.fetchall()
                cursor.close()

                # Me-render HTML 
                rendered = render_template('/admin/laporan/laporan.html', container = reservasi, user = session['nama_user'])
    
                # Mempersiapkan config HTMLtoPDF
                wkhtmltopdf_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
                config = pdfkit.configuration(wkhtmltopdf = wkhtmltopdf_path)
                pdf = pdfkit.from_string(rendered, configuration=config)

                # Convert halaman HTML menjadi PDF dan mengirim ke ADMIN untuk di download
                response = make_response(pdf)
                response.headers['Content-Type'] = 'application/pdf'
                response.headers['Content-Disposition'] = 'attachment; filename = "Laporan Reservasi.pdf"'
                return response
            
            except (MySQLdb.Error) as err:
                # Menangkap error dan memberikan pesan gagal
                flash('Gagal men-generate Laporan! %d: %s' % (err.args[0], err.args[1]))
                return redirect('/home')
    
    return redirect('/login')

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# BLAST EMAIL
# ------------------------------------------------------------------------------------------------------------------------------------------------------
# Menampilkan form yang dapat digunakan untuk mengirim email ke user yang dipilih
@app.route('/sendEmail/<emailPenerima>', methods=['GET', 'POST'])
def sendEmail(emailPenerima):
    if 'nama_user' in session:
        if session['status'] == "ADMIN":
            if (request.method == 'POST'):
                # Mengambil input form
                data = request.form
                subject = data['subject']
                sender = data['sender']
                isiPesan = data['isiPesan']

                try :
                    # Mencoba mengirim email kepada penerima yang dipilih
                    namaHotel = sender
                    msg = Message(subject, sender = (namaHotel, app.config['MAIL_USERNAME']), recipients = [emailPenerima])
                    msg.body = isiPesan
                    mail.send(msg)

                    # jika berhasil mengirim email, memberikan pesan berhasil
                    flash('Email berhasil dikirim!')
                    return redirect('/daftarUser')
                except:
                    # jika gagal mengirim email, memberikan pesan gagal
                    flash('Email gagal dikirim!')
                    return redirect('/daftarUser')
            
            return render_template('/admin/email/sendEmail.html', container = emailPenerima)
        
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
                flash('Gagal melakukan Login! %d: %s' % (err.args[0], err.args[1]))
                return redirect('/login')
            
        if (len(hasil) > 0):
            # Apabila terdapat data username dan password, verifikasi berhasil
            # Menyimpan data user (nama, status, dan kode) ke dalam session
            session.permanent = True
            session['kode_user'] = hasil[0][0]
            session['nama_user'] = hasil[0][1]
            session['status'] = hasil[0][5]
        
            # Verifikasi berhasil, mengirim pesan berhasil login
            flash('Login Berhasil! Welcome %s!' % hasil[0][1])
            return redirect('/login')
        else:
            # Apabila tidak ada data username dan password, verfikasi gagal
            flash('Email atau Password salah!')
            return render_template('login.html')
    
    else:
        if 'nama_user' in session:
            return redirect('/home')

    return render_template('login.html')

# REGISTER - CLIENT
# Digunakan untuk melakukan register agar dapat melakukan reservasi kamar.
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
# Keluar dari akun yang masuk ke dalam website
# Membersihkan data - data yang tersimpan dalam session
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