

#%%

import os
import sys
import streamlit as st
# from PIL import Image
# import pandas as pd

PATH = os.path.dirname(__file__)
# PATH = os.getcwd()
sys.path.append(PATH)

#%% global vars

DATAPATH_1 = '/home/fremen/workspaces/GM/projects/sardegna2025/viewer/ml-viewer/data'


#%% app

st.set_page_config(layout="wide")

if __name__ == '__main__':
    st.write('Select a project from the sidebar to start exploring the data')


#%%



