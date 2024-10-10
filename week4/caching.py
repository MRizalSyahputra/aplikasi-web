import streamlit as st
import time
import requests

@st.cache_data
def coy():
    time.sleep(2)
    return 1, 2, 3, 4, 5

@st.cache_data
def link(url):
    time.sleep(2)
    response = requests.get(url)
    return response.content

@st.cache_data
def links(url2):
    time.sleep(2)
    response = requests.get(url2)
    return response.content

url = "https://wallpapers.com/downloads/high/beautiful-scenery-sunrise-waterfall-wnxju2647uqrcccv.webp"
url2 = "https://cdn.magicdecor.in/com/2023/12/20172031/Elegant-Mount-Fuji-Scenery-Wallpaper-in-Japandi-Style.jpg"


st.title("ini caching ma")
if st.button("Angkas"):
    data = coy()
    st.write("Data:", data)

if st.button("gambar"):
    gambar = link(url)
    st.image(gambar)

if st.button("gambar yang sama"):
    gambar = link(url)
    st.image(gambar)

if st.button("beda gambar"):
    gambar = links(url2)
    st.image(gambar)