# Cara Run Project di Local (PENTING)

**Table of Contents**

1. [Initial Run](#initial-run-1)
2. [Run Biasa](#run-biasa-2)
3. [Add-Commit-Push](#add-commit--push-3)

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
source env/bin/activate
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

```git
# push pertama kali
git push -u origin main

# push kedua, ketiga, dst.
git push
```
