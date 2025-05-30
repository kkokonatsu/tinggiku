# Tinggiku: Pengukur Tinggi Badan berbasis Foto

## Struktur Proyek

```
tinggiku/
├── app.py
├── requirements.txt
├── .flaskenv
├── .gitignore
├── static/
├── templates/
├── models/
├── data/
├── src/
└── notebooks/
```

### app.py

File ini berisi kode utama yang menginisialisasi aplikasi Flask, mendefinisikan rute atau endpoint web (misalnya, apa yang terjadi ketika seseorang membuka http://127.0.0.1:5000/ atau mengunggah gambar ke /process-image), dan bertindak sebagai "orkestrator" yang memanggil logika bisnis dari modul-modul lain di folder src/.

### requirements.txt

File ini adalah daftar resep untuk semua library Python yang dibutuhkan proyek Anda. Ketika Anda atau pengembang lain menjalankan pip install -r requirements.txt, Python akan menginstal semua dependensi yang tercantum (seperti Flask, PyTorch, ONNX Runtime, Pillow, dll.) dengan versi yang spesifik. Ini memastikan setiap orang yang mengerjakan proyek menggunakan versi library yang sama persis, mencegah masalah "berfungsi di komputer saya tapi tidak di komputer Anda".

### .flaskenv

Ini adalah file konfigurasi kecil untuk variabel lingkungan Flask. File ini memberitahu perintah flask (seperti flask run) di mana menemukan aplikasi Flask Anda (yaitu, app.py). Dengan .flaskenv, Anda tidak perlu mengatur FLASK_APP=app.py secara manual setiap kali memulai sesi terminal baru.

### .gitignore

File ini adalah daftar abaian untuk Git. .gitignore memberi tahu Git file atau folder mana yang tidak boleh dilacak atau di-commit ke repositori. Ini penting untuk mengabaikan folder besar seperti env/ (virtual environment Python) dan node_modules/ (dependensi JavaScript/Node.js) serta file yang dihasilkan otomatis (seperti **pycache**/ dan static/css/output.css). Ini menjaga ukuran repositori tetap kecil dan rapi.

### static/

Folder ini menampung semua aset frontend statis Anda. Ini termasuk:

- **css:** File styling (seperti style.css atau output.css dari Tailwind) yang menentukan tampilan aplikasi Anda.
- **js:** File skrip (script.js) yang membuat halaman web interaktif (misalnya, menangani unggah gambar, menampilkan hasil).
- **img:** Gambar-gambar kecil atau ikon yang digunakan di antarmuka pengguna. Flask akan melayani file-file ini langsung ke browser pengguna.

### templates/

Folder ini berisi file HTML yang akan disajikan oleh Flask. Biasanya, ini adalah halaman utama aplikasi Anda (seperti `index.html`).

### models/

Ini adalah tempat Anda menyimpan file-file model Deep Learning yang sudah terlatih. Dalam kasus "Tinggiku", ini akan menjadi file model YOLOS dan MiDaS/DPT yang sudah Anda ekspor ke format yang optimal untuk inferensi di CPU (misalnya, .onnx). Model-model ini akan dimuat ke memori server saat aplikasi dimulai.

### data/

Folder ini digunakan untuk menyimpan data statis atau data lookup yang tidak memerlukan database eksternal. Untuk proyek "Tinggiku", ini akan menampung file camera_sensors.json yang berisi informasi ukuran sensor kamera untuk berbagai model. Data ini akan dibaca oleh aplikasi Python saat startup.

### src/

Ini adalah jantung logika bisnis Anda yang lebih terstruktur. Folder `src/` (singkatan dari source) adalah tempat Anda akan memisahkan kode Python utama Anda menjadi modul-modul yang lebih kecil dan terorganisir. Pendekatan ini membantu menjaga app.py tetap ringkas dan membuat proyek lebih modular dan mudah dikelola. Di dalamnya biasanya ada sub-folder:

- `services/` (untuk logika bisnis utama)
- `utils/` (untuk fungsi pembantu).

### notebooks/

Folder ini didedikasikan untuk file Jupyter Notebook (.ipynb) Anda. Notebook sangat berguna untuk eksperimen, analisis data, pelatihan model awal, atau pengujian bagian-bagian kecil dari logika Deep Learning Anda secara iteratif, sebelum mengintegrasikannya ke dalam kode aplikasi Flask utama. Menjaga notebook terpisah membantu membedakan kode eksperimental dari kode produksi.

# Cara Run Project di Local (PENTING)

**Table of Contents**

1. [Initial Run](#initial-run-1)
2. [Run Biasa](#run-biasa-2)
3. [Add-Commit-Push](#add-commit--push-3)

---

## NOTES!

- Jangan lupa selalu `git pull` tiap mau mulai ngedit file
- Sebelum `git push` jangan lupa untuk edit **`requirements.txt`** setiap ada penambahan atau perubahan _library/package_ yang dipake
- Jangan lupa untuk `git push` setiap suatu fitur selesai dibuat

---

## Initial Run (1)

INGET, INI UNTUK **RUN PROJECT PERTAMA KALI** ATAU BELUM PERNAH ADA FILE PROYEK TINGGIKU SAMSEK ALIAS DARI AWAL!!

Ini akan mengunduh seluruh kode proyek Anda dari Git ke komputer lokal Anda.

1. Buka Command Prompt atau GitBash.
2. Navigasikan ke lokasi di mana Anda ingin menyimpan proyek Anda. Contoh:

```shell
cd C:\Users\NamaAnda\Documents\
```

3. Gunakan perintah git clone diikuti dengan URL repository Git Anda.

```shell
git clone https://github.com/kkokonatsu/tinggiku.git
```

4. Masuk ke Direktori Proyek:

```shell
cd tinggiku
```

5. Buat Virtual Environment: Ini mengisolasi dependensi proyek Anda.

```shell
python -m venv env
```

6. Aktifkan Virtual Environment:

```shell
# cara 1
.\env\Scripts\activate

# cara 2
source env/bin/activate
```

7. Instal Dependensi: Ini akan mengunduh dan menginstal semua library Python yang dibutuhkan proyek Anda berdasarkan file `requirements.txt`

```shell
pip install -r requirements.txt
```

7. Buat file Konfigurasi Flask dengan nama `.flaskenv` di root direktori **tinggiku**. Kemudian, isi dengan tulisan berikut:

```python
FLASK_APP=app.py
```

8. Dari CMD/Bash terakhir yang nyangkut di path proyek, Jalankan Aplikasi Flask:

```shell
flask run
```

<br>

**JANGAN LUPA UNTUK SELALU GIT PUSH SETIAP ADA PERUBAHAN!!**

---

## Run Biasa (2)

INGET, INI KALO UDH ADA FILE PROYEK TINGGIKU DAN SELALU MULAI DARI GIT PULL SETIAP MAU NGUBAH KODINGAN OKEY!!

1. Masuk ke Direktori Proyek Anda:

```shell
cd ../tinggiku
```

2. Aktifkan Virtual Environment Anda: Ini penting agar semua operasi pip dan flask menggunakan lingkungan yang benar.

```shell
# cara 1
.\env\Scripts\activate

# cara 2
source env/Scripts/activate
```

3. Tarik Perubahan Terbaru (Pull Changes): Ini akan mengunduh perubahan terbaru dari repository Git.

```shell
git pull origin main
```

4. Perbarui Dependensi (Jika requirements.txt Berubah): Jika ada perubahan pada file requirements.txt (misalnya, ada library baru yang ditambahkan atau versi library yang diperbarui), Anda perlu menginstalnya.

```shell
pip install -r requirements.txt
```

5. Dari CMD/Bash terakhir yang nyangkut di path proyek, Jalankan Aplikasi Flask:

```shell
flask run
```

---

## Add, Commit, & Push (3)

**1. Add**

```git
git add .
```

**2. Commit**

Awali dengan kata kunci yang menunjukkan tipe perubahan, diikuti titik dua dan spasi. Contohnya:

```
git commit -m "feat: tambahkan fitur unggah gambar untuk estimasi tinggi"
```

- `feat`: (feature): Menambahkan fitur baru.
- `fix`: (bug fix): Memperbaiki bug.
- `docs`: (documentation): Perubahan pada dokumentasi.
- `chore`: (chore): Pemeliharaan rutin, tanpa perubahan kode aplikasi atau tes.
- `refactor`: (refactor): Perubahan kode yang tidak mengubah fungsionalitas (misalnya, merestrukturisasi kode).
- `test`: (test): Menambahkan atau memperbaiki tes.
- `perf`: (performance): Peningkatan kinerja kode.
- `style`: (style): Perubahan gaya kode (formatting, titik koma, dll.).

**3. Push**

**Sebelum ngepush pastiin ada file `.gitignore` dan ada isinya! samain isinya kyk yg di [repository git tinggiku](https://github.com/kkokonatsu/tinggiku/blob/main/.gitignore).**

```git
# push pertama kali
git push -u origin main

# push kedua, ketiga, dst.
git push
```

---

```
Thanks :) semangat ngodingnya!
```
