import streamlit as st
import joblib
import re
import string

# Fungsi preprocessing dari Jupyter Notebook
def preprocess(text):
    # Mengubah menjadi huruf kecil
    text = text.lower()

    # Menghapus angka
    text = re.sub(r'\d+', '', text)

    # Menghapus tanda baca
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Hilangkan spasi berlebih
    text = text.strip()

    return text

# Muat model dan vectorizer
model = joblib.load('sentiment_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

def main():
    st.title("Analisis Sentimen Menggunakan App NLP")
    st.title("Proyek Streamlit")

    menu = ["beranda", "tentang"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "beranda":
        st.subheader("Beranda")
        with st.form("nlpForm"):
            raw_text = st.text_area("Masukkan kalimat Anda")
            submit_button = st.form_submit_button(label='Analyze')

        # Layout
        col1, col2 = st.columns(2)
        if submit_button:
            with col1:
                st.info("Results")

                # Preprocessing input text
                raw_text_cleaned = preprocess(raw_text)  # Preprocess teks input
                text_vectorized = vectorizer.transform([raw_text_cleaned])  # Vectorize input

                # Prediksi sentimen menggunakan model
                prediction = model.predict(text_vectorized)[0]

                # Tampilkan hasil prediksi
                if prediction == 1:
                    st.write("Sentimen: Positif")
                    st.image("senyum.jpeg")
                elif prediction == -1:
                    st.write("Sentimen: Negatif")
                    st.image("geram.jpeg")
                else:
                    st.write("Sentimen: Netral")
                    st.image("batu.jpg")

    else:
        st.subheader("Tentang")

if __name__ == '__main__':
    main()
