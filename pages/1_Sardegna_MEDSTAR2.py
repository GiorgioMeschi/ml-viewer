
#%%

import streamlit as st
import sys
import os
from PIL import Image
import shutil 

#%%

def access_data():
    data_root = st.session_state.get("data_root")
    if not data_root or not os.path.isdir(data_root):
        st.info("No uploaded dataset for this session. Please upload on the Home page.")
        st.stop()
    
    if st.sidebar.button("Finish session and remove my upload"):
        try:
            shutil.rmtree(data_root)
        except Exception as e:
            st.warning(f"Could not delete upload directory: {e}")
        st.session_state.pop("data_root", None)
        st.success("Your upload was removed.")
        st.stop()

    return data_root


p = os.path.dirname(os.path.dirname(__file__) )
sys.path.append(p)

from utils import plot_img
DATAPATH = access_data()

# page code
project_datapath = f'{DATAPATH}/data/sardegna-medstar'

run_dates = sorted([f for f in os.listdir(project_datapath) if f != 'static'])
latest = run_dates[0]

# initiate the country selection 
if 'run' not in st.session_state:
    st.session_state.run = latest

def change_run_id():
    return st.session_state.run

run_date = st.sidebar.selectbox('RUN DATES', run_dates, index = run_dates.index(st.session_state.run), on_change = change_run_id, key = 'run')

header_cols = st.columns(3)
with header_cols[1]:
    st.header('Sardegna MEDSTAR2')

st.divider()

columns_1st = st.columns(2)

img_width = st.slider("Image width", min_value=100, max_value=1000, value=550)

with columns_1st[0]:
    # st.subheader('Fuel MAP')
    fuel_path = f'{project_datapath}/{run_date}'
    fuel_img = [f for f in os.listdir(fuel_path) if f.startswith('haz_plot_')][0]
    plot_img(f'{fuel_path}/{fuel_img}', img_width)
    

with columns_1st[1]:
    # st.subheader('SUSCPETBILITY')
    suscept_path = f'{project_datapath}/{run_date}'
    suscept_img = [f for f in os.listdir(suscept_path) if f.startswith('susc_plot')][0]
    plot_img(f'{suscept_path}/{suscept_img}', img_width)

st.divider()

img_width_1 = st.slider(" ", min_value=200, max_value=700, value=550)

columns_2nd = st.columns(3)


with columns_2nd[0]:
    st.subheader('SPI 1')
    spi1_path = f'{project_datapath}/{run_date}/SPI1_{run_date}.png'
    plot_img(spi1_path, img_width_1)

with columns_2nd[1]:
    st.subheader('SPI 3')
    spi3_path = f'{project_datapath}/{run_date}/SPI3_{run_date}.png'
    plot_img(spi3_path, img_width_1)

with columns_2nd[2]:
    st.subheader('SPI 6')
    spi6_path = f'{project_datapath}/{run_date}/SPI6_{run_date}.png'
    plot_img(spi6_path, img_width_1)

st.divider()

columns_3rd = st.columns(3)

with columns_3rd[0]:
    st.subheader('SPEI 1')
    spei1_path = f'{project_datapath}/{run_date}/SPEI1_{run_date}.png'
    plot_img(spei1_path, img_width_1)

with columns_3rd[1]:
    st.subheader('SPEI 3')
    spei3_path = f'{project_datapath}/{run_date}/SPEI3_{run_date}.png'
    plot_img(spei3_path, img_width_1)

with columns_3rd[2]:
    st.subheader('SPEI 6')
    spei6_path = f'{project_datapath}/{run_date}/SPEI6_{run_date}.png'
    plot_img(spei6_path, img_width_1)

st.divider()

static_path = f'{project_datapath}/static'
columns_4th = st.columns(4)

with columns_4th[0]:
    st.subheader('DEM')
    dem_path = f'{static_path}/DEM.png'
    plot_img(dem_path, img_width_1)

with columns_4th[1]:
    st.subheader('Vegetation')
    veg_path = f'{static_path}/vegetation.png'
    plot_img(veg_path, img_width_1)

with columns_4th[2]:
    # slope
    st.subheader('Slope')
    slope_path = f'{static_path}/Slope.png'
    plot_img(slope_path, img_width_1)

with columns_4th[3]:
    # aspect
    st.subheader('Aspect')
    aspect_path = f'{static_path}/Aspect.png'
    plot_img(aspect_path, img_width_1)



#%%

# from auth import login_widget, logout_widget

# transfer the autentication among pages
# try:
#     auth_status = login_widget()  # visible login on main page
# except Exception as e:  # None (widget shown, not yet submitted)
#     # st.error("Username/password incorrect")
#     st.error(str(e))


# if st.session_state.get('authentication_status'):
#     logout_widget(key = 'logut_page1')
# elif st.session_state.get('authentication_status') is False:
#     st.error('Username/password is incorrect')
# elif st.session_state.get('authentication_status') is None:
#     st.warning('Please enter your username and password')

    



