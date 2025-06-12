#!/usr/bin/env python
# coding: utf-8

# ## 1. Import Library

# In[4]:


import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from transformers import YolosImageProcessor, YolosForObjectDetection, pipeline
from PIL import Image, ImageDraw, ImageFont
import torch
from ultralytics import YOLO
from PIL.ExifTags import TAGS, GPSTAGS
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS, GPSTAGS, IFD
from pillow_heif import register_heif_opener  # HEIF support
import piexif

import sys
sys.path.append("ml-depth-pro/src")  # Pastikan ini menunjuk ke root package "depthpro"

from depthpro import depth_pro, utils


# ## 2. Pendefinisian Fungsi 

# ### 2.1 YOLO : Fitur Panjang Pixel dan Titik Tengah Objek

# In[ ]:


def deteksiPerson(image_path, threshold=0.7, visualize=False):
    # Load model YOLO
    model = YOLO("../models/yolov8n.pt")
    
    # Run inference
    results = model(image_path)[0]

    # Siapkan gambar untuk visualisasi jika diminta
    image = Image.open(image_path).convert("RGB")
    if visualize:
        image_draw = image.copy()
        draw = ImageDraw.Draw(image_draw)

    best_person = None
    best_score = threshold

    for box in results.boxes:
        cls_id = int(box.cls.item())
        score = box.conf.item()
        if cls_id == 0 and score >= best_score:
            x_min, y_min, x_max, y_max = box.xyxy[0].tolist()
            x_min, y_min, x_max, y_max = round(x_min, 2), round(y_min, 2), round(x_max, 2), round(y_max, 2)

            width = x_max - x_min
            height = y_max - y_min
            center_x = (x_min + x_max) / 2
            center_y = (y_min + y_max) / 2

            best_person = {
                "TitikTengah": (center_x, center_y),
                "LebarBB": width,
                "TinggiBB": height,
                "Skor": score
            }

    # Gambar bounding box jika visualisasi diaktifkan
    if visualize and best_person:
        draw.rectangle([
            best_person["TitikTengah"][0] - best_person["LebarBB"]/2,
            best_person["TitikTengah"][1] - best_person["TinggiBB"]/2,
            best_person["TitikTengah"][0] + best_person["LebarBB"]/2,
            best_person["TitikTengah"][1] + best_person["TinggiBB"]/2
        ], outline="red", width=3)
        draw.text((
            best_person["TitikTengah"][0] - best_person["LebarBB"]/2,
            best_person["TitikTengah"][1] - best_person["TinggiBB"]/2 - 10
        ), f"Person {best_person['Skor']:.2f}", fill="red")

        os.makedirs('Hasil_YOLO', exist_ok=True)
        output_filename = os.path.splitext(os.path.basename(image_path))[0] + '_yolo.png'
        output_path = os.path.join('Hasil_YOLO', output_filename)
        image_draw.save(output_path)

    return best_person

# ### 2.2 DepthAnythingV2 : Fitur Kedalaman Absolut Citra pada Titik tertentu

# In[ ]:

def kedalamanCitra(img_path, point_xy, visualize=False):
    """
    Mengembalikan nilai depth dan focal length pada titik (x, y) dari gambar.
    
    Parameters:
        img_path (str): Path ke gambar input.
        point_xy (tuple): Titik (x, y) tempat nilai depth diambil.
        visualize (bool): Jika True, tampilkan visualisasi. Default False.
    
    Returns:
        depth_value (float): Nilai kedalaman (dalam meter) pada titik (x, y).
        focallength_px (float): Nilai focal length dalam piksel.
    """

    # Load model dan transformasi
    model, transform = depth_pro.create_model_and_transforms()
    model.eval()

    # Load dan preprocess gambar
    image, _, f_px = utils.load_rgb(img_path)
    image_tensor = transform(image)

    # Inference
    prediction = model.infer(image_tensor, f_px=f_px)
    depth_map = prediction["depth"]
    focallength_px = prediction["focallength_px"]

    x, y = point_xy
    height, width = depth_map.shape[-2:]

    # Validasi titik
    if not (0 <= x < width and 0 <= y < height):
        raise ValueError(f"Point {point_xy} out of bounds. Image size: {width}x{height}")

    # Ambil nilai depth
    depth_value = depth_map[int(y), int(x)].item()

    # Visualisasi
    if visualize:
        # Buat folder 'Hasil' jika belum ada
        os.makedirs('Hasil DepthPro', exist_ok=True)

        fig, axs = plt.subplots(1, 2, figsize=(12, 5))

        # RGB image
        axs[0].imshow(image)
        axs[0].scatter([x], [y], color='red', label='Titik')
        axs[0].set_title(f"RGB Image\nTitik: ({x}, {y})")
        axs[0].axis('off')

        # Depth map
        axs[1].imshow(depth_map.cpu().numpy(), cmap='viridis')
        axs[1].scatter([x], [y], color='red', label='Titik')
        axs[1].set_title(f"Depth Map\nDepth: {depth_value:.2f} m")
        axs[1].axis('off')

        plt.tight_layout()

        # Simpan gambar ke folder Hasil dengan nama sesuai citra
        output_filename = os.path.splitext(os.path.basename(img_path))[0] + '_hasil.png'
        output_path = os.path.join('Hasil DepthPro', output_filename)
        plt.savefig(output_path)

        plt.close(fig)  # Tutup figure agar tidak tampil di jendela saat batch processing
    # Hapus path setelah selesai digunakan
    if "ml-depth-pro/src" in sys.path:
        sys.path.remove("ml-depth-pro/src")

    return depth_value, focallength_px


# ### 2.3 Exif : Fitur Metadata Citra

# In[ ]:                     

register_heif_opener() 

def ekstrakMetadataCitra(fname: str) -> dict:
    img = Image.open(fname)
    exif = img.getexif()

    metadata = {}

    # Ambil tag dasar
    for k, v in exif.items():
        tag = TAGS.get(k, k)
        metadata[tag] = v

    # Ambil tag tambahan dari setiap IFD
    for ifd_id in IFD:
        try:
            ifd = exif.get_ifd(ifd_id)
            resolve = GPSTAGS if ifd_id == IFD.GPSInfo else TAGS

            for k, v in ifd.items():
                tag = resolve.get(k, k)
                metadata[tag] = v
        except KeyError:
            continue

    return metadata


# ### 2.4 Pendefinisian Fungsi Resize Citra
def ubahUkuran(img_path):
    # Buka gambar
    img = Image.open(img_path)

    # Dapatkan ukuran asli
    width, height = img.size

    # Tentukan tinggi maksimum
    max_height = 750

    # Hitung ulang ukuran jika tinggi melebihi maksimum
    if height > max_height:
        ratio = max_height / height
        new_height = max_height
        new_width = int(width * ratio)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    return img

# ## 3. Main Program

# In[ ]:

def ekstraksiFitur(img_path, visualize):
    metadata = ekstrakMetadataCitra(img_path)
    img = ubahUkuran(img_path)
    dataObjek = deteksiPerson(img_path, visualize=visualize)
    kedalamanObjek, focal_length_px = kedalamanCitra(img_path, dataObjek[0]['TitikTengah'], visualize=visualize)
    return dataObjek, kedalamanObjek, metadata, focal_length_px