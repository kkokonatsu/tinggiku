from flask import Flask, render_template

# Inisialisasi aplikasi Flask
# 'static_folder' dan 'template_folder' memberi tahu Flask di mana menemukan file frontend Anda.
app = Flask(__name__, static_folder='static', template_folder='templates')

# --- Rute Halaman Utama ---
# Ketika pengguna mengakses alamat dasar website Anda (misalnya, http://127.0.0.1:5000/)
@app.route('/')
def index():
    # Flask akan mencari file 'index.html' di dalam folder 'templates/'
    return render_template('index.html')

# --- Bagian untuk Menjalankan Aplikasi ---
# Ini memastikan aplikasi hanya berjalan ketika file ini dieksekusi secara langsung
if __name__ == '__main__':
    # Aktifkan mode debug untuk pengembangan (akan otomatis me-reload server saat kode berubah)
    app.run(debug=True)