import streamlit as st
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder

model = pickle.load(open('model.pkl', 'rb'))

def predict_default(input_data):
    prediction = model.predict(input_data)  
    return prediction



bank_name_encoder = LabelEncoder()
bank_name_encoder.classes_ = np.array(['Diamond Bank','EcoBank','First Bank','GT Bank','UBA','Union Bank','FCMB','Access Bank','Zenith Bank','Fidelity Bank','Stanbic IBTC','Skye Bank','Sterling Bank','Wema Bank','Keystone Bank','Unity Bank','Heritage Bank','Standard Chartered'])  

employment_status_encoder = LabelEncoder()
employment_status_encoder.classes_ = np.array(['Permanent', 'Self-Employed', 'Student', 'Unemployed', 'Retired', 'Contract'])

# Streamlit App
st.title("Loan Default Prediction")
html_file="""
<div style="background-color:Blue; padding:10px">
<h2 style="color:white; text-align:center;">StreamLit loan default App</h2>
</div>
"""

st.markdown(html_file, unsafe_allow_html=True)

longitude_gps_input = st.text_input('Longitude GPS')
latitude_gps_input = st.text_input('Latitude GPS')
totaldue_y_input = st.text_input('Total Due Y')

error_flag = False
age = st.number_input('Age', min_value=18, max_value=90, step=1)
loannumber_y = st.number_input('Loan Number Y', min_value=1, step=1)
bank_name_clients = st.selectbox('Bank Name', options=bank_name_encoder.classes_)
loanamount_y = st.number_input('Loan Amount Y', min_value=5000, step=50)
employment_status_clients = st.selectbox('Employment Status', options=employment_status_encoder.classes_)
termdays_y = st.number_input('Term Days Y', min_value=1, max_value=30, step=1)
totaldue_x = st.number_input('Total Due X', min_value=10, step=5)


if st.button('Predict Loan Default'):
    try:
        longitude_gps = float(longitude_gps_input)
    except ValueError:
        st.error("Please enter a valid numeric value for Longitude GPS")
        error_flag = True
    try:
        latitude_gps = float(latitude_gps_input)
    except ValueError:
        st.error("Please enter a valid numeric value for Latitude GPS")
        error_flag = True
    try:
        totaldue_y = float(totaldue_y_input)
    except ValueError:
        st.error("Please enter a valid numeric value for Total Due Y")
        error_flag = True
    if not error_flag:
        bank_name_encoded = bank_name_encoder.transform([bank_name_clients])[0]
        employment_status_encoded = employment_status_encoder.transform([employment_status_clients])[0]
        input_data = np.array([
            longitude_gps, latitude_gps, age, loannumber_y, bank_name_encoded,
            totaldue_y, loanamount_y, employment_status_encoded, termdays_y, totaldue_x
        ]).reshape(1, -1)
        prediction = predict_default(input_data)
        if prediction == 1:
            st.markdown(f"<h3 style='font-weight:bold; font-size: 30px;'>This person is likely to default in paying back</h3>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h3 style='font-weight:bold; font-size: 30px;'>This person is unlikely to default in paying back</h3>", unsafe_allow_html=True)
           
