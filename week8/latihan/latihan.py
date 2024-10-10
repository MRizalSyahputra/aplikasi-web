import streamlit as st
import joblib,os
import numpy as np 

# Loading Models
def load_prediction_model(model_file):
	loaded_model = joblib.load(open(os.path.join(model_file),"rb"))
	return loaded_model

def main():
	"""Regresi Linier Sederhana"""

	st.title("Harga emas dalam periode")

	html_templ = """
	<div style="background-color:#726E6D;padding:10px;">
	<h3 style="color:white">Prediksi harga emas menggunakan regresi linear</h3>
	</div>
	"""

	st.markdown(html_templ,unsafe_allow_html=True)

	activity = ["Penentuan harga emas","Apa itu Regresi?"]
	choice = st.sidebar.selectbox("Menu",activity)

	if choice == 'Penentuan harga emas':

		st.subheader("Penentuan Harga Emas")

		experience = st.slider("bulan ke-berapa? (bulan 1 : Januari 1950)",1,826)


		if st.button("Proses"):

			regressor = load_prediction_model("D:/eksperimen/appweb/week8/latihan/lregress_goldprice2.pkl")
			experience_reshaped = np.array(experience).reshape(-1,1)

			predicted_price = regressor.predict(experience_reshaped)

			st.info("Harga emas setelah bulan ke- {} : {}".format(experience,(predicted_price[0][0].round(2))))



if __name__ == '__main__':
	main()