import streamlit as st
import pandas as pd

from PIL import Image
image = Image.open("D:\\mgodonf\\appweb\\week3\\pexels-souvenirpixels-417074.jpg")
st.image(image, caption = 'pemandangan sungai dan gunung')

audio_file = open("D:\\mgodonf\\appweb\\week3\\test.mp3", 'rb')
audio_bytes = audio_file.read()
st.audio(audio_bytes, format= 'audio/mp3')

video_file = open("D:\\mgodonf\\appweb\\week3\\lifecouldbeadream.mp4", 'rb')
video_bytes = video_file.read()

st.video(video_bytes)