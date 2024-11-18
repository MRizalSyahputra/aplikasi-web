import streamlit as st
import torch
import torch.nn as nn
import torchvision.models as models
from torchvision import transforms
from PIL import Image
import json

# Label mapping
label_mapping = {
    0: "adas",
    1: "andaliman",
    2: "asam jawa",
    3: "bawang bombai",
    4: "bawang merah",
    5: "bawang putih",
    6: "biji ketumbar",
    7: "bunga lawang",
    8: "cengkeh",
    9: "daun jeruk",
    10: "daun kemangi",
    11: "daun ketumbar",
    12: "daun salam",
    13: "jahe",
    14: "jinten",
    15: "kapulaga",
    16: "kayu manis",
    17: "kayu secang",
    18: "kemiri",
    19: "kemukus",
    20: "kencur",
    21: "kluwek",
    22: "kunyit",
    23: "lada",
    24: "lengkuas",
    25: "pala",
    26: "saffron",
    27: "serai",
    28: "vanili",
    29: "wijen"
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
        _, predicted = outputs.max(1)
    predicted_label = predicted.item()
    return label_mapping.get(predicted_label, "Label tidak dikenal")

# Streamlit App
st.title("Aplikasi Deteksi Bumbu Masak")

st.write("Unggah gambar bumbu masak untuk mendapatkan prediksinya.")

uploaded_file = st.file_uploader("Upload gambar", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        # Baca file gambar
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Gambar yang diunggah", use_container_width=True)
        
        # Load model
        model = load_model()

        # Load informasi bumbu
        bumbu_info = load_bumbu_info()

        # Prediksi
        label = predict(image, model, transform)
        st.success(f"Prediksi: **{label.capitalize()}**")
        
        # Tampilkan deskripsi
        if label in bumbu_info:
            info = bumbu_info[label]
            
            # Deskripsi
            if "description" in info:
                st.write("**Deskripsi:**")
                st.write(info["description"])
            
            # Resep
            if "recipes" in info and info["recipes"]:
                st.write("**Contoh Masakan:**")
                for recipe in info["recipes"]:
                    if "image" in recipe and recipe["image"]:
                        st.image(recipe["image"], caption=recipe["name"], width=300)
                    st.write(f"- [{recipe['name']}]({recipe['link']})")
            
            # Catatan
            if "notes" in info:
                st.write("**Catatan:**")
                st.markdown(info["notes"])
            
            # Perbedaan
            if "diff" in info and info["diff"]:
                for diff in info["diff"]:
                    st.write(f"- [{diff['name']}]({diff['link']})")
        else:
            st.warning("Informasi tentang bumbu ini belum tersedia.")

    except Exception as e:
        st.error(f"Terjadi kesalahan: {str(e)}")
