# src/services/inference_service.py

import pandas as pd
import joblib
import os
from PIL.Image import open as open_image

# Import semua fungsi yang dibutuhkan dari FeatureExtraction.py
# Perhatikan path relatif. Karena inference_service.py ada di src/services/,
# dan FeatureExtraction.py ada di src/utils/, kita perlu '..utils.FeatureExtraction'
from ..utils.FeatureExtraction import ekstraksiFitur

# Ini penting untuk HEIF agar PIL.Image.open bisa membaca .heif
from pillow_heif import register_heif_opener
register_heif_opener()

# Path ke model RandomForest Anda
# Perhatikan path relatif dari src/services/ ke models/
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../models/ModelPrediksiTinggiku/model_randomforest.pkl')


def perform_inference(img_path: str, visualize: bool = False):
    """
    Melakukan inferensi prediksi tinggi berdasarkan fitur yang diekstrak dari gambar.

    Args:
        img_path (str): Path lengkap ke gambar input.
        visualize (bool): Jika True, akan menampilkan visualisasi dari proses ekstraksi fitur (mode debug/dev).

    Returns:
        float: Hasil prediksi tinggi, atau None jika terjadi error.
    """
    print(f"Memulai ekstraksi fitur untuk gambar: {os.path.basename(img_path)}")

    # ====================================================================
    # DUMMY DATA HASIL EKSTRAKSI FITUR
    # ====================================================================
    TinggiBB = 3034.5
    kedalamanObjek = 1.5962492227554321
    focal_length_px = 2779.943164886649
    ApertureValue = 1.6959938128383605
    BrightnessValue = 3.672446894159906
    # ====================================================================

    # Panggil fungsi ekstraksiFitur
    # try:
    #     dataObjek, kedalamanObjek, metadata, focal_length_px = ekstraksiFitur(img_path, visualize)
    # except ValueError as e:
    #     print(f"Error ekstraksi fitur: {e}")
    #     return None
    # except Exception as e:
    #     print(f"Terjadi error tak terduga saat ekstraksi fitur: {e}")
    #     return None

    # # Ekstrak nilai yang dibutuhkan dari hasil ekstraksi fitur
    # if not dataObjek or not dataObjek[0] or 'TinggiBB' not in dataObjek[0]:
    #     print("Error: TinggiBB tidak ditemukan di data objek yang terdeteksi.")
    #     return None
    # TinggiBB = dataObjek[0]['TinggiBB']

    # Asumsi nama key di metadata sesuai dengan yang dibutuhkan model
    # Gunakan .get() dengan nilai default untuk keamanan
    ApertureValue = metadata.get('ApertureValue', 1.648637324)
    BrightnessValue = metadata.get('BrightnessValue', 2.186689273)

    # Validasi: jika kedalamanObjek < 1, ubah jadi 1.5
    if kedalamanObjek < 1:
        print(f"Warning: kedalamanObjek terlalu kecil ({kedalamanObjek:.2f}), diset menjadi 1.5")
        kedalamanObjek = 1.5

    # Hitung rasio
    if focal_length_px == 0:
        print("Error: Focal length dalam piksel adalah nol. Tidak dapat menghitung rasio.")
        return None

    rasioDepth_flpx = kedalamanObjek / focal_length_px
    rasioTBB_flpx = TinggiBB / focal_length_px

    # Susun input sebagai DataFrame sesuai urutan dan nama fitur model
    data = pd.DataFrame([{
        'rasioTBB_flpx': rasioTBB_flpx,
        'rasioDepth_flpx': rasioDepth_flpx,
        'TinggiBB': TinggiBB,
        'kedalamanObjek': kedalamanObjek,
        'fl_px': focal_length_px,
        'ApertureValue': ApertureValue,
        'BrightnessValue': BrightnessValue
    }])

    # Load model dan prediksi
    try:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model tidak ditemukan di path: {MODEL_PATH}")

        model = joblib.load(MODEL_PATH)
        prediction = model.predict(data)
        print(f"Hasil prediksi: {prediction[0]:.2f} meter")
        return prediction[0]
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Pastikan file model 'model_randomforest.pkl' ada di lokasi yang benar.")
        return None
    except Exception as e:
        print(f"Terjadi error saat memuat atau memprediksi dengan model: {e}")
        return None
    
    # print(f"File gambar berhasil diunggah ke: {img_path}")
    # print(f"Parameter visualize: {visualize}")

    # import random
    # simulated_height = round(random.uniform(1.50, 1.90), 2) # Tinggi antara 1.50m - 1.90m

    # print(f"Simulasi hasil prediksi: {simulated_height:.2f} meter")
    # return simulated_height