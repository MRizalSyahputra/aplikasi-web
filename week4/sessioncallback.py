import streamlit as st 


if 'key' not in st.session_state:
    st.session_state.key = 'value'

st.session_state.key = 'value2' 
st.session_state['key'] = 'value2' 

del st.session_state['key']

for key in st.session_state.keys():
    del st.session_state[key]

def form_callback():
    st.write(st.session_state.my_slider)
    st.write(st.session_state.my_checkbox)

with st.form(key='my_form'):
    slider_input = st.slider('My slider', 0, 10, 5, key='my_slider')
    checkbox_input = st.checkbox('Yes or No', key='my_checkbox')
    submit_button = st.form_submit_button(label='Submit', on_click=form_callback)