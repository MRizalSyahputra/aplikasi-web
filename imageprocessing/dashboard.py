import streamlit as st
from PIL import Image, ImageOps
import numpy as np
from tensorflow.keras.models import load_model

# Memuat model yang sudah dilatih
model = load_model('D:/eksperimen/appweb/code/imageprocessing/trainmodel.keras')

# Judul aplikasi
st.title("Program Deteksi Bahasa Isyarat (ASL - American Sign Language)")

st.text("Silakan upload gambar Anda")

# Daftar kelas 0-9 dan a-z
class_indices = list("0123456789abcdefghijklmnopqrstuvwxyz")

# Fungsi untuk memproses gambar agar sesuai dengan input model
def preprocess_image(image):
    size = (400, 400)  # Sesuaikan dengan input model kamu
    image = ImageOps.fit(image, size, Image.LANCZOS)  # Resize gambar
    image = np.array(image) / 255.0  # Normalisasi pixel ke rentang [0, 1]
    image = np.expand_dims(image, axis=0)  # Tambahkan batch dimension
    return image

# Upload file gambar
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png"])

if uploaded_file is not None:
    # Tampilkan gambar yang diupload
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Preprocessing dan prediksi
    processed_image = preprocess_image(image)
    prediction = model.predict(processed_image)  # Prediksi dengan model

    # Ambil kelas dengan probabilitas tertinggi
    predicted_class = class_indices[np.argmax(prediction)]

    # Tampilkan hasil prediksi
    st.write(f"Prediksi: {predicted_class}")
