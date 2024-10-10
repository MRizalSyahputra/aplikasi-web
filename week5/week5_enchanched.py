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

model = joblib.load('model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

def main():
    st.title("Analisis Sentimen Menggunakan App NLP")
    st.title("Berbahasa Indonesia")

    menu = ["beranda", "tentang"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "beranda" :
        st.subheader("Beranda")
        with st.form("nlpForm"):
            raw_text = st.text_area("Masukkan kalimat Anda")
            submit_button = st.form_submit_button(label='Analyze')
        
        col1, col2 = st.columns(2)
        if submit_button:
            with col1:
                st.info("Results")

                raw_text_cleaned = preprocess(raw_text) 
                text_vectorized = vectorizer.transform([raw_text_cleaned]) 

                prediction = model.predict(text_vectorized)[0]

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