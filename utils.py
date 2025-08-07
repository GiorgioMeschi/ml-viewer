import streamlit as st
from PIL import Image

def plot_img(path):
    try:    
        img = Image.open(path)
        st.image(img) 
    except:
        st.write('No image available')

