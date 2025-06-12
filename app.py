from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import sys
import uuid 
from werkzeug.utils import secure_filename 
from PIL import Image 

project_root = os.path.dirname(os.path.abspath(__file__))
depthpro_src_path = os.path.join(project_root, 'notebooks', 'ml-depth-pro', 'src')
sys.path.insert(0, depthpro_src_path)

from src.services.inference_service import perform_inference

# Inisialisasi aplikasi Flask
app = Flask(__name__, static_folder='static', template_folder='templates')

# --- Konfigurasi Folder Unggahan ---
# Folder tempat menyimpan gambar yang diunggah sementara
UPLOAD_FOLDER = 'uploads'
# Buat folder jika belum ada
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Batasi jenis file yang diizinkan (sesuaikan dengan yang bisa diproses oleh FeatureExtraction)
# Tambahkan 'heif' dan 'heic' jika Anda menggunakan pillow-heif untuk mendukungnya
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'heif', 'heic'} 

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Rute Halaman Utama ---
# Ketika pengguna mengakses alamat dasar website Anda (misalnya, http://127.0.0.1:5000/)
@app.route('/')
def index():
    # Flask akan mencari file 'index.html' di dalam folder 'templates/'
    return render_template('index.html')

# --- Rute Prediksi ---
# Ketika ada permintaan POST ke /predict (misalnya dari form HTML atau AJAX)
@app.route('/predict', methods=['POST'])
def predict_height():
    # Cek apakah ada file di request
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files['image']

    # Jika user tidak memilih file, browser juga mengirimkan empty part tanpa filename
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        # Amankan nama file dan buat nama unik untuk menghindari konflik
        filename = secure_filename(file.filename)
        unique_filename = str(uuid.uuid4()) + "_" + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        try:
            # Simpan file yang diunggah sementara
            # Gunakan PIL untuk membuka dan menyimpan kembali gambar.
            # Ini membantu menangani berbagai format, termasuk HEIF/HEIC jika pillow-heif sudah terdaftar.
            img = Image.open(file.stream)
            img.save(filepath)
            
            # Ambil parameter visualize dari query string (opsional, default False)
            # Misalnya: /predict?visualize=true
            visualize_param = request.args.get('visualize', 'false').lower()
            visualize = visualize_param == 'true'

            # Panggil service inferensi yang sudah Anda buat
            predicted_height = perform_inference(filepath, visualize=visualize)

            # Hapus gambar sementara setelah inferensi selesai
            os.remove(filepath)

            if predicted_height is not None:
                return jsonify({"predicted_height_meters": predicted_height}), 200
            else:
                return jsonify({"error": "Failed to perform inference. Check server logs for details."}), 500
        except Exception as e:
            # Jika ada error saat memproses atau menyimpan gambar, hapus file yang mungkin sudah tersimpan
            if os.path.exists(filepath):
                os.remove(filepath)
            print(f"Error during image processing or inference: {e}") # Log error untuk debugging
            return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
    else:
        return jsonify({"error": f"Allowed image types are {', '.join(ALLOWED_EXTENSIONS)}"}), 400

# --- Opsional: Rute untuk Melayani File Visualisasi ---
# Jika `visualize=true` dan fungsi Anda menyimpan output visualisasi ke folder seperti 'Hasil_YOLO' atau 'Hasil DepthPro',
# Anda mungkin ingin melayani file-file tersebut. Sesuaikan path folder.
@app.route('/visualizations/<filename>')
def serve_visualization(filename):
    # Asumsi hasil visualisasi YOLO disimpan di 'Hasil_YOLO'
    # Jika Anda memiliki beberapa folder visualisasi, Anda perlu logika lebih lanjut
    # untuk menentukan dari mana file harus dilayani.
    vis_folder = 'Hasil_YOLO' # Atau 'Hasil DepthPro'
    if not os.path.exists(vis_folder):
        os.makedirs(vis_folder) # Pastikan folder ini ada
    return send_from_directory(vis_folder, filename)


# --- Bagian untuk Menjalankan Aplikasi ---
if __name__ == '__main__':
    # Aktifkan mode debug untuk pengembangan (akan otomatis me-reload server saat kode berubah)
    # Untuk produksi, ini harus False dan gunakan server WSGI seperti Gunicorn/Waitress.
    app.run(debug=True, host='0.0.0.0', port=5000)