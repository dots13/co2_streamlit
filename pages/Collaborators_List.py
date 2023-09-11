import streamlit as st
st.set_page_config(page_title='Predicting CO2 Emissions', page_icon=':earth_africa:', initial_sidebar_state='auto')
st.title('Omdena CO2 emissions project', anchor=None)
st.subheader('Active Collaborators List')

st.markdown(
"""
- Aisha Yasir
- Anastasiia Marchenko
- Anilreddy Kunta
- AqibRehman PirZada
- Arnav Upadhyay
- Augustine
- Chris Hollman
- Dorsa Rohani
- Gabriela Enríquez
- Hilda Posada
- Marvin Lav
- Mateusz Filipowicz
- Mohamed Chahed
- Neev Goenka
- Nurullah Sirca
- Omughele Fabulous
- Saloni Jhalani
- Sanket Sharma
- Shaheer Abdullah
- Sosna Achamyeleh
- Srihitha Reddy
- Tanisha Banik
- Vânia Nunes
- Walid Hossain
- Wallace Ferreira
- Wout Van parijs
- Shaista Hussain
"""
)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)