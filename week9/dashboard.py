import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from textblob import TextBlob
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords as stopwords_scratch
import re
import string
import joblib

st.title("NLP Dashboard Bahasa Indonesia")

@st.cache_data
def load_data():
    data = pd.read_csv('komentardengansentimen.csv', index_col=0)
    return data

df = load_data()
df['Komentar'] = df['Komentar'].fillna('')
comments = df['Komentar'].to_list()

pipeline = joblib.load('training.joblib')

def preprocess(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.strip()
    return text

def get_stopwords():
    list_stopwords = stopwords_scratch.words('indonesian') + stopwords_scratch.words('english')
    list_stopwords.extend(['ya', 'yg', 'ga', 'yuk', 'dah', 'ngga', 'engga', 'ygy', 'wkwkwk', 'sih', 'tdk', 'aja', 'dan', 'yang'])
    return list_stopwords

stopwords = get_stopwords()

vectorizer = TfidfVectorizer(stop_words=stopwords)
X = vectorizer.fit_transform(comments[:100])

true_k = 4
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1, random_state=42)
model.fit(X)

# Fungsi Prediksi Sentimen dengan TextBlob
def analyze_sentiment(text):
    analysis = TextBlob(text).sentiment.polarity
    if analysis > 0:
        return "Positif"
    elif analysis < 0:
        return "Negatif"
    else:
        return "Netral"

# Fungsi Prediksi Kluster
def predict_cluster(text):
    vector = vectorizer.transform([text])
    if vector.nnz == 0:
        return None  # Kata tidak ditemukan
    return model.predict(vector)[0]

# Fungsi WordCloud
def generate_wordcloud(labels, text_data, title):
    cluster_text = ' '.join(text_data)
    wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=stopwords).generate(cluster_text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    st.pyplot(plt)

# 4. Navigasi Antar Halaman
page = st.sidebar.selectbox("Pilih Halaman", ["Analisis Sentimen", "WordCloud"])

if page == "Analisis Sentimen":
    st.title("Analisis Sentimen")
    with st.form("nlpForm"):
        user_input = st.text_input("Masukkan kalimat:")
        submit_button = st.form_submit_button(label='Analisis!')
    if user_input:
        st.info("Hasil Analisis")
        cleaned = preprocess(user_input)
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

elif page == "WordCloud":
    st.title("WordCloud dari Clustering atau Sentimen")
    option = st.selectbox("Pilih WordCloud", ["Clustering", "Berdasarkan Sentimen"])

    if option == "Clustering":
        labels = model.predict(X)
        for i in range(true_k):
            cluster_comments = [comments[j] for j in range(len(labels)) if labels[j] == i]
            generate_wordcloud(labels, cluster_comments, f'WordCloud untuk Kluster {i}')

    elif option == "Berdasarkan Sentimen":
        for sentiment in ["Positif", "Negatif", "Netral"]:
            sentiment_comments = [c for c in comments if analyze_sentiment(c) == sentiment]
            generate_wordcloud([], sentiment_comments, f'WordCloud untuk Sentimen {sentiment}')
