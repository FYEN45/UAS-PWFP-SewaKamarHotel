# Harus di Download
- Code Editor (Bebas)
- GitHub (opsional)
- XAMPP
- Python
- wkHTMLtoPDF (64 BIT) ``https://wkhtmltopdf.org/downloads.html``

# Cara untuk mempersiapkan dan menjalankan project
- Pull dari github / download project
- Pindah ke directory project                                   ``[$ cd ...]``
- Bikin virtual env (jika belum ada),                           ``[$ python -m venv env]``
- Aktifin scripts                                               ``[$ env/Scripts/activate]``
- Donlod smua requirements project (ada dalem requirements.txt) ``[$ pip install -r requirements.txt]``
- Setup project flask                                           ``[$ set NamaProject=app.py]``
- Menjalankan project project                                   ``[$ flask run]`` atau ``[$ python app.py]``

# Database ( Menggunakan XAMPP )
- Dalam folder project ada folder database
- Nyalakan XAMPP ( Apache & MySQL )
- Buka http://localhost/phpmyadmin
- Import file sql ke Database anda

# Login Website
Untuk login website bisa menggunakan,
- email = 'admin@gmail.com'
- password = 'admin123'

Source :
- Pembahasan Import & Export Requirement Virtual Environment
https://stackoverflow.com/questions/14684968/how-to-export-virtualenv
