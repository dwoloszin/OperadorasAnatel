import streamlit as st
from PIL import Image
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import io
import nltk
nltk.download('punkt')

st.set_page_config(page_title='InNews🇮🇳: A Summarised News📰 Portal', page_icon='./Meta/newspaper.ico')

mosiacLink = 'http://sistemas.anatel.gov.br/se/public/view/b/licenciamento.php'



    





def run():
    st.title("Anatel: Get sites")
    image = Image.open('./Meta/newspaper.png')
    col1, col2, col3 = st.columns([3, 5, 3])
    with col1:
        st.write("")
    with col2:
        st.image(image, use_column_width=False) 
    with col3:
        st.write("")   
    category = ['--Select--', 'SP', 'RJ', 'BA'] 
    cat_op = st.selectbox('Select your Category', category)
    if cat_op == category[0]:
        st.warning('Please select Type!!')
 

run()
