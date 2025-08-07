import streamlit as st
from PIL import Image

def plot_img(path, w = None):
    try:    
        img = Image.open(path)
        if w is None:
            st.image(img)
        else:
            st.image(img, width = w)
    except:
        st.write('No image available')





