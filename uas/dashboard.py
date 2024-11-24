import streamlit as st
import torch
import torch.nn as nn
import torchvision.models as models
from torchvision import transforms
from PIL import Image
import json
import time
import base64

def add_background(image_path):
    with open(image_path, "rb") as img_file:
        b64_image = base64.b64encode(img_file.read()).decode()
    bg_style = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpeg;base64,{b64_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(bg_style, unsafe_allow_html=True)

image_path = r"./assets/40944.png"

# Tambahkan background
add_background(image_path)


# Fungsi untuk memuat file CSS
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# Label mapping
label_mapping = {
    0: "adas", 1: "andaliman", 2: "asam jawa", 3: "bawang bombai", 4: "bawang merah",
    5: "bawang putih", 6: "biji ketumbar", 7: "bunga lawang", 8: "cengkeh", 9: "daun jeruk",
    10: "daun kemangi", 11: "daun ketumbar", 12: "daun salam", 13: "jahe", 14: "jinten",
    15: "kapulaga", 16: "kayu manis", 17: "kayu secang", 18: "kemiri", 19: "kemukus",
    20: "kencur", 21: "kluwek", 22: "kunyit", 23: "lada", 24: "lengkuas", 25: "pala",
    26: "saffron", 27: "serai", 28: "vanili", 29: "wijen"
}

# Fungsi untuk memuat model
@st.cache_resource
def load_model():
    num_classes = len(label_mapping)
    model = models.resnet18(pretrained=True)
    model.fc = nn.Sequential(
        nn.Dropout(0.5),
        nn.Linear(model.fc.in_features, num_classes)
    )
    model.load_state_dict(torch.load('model.pth', map_location=torch.device('cpu')))
    model.eval()
    return model

# Fungsi untuk memuat informasi bumbu
@st.cache_data
def load_bumbu_info():
    with open("info.json", "r") as file:
        return json.load(file)

# Definisikan transformasi gambar
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Fungsi untuk melakukan prediksi
def predict(image, model, transform):
    image = transform(image).unsqueeze(0)  # Tambahkan batch dimension
    with torch.no_grad():
        outputs = model(image)
        probabilities = torch.softmax(outputs, dim=1)
        confidence, predicted = probabilities.max(1)
    predicted_label = predicted.item()
    return predicted_label, confidence.item() * 100

# Sidebar navigation
st.sidebar.title("Navigasi")
st.sidebar.markdown("""
    <div style="background-color:#FFF7D1; padding:10px; border-radius:5px; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);">
        <h3>Selamat Datang!</h3>
        <p>Pilih halaman berikut untuk menjelajahi aplikasi:</p>
    </div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio("Pilih halaman", ["Beranda", "Klasifikasi", "Tentang"])

if menu == "Beranda":
    # Halaman Beranda

    st.markdown("""
        <div class="content">
            <div class="title">
                Aplikasi Deteksi Rempah Indonesia
            </div>
        </div>
    """,
    unsafe_allow_html=True,)

    st.markdown("""
        <div class="content">
            <div class="write">
                Halo-halo, selamat datang di aplikasi deteksi rempah Indonesia ini
            </div>
            <div class="write">
                Anda punya rempah, tapi tidak tahu bagaimana cara memanfaatkannya? Atau Anda sekedar iseng saja ingin tahu? Kebetulan sekali tuh, aplikasi ini bisa membantu anda mendeteksi rempah tersebut. Cukup dengan memotret rempah yang anda punya, kemudian upload ke sini. Aplikasi ini akan membantu anda mengetahui rempah apa itu, dan bagaimana penggunaannya. 
            </div>  
        </div>
    """,
    unsafe_allow_html=True,)

    st.markdown("""
        <div class="content">
            <div class="subheader">
                💡 Bagaimana cara pakainya?
            </div>
            <div class="write">
                <ol>
                    <li> Siapkan foto dari rempah yang anda ingin ketahui dengan format JPG atau PNG </li>
                    <li> Upload foto tersebut di tempat yang telah disediakan </li>
                    <li> Tunggu aplikasi menganalisis foto tersebut, hasil akan segera diketahui tidak lama kemudian </li>
                </ol>
            </div>  
        </div>
    """,
    unsafe_allow_html=True,)
    
    st.markdown("""
        <div class="content">
            <div class="subheader">
                📋 Jenis rempah apa yang bisa dideteksi?
            </div>
            <div class="write">
                Saat ini, model hanya dilatih untuk mendeteksi rempah-rempah yang sering digunakan dalam masakan Indonesia, sehingga untuk rempah-rempah yang digunakan untuk masakan luar negeri dan jarang digunakan di Indonesia, model belum bisa mendeteksinya (daftar lengkap silahkan lihat di halaman “tentang”)
            </div>  
        </div>
    """,
    unsafe_allow_html=True,)


elif menu == "Klasifikasi":
    # Halaman Klasifikasi
    st.markdown("""
        <div class="content">
            <div class="title">
                🔍 Potret rempah Anda di sini
            </div>  
        </div>
    """,
    unsafe_allow_html=True,)

    st.markdown("""
        <div class="content">
            <div class="subheader">
                Sebelum anda menggunakan app ini, mohon untuk memperhatikan hal-hal berikut
            </div>
            <div class="write">
                <ol>
                    <li>Gunakan foto berformat JPG/JPEG/PNG agar dapat terbaca dengan baik</li>
                    <li>Model mungkin akan mengenali benda random sebagai rempah, jadi mohon untuk mengupload foto rempah saja</li>
                    <li>Saat ini, model hanya mengenali rempah-rempah yang digunakan di masakan Indonesia</li>
                </ol>
            </div>  
        </div>
    """,
    unsafe_allow_html=True,)
    
    uploaded_file = st.file_uploader("Upload file anda di sini", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        try:
            # Baca file gambar
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, caption="Gambar yang diunggah", use_container_width=True)
            
            # Load model
            model = load_model()

            # Load informasi bumbu
            bumbu_info = load_bumbu_info()
            st.markdown("""
                <div class="content">
                    <div class="write">
                        Memulai proses analisis...
                    </div>
                </div>
            """,
                unsafe_allow_html=True,)
            latest_iteration = st.empty()
            bar = st.progress(0)

            for i in range(100):
                latest_iteration.text(f'Progres: {i + 1}%')
                bar.progress(i + 1)
                time.sleep(0.05)
                
            with st.spinner(text="""Sedang memproses file anda
                                Mohon tunggu sebentar"""):
                time.sleep(2)

            # Prediksi
            label_idx, confidence = predict(image, model, transform)
            label = list(bumbu_info.keys())[label_idx]
            st.success(f"Hasil analisis : **{label.capitalize()}** ({confidence:.2f}%)")

            # Tampilkan deskripsi
            if label in bumbu_info:
                info = bumbu_info[label]
                st.markdown(f"""
                    <div class="content">
                        <div class="subheader">
                            📖 Tentang {label.capitalize()}
                        </div>
                        <div class="write">
                            {info.get("description", "Deskripsi tidak tersedia.")}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                    <div class="content">
                        <div class="subheader">
                            💡 Tips dalam memanfaatkan {label.capitalize()}
                        </div>
                        <div class="write">
                            {info.get("notes", "Tips tidak tersedia.")}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                    <div class="content">
                        <div class="subheader">
                            📖 Catatan tambahan
                        </div>
                        <div class="write">
                            {info.get("diff", "Tidak ada.")}
                        </div>
                    </div>
                """, unsafe_allow_html=True)


        except Exception as e:
            st.markdown(f"""
                <div class="error-message">
                    Terjadi kesalahan: {str(e)}
                </div>
            """, unsafe_allow_html=True)

elif menu == "Tentang":
    st.markdown("""
        <div class="content">
            <div class="title">
                ℹ️ Tentang Aplikasi
            </div>
        </div>
    """,
    unsafe_allow_html=True)
    
    st.markdown("""
        <div class="content">
            <div class="subheader">
                Daftar rempah yang dapat dikenali
            </div>
            <div class="write">
                <ul>
                    <li>Adas</li>
                    <li>Andaliman</li>
                    <li>Asam Jawa</li>
                    <li>Bawang Bombay</li>
                    <li>Bawang Merah</li>
                    <li>Bawang Putih</li>
                    <li>Biji Ketumbar</li>
                    <li>Bunga Lawang</li>
                    <li>Cengkeh</li>
                    <li>Daun Jeruk</li>
                    <li>Daun Kemangi</li>
                    <li>Daun Ketumbar</li>
                    <li>Daun Salam</li>
                    <li>Jahe</li>
                    <li>Jinten</li>
                    <li>Kapulaga</li>
                    <li>Kayu Manis</li>
                    <li>Kayu Secang</li>
                    <li>Kemiri</li>
                    <li>Kemukus</li>
                    <li>Kencur</li>
                    <li>Kluwek</li>
                    <li>Kunyit</li>
                    <li>Lada</li>
                    <li>Lengkuas</li>
                    <li>Pala</li>
                    <li>Saffron</li>
                    <li>Serai</li>
                    <li>Vanili</li>
                    <li>Wijen</li>
                </ul>
            </div>
        <div>
    """,
    unsafe_allow_html=True)

    st.markdown("""
        <div class="content">
            <div class="subheader">
                🛠 Teknologi yang digunakan dalam membangun aplikasi ini
            </div>
            <div class="write">
                <ul>
                    <li>Framework aplikasi : Streamlit 1.40.0</li>
                    <li>Framework pelatihan model : PyTorch cuda 12.4</li>
                    <li>Bahasa pemrograman : Python 3.12.5</li>
                </ul>
            </div>
        </div>
    """,
    unsafe_allow_html=True)
    
    st.markdown("""
        <div class="content">
            <div class="subheader">
                Catatan pengembang
            </div>
            <div class="write">
                Model mungkin masih perlu pengembangan lebih jauh lagi, dikarenakan keterbatasan rempah yang bisa dideteksi. Selain itu, beberapa rempah dengan penampilan visual mirip masih akan membingungkan model, sehingga Anda mungkin memerlukan info tambahan agar bisa membedakannya dengan benar dikarenakan adanya peluang model salah mengenali rempah yang mirip secara visual tersebut.
            </div>
        </div>
    """,
    unsafe_allow_html=True)