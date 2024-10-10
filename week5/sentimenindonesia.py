import streamlit as st
import joblib
import re
import string

def preprocess(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.strip()
    return text

model = joblib.load('indonesiamodel.pkl')
vectorizer = joblib.load('indonesiavectorizer.pkl')

def main():
    st.title("Analisis Sentimen Menggunakan app NLP")
    st.title("Berbahasa Indonesia")

    st.subheader("Beranda")
    with st.form("nlpForm"):
        raw_text = st.text_area("Masukkan kalimat yang akan dianalisis")
        submit_button = st.form_submit_button(label='Analisis!')

    col1, col2 = st.columns(2)
    if submit_button:
        with col1:
            st.info("Hasil Analisis")
            cleaned = preprocess(raw_text)
            vectorized = vectorizer.transform([cleaned])
            prediction = model.predict(vectorized)[0]

            if prediction == 1:
                st.write("Kalimat anda memiliki sentimen positif")
                st.image("senyum.jpeg")
            elif prediction == -1:
                st.write("Kalimat anda memiliki sentimen negatif")
                st.image("geram.jpeg")
            else:
                st.write("kalimat anda netral sekali bung")
                st.image("batu.jpg")

if __name__ == "__main__":
    main()