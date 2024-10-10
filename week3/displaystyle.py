import streamlit as st
import pandas as pd

col1, col2, col3, col4 = st.columns(4)
col1.metric("Jumlah pendapatan", value=15, delta=2.5)
col2.metric("Jumlah pengeluaran", value=13, delta=-13)
col3.metric("Saldo sekarang", value=13129, delta=2, delta_color="off")
col4.metric("Tanggal gajian selanjutnya", "1/9/2024")

df = pd.DataFrame({
    'Kode Barang' : ['A14V', '99RG', 'G834', 'IRX9', 'RZ09'],
    'Nama Barang' : ['MSI Titan 18 HX', 'Acer Predator Helios 18', 'Asus ROG Strix Scar 18', 'Lenovo Legion 9i (2024)', 'Razer Blade 18'],
    'Jumlah Stok' : [5, 7, 6, 6, 4],
    'Harga Satuan' : ['$5100', '$4000', '$3848', '$3700', '$4900']
})

st.dataframe(df)