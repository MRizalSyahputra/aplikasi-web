import streamlit as st
import joblib,os
import numpy as np

def loadmodel(model_file):
    loaded = joblib.load(open(os.path.join(model_file),"rb"))
    return loaded

def main():
    """Regresi Linear Simpel"""
    st.title("Perkiraan Penggunaan Listrik")

    html = """
	<div style="background-color:#726E6D;padding:10px;">
	<h3 style="color:white">Perkiraan penggunaan listrik menggunakan regresi linear</h3>
	</div>
	"""

    st.markdown(html, unsafe_allow_html=True)

    st.subheader("Perkiraan penggunaan listrik")
    experience = st.slider("Ini bulan perhitungan ke-berapa?", 1, 36)

    if st.button("Perkirakan"):
        regressor = loadmodel("elecusage.pkl")
        experience_reshaped = np.array(experience).reshape(-1,1)
        prediction = regressor.predict (experience_reshaped)

        st.info("Perkiraan Penggunaan Listrik pada Bulan ke-{} Adalah: {} kWh".format(experience,(prediction[0][0].round(2))))


if __name__ == '__main__':
	main()

