from PIL import Image
import streamlit as st

def app():

    img = Image.open('payme.jpeg')
    st.image(img,width=200,caption='Scan to support this project')
    st.subheader("What I’m going to do with your donation: 
    "-  Implementing new models"
    "-	Buy better servers to make faster analysis
 
    ")
