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

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import pyheif

import sys
sys.path.append("ml-depth-pro/src")  # Pastikan ini menunjuk ke root package "depthpro"

from depthpro import depth_pro, utils


# ## 2. Pendefinisian Fungsi 

# ### 2.1 YOLO : Fitur Panjang Pixel dan Titik Tengah Objek

# In[ ]:

def deteksiPerson(image_path, threshold=0.9, visualize=False):
    # Load image
    image = Image.open(image_path).convert("RGB")

    # Load model dan processor
    model = YolosForObjectDetection.from_pretrained('hustvl/yolos-tiny')
    processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")

    # Preprocess image
    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)

    # Post-process
    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(
        outputs, threshold=threshold, target_sizes=target_sizes
    )[0]

    # Inisialisasi hasil
    person_data = []

    # Siapkan gambar untuk visualisasi jika diminta
    if visualize:
        image_draw = image.copy()
        draw = ImageDraw.Draw(image_draw)

    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        if label.item() == 1:  # Label ID 1 = person (COCO)
            box = [round(coord, 2) for coord in box.tolist()]
            x_min, y_min, x_max, y_max = box

            width = x_max - x_min
            height = y_max - y_min
            center_x = (x_min + x_max) / 2
            center_y = (y_min + y_max) / 2

            person_data.append({
                "center": (center_x, center_y),
                "width": width,
                "height": height
            })

            # Gambar bounding box
            if visualize:
                draw.rectangle([x_min, y_min, x_max, y_max], outline="red", width=3)
                draw.text((x_min, y_min - 10), f"Person {score:.2f}", fill="red")

    # Tampilkan gambar jika diminta
    if visualize:
        image_draw.show()

    return person_data

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
        plt.show()
    # Hapus path setelah selesai digunakan
    if "ml-depth-pro/src" in sys.path:
        sys.path.remove("ml-depth-pro/src")

    return depth_value, focallength_px


# ### 2.3 Exif : Fitur Metadata Citra

# In[ ]:


def ekstrakMetadataCitra(image_path):
    try:
        ext = os.path.splitext(image_path)[1].lower()
        
        if ext == ".heic":
            heif_file = pyheif.read(image_path)
            metadata = {}

            # Cek apakah ada metadata
            if heif_file.metadata:
                for item in heif_file.metadata:
                    metadata[item['type']] = item['data']
                return metadata
            else:
                return {"Warning": "Tidak ada metadata ditemukan dalam file HEIC."}
        
        else:
            image = Image.open(image_path)
            exif_data = image._getexif()

            if not exif_data:
                return {"Warning": "Tidak ada data EXIF ditemukan."}

            metadata = {}
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag == "GPSInfo":
                    gps_data = {}
                    for t in value:
                        sub_tag = GPSTAGS.get(t, t)
                        gps_data[sub_tag] = value[t]
                    metadata["GPSInfo"] = gps_data
                else:
                    metadata[tag] = value

            return metadata

    except Exception as e:
        return {"Error": str(e)}


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

    # Simpan kembali ke variabel img_path jika ingin menimpa file
    img.save(img_path)
    return img

# ## 3. Main Program

# In[ ]:

def ekstraksiFitur(img_path, visualize):
    metadata = ekstrakMetadataCitra(img_path)
    img = ubahUkuran(img_path)
    dataObjek = deteksiPerson(img_path, visualize=visualize)
    kedalamanObjek, focal_length_px = kedalamanCitra(img_path, dataObjek[0]['center'], visualize=visualize)
    return dataObjek, kedalamanObjek, metadata, focal_length_px