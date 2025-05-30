#!/usr/bin/env python
# coding: utf-8

# ## 1. Import Library

# In[4]:


import pandas as pd
import numpy as np
import os

from transformers import YolosImageProcessor, YolosForObjectDetection, pipeline
from PIL import Image, ImageDraw, ImageFont
import torch

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import pyheif


# ## 2. Pendefinisian Fungsi 

# ### 2.1 YOLO : Fitur Panjang Pixel dan Titik Tengah Objek

# In[ ]:


def deteksiPerson(image_path, threshold=0.9):
    # Load image
    image = Image.open(image_path)

    # Load model dan processor
    model = YolosForObjectDetection.from_pretrained('hustvl/yolos-tiny')
    processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")

    # Preprocess image
    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)

    # Post-process
    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs, threshold=threshold, target_sizes=target_sizes)[0]

    # Inisialisasi hasil
    person_data = []

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

    return person_data


# ### 2.2 DepthAnythingV2 : Fitur Kedalaman Absolut Citra pada Titik tertentu

# In[ ]:



def kedalamanCitra(image, point, depth_estimator):
    """
    Mengembalikan nilai kedalaman pada titik tertentu dari citra menggunakan ZoeDepth.
    
    Args:
        image (PIL.Image): Citra input.
        point (tuple): Titik (x, y) pada citra asli.
        
    Returns:
        float: Nilai kedalaman pada titik tersebut, atau None jika titik di luar jangkauan.
    """
    x_orig, y_orig = point

    # Dapatkan ukuran citra asli
    orig_width, orig_height = image.size

    # Validasi titik input
    if x_orig >= orig_width or y_orig >= orig_height or x_orig < 0 or y_orig < 0:
        print("Titik di luar jangkauan gambar asli.")
        return None

    # Inference depth map
    outputs = depth_estimator(image)
    depth_image = outputs['depth']
    depth_array = np.array(depth_image)

    # Ukuran depth map
    depth_width, depth_height = depth_image.size

    # Konversi titik ke skala depth map
    x_depth = int(x_orig * depth_width / orig_width)
    y_depth = int(y_orig * depth_height / orig_height)

    # Validasi titik pada depth map
    if x_depth >= depth_width or y_depth >= depth_height:
        print("Titik di luar jangkauan depth map.")
        return None

    # Ambil nilai kedalaman
    depth_value = float(depth_array[y_depth, x_depth])
    return depth_value


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


# ### 2.4 Pendefinisian Fungsi Convert HEIC to JPG

# ## 3. Main Program

# In[ ]:


def ekstraksiFitur(img_path, depth_estimator):
    dataObjek = deteksiPerson(img_path)
    kedalamanObjek = kedalamanCitra(img_path, dataObjek['center'], depth_estimator)
    metadata = ekstrakMetadataCitra(img_path)
    return dataObjek, kedalamanObjek, metadata

