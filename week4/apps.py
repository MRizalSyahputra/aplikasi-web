import streamlit as st 
import pandas as pd
import numpy as np

st.title('A diagram of founded pokemon in pokemon GO')

URL = "C:\\Users\\ACER\\Downloads\\uber-raw-data-sep14.csv.gz"
date = 'date/time'

@st.cache_data
def load(nrows):
    data = pd.read_csv(URL, nrows=nrows)
    lowercase = lambda x: str(x).lower() 
    data.rename(lowercase, axis='columns', inplace=True)
    data[date] = pd.to_datetime(data[date])
    return data

data_load_state = st.text("loading your data")
data = load(1000000)
data_load_state.text("done!")

if st.checkbox("Show data"):
    st.subheader("Raw Data")
    st.write(data)

st.subheader("Catched pokemon each hour")
hist_values = np.histogram(data[date].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

htf = st.slider('hour', 0, 23, 17)
fd = data[data[date].dt.hour==htf]

st.subheader('Map of all capture at %s:00' % htf)
st.map(fd)