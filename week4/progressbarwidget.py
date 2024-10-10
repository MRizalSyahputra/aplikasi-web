import streamlit as st
import time 


'memulai proses'
'mohon tunggu sebentar...'
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100) :
    latest_iteration.text(f'progres : {i+1} %')
    bar.progress(i+1)
    time.sleep(0.1)
    
with st.spinner(text="dikit lagi...") :
    time.sleep(3)

st.balloons()
'proses selesai!'