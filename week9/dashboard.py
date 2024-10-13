import streamlit as st
import pickle

with open("wordcloud.pkl", "rb") as f:
    fig = pickle.load(f)

st.pyplot(fig)