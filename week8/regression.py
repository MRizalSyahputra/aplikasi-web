# Core Pkgs
import streamlit as st
import sklearn
import joblib,os
import numpy as np 

# Loading Models
def load_prediction_model(model_file):
	loaded_model = joblib.load(open(os.path.join(model_file),"rb"))
	return loaded_model

def main():
	"""Regresi Linier Sederhana"""

	st.title("Penentuan Gaji Karyawan")

	html_templ = """
	<div style="background-color:#726E6D;padding:10px;">
	<h3 style="color:white">Penentuan Gaji Karyawan Menggunakan Regresi Linier</h3>
	</div>
	"""

	st.markdown(html_templ,unsafe_allow_html=True)

	activity = ["Penentuan Gaji Karyawan","Apa itu Regresi?"]
	choice = st.sidebar.selectbox("Menu",activity)

# Salary Determination CHOICE
	if choice == 'Penentuan Gaji Karyawan':

		st.subheader("Penentuan Gaji Karyawan")

		experience = st.slider("Berapa tahun pengalaman kerjanya?",0,20)

		#st.write(type(experience))

		if st.button("Proses"):

			regressor = load_prediction_model("linear_regression_salary.pkl")
			experience_reshaped = np.array(experience).reshape(-1,1)

			predicted_salary = regressor.predict(experience_reshaped)

			st.info("Gaji untuk karyawan dengan pengalaman bekerja {} tahun: {}".format(experience,(predicted_salary[0][0].round(2))))



if __name__ == '__main__':
	main()