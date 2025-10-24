
#%%

import streamlit as st
import sys
import os


p = os.path.dirname(os.path.dirname(__file__) )
sys.path.append(p)

from utils import plot_img, access_data, show_burned_pixel_per_susc_class
from stats import generate_ba_stats_plot, fuel_pie


#%%


DATAPATH = access_data()

if 'vs' not in st.session_state:
    st.session_state.vs = None

def set_vs(v):
    st.session_state.vs = v

# create 2 buttons based on the version you want to view
vs_selection_cols = st.columns(4)
with vs_selection_cols[1]:
    normal_version = st.button('single model Version', on_click = set_vs, args=('Single',), key = 'v1')
with vs_selection_cols[2]:
    models_version = st.button('4-models Version',  on_click = set_vs, args=('4-Models',), key = 'v2')

vs = st.session_state.vs

if vs == 'Single':
    project_datapath = f'{DATAPATH}/data/sardegna-medstar'
    if not os.path.isdir(project_datapath):
        st.error(f"No data availble for this project in your dataset.")
        st.stop()

    # change color if selected
    css = '''
    .stElementContainer.element-container.st-key-v1.st-emotion-cache-zh2fnc.eceldm40 {
        background-color: yellow !important;
        color: red;
        
    }
    .stButton.st-emotion-cache-8atqhb.e1mlolmg0 {
        opacity: 0.8;
        }'''
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

elif vs == '4-Models':
    project_datapath = f'{DATAPATH}/data/sardegna-medstar/4models'
    if not os.path.isdir(project_datapath):
        st.error(f"No data availble for this project in your dataset.")
        st.stop()
    
    # change color if selected
    css = '''
    .stElementContainer.element-container.st-key-v2.st-emotion-cache-zh2fnc.eceldm40 {
        background-color: yellow !important;
        color: red;
        
    }
    .stButton.st-emotion-cache-8atqhb.e1mlolmg0 {
        opacity: 0.8;
        }'''

    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

else:
    project_datapath = f'{DATAPATH}/data/-'  # default


# st.write("Selected version:", vs)
# st.write("Selected version:", project_datapath)
if not os.path.isdir(project_datapath):
    st.info(f"select a model version to proceed")
    st.stop()

# else:
# st.write("Selected version:", vs)

run_dates = sorted([f for f in os.listdir(project_datapath) if f not in ['static', 'statistics']])
latest = run_dates[0]

# initiate the country selection 
if 'run' not in st.session_state:
    st.session_state.run = latest

def change_run_id():
    return st.session_state.run

try:
    run_date = st.sidebar.selectbox('RUN DATES', run_dates, index = run_dates.index(st.session_state.run), on_change = change_run_id, key = 'run')
except ValueError: # handle the first date in session state that is absent in 1 version
    run_date = st.sidebar.selectbox('RUN DATES', run_dates, index = 0, on_change = change_run_id, key = 'run')

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


# add toggle object - fuel map distribibution
fuel_chart = st.toggle("Show Fuel Class Distribution Pie Chart", key="show_fuel_pie")

if fuel_chart:
    fuel_pie(project_datapath, run_date)



# insert container with stats plot
with st.expander("Statistics"):
    stats_path = f'{project_datapath}/statistics/sentinel_ba_over_fuel_classes.csv'
    if os.path.isfile(stats_path):
        generate_ba_stats_plot(stats_path)
        st.caption("Fuel class distribution in sentinel2 burned area from Autobam")
    else:
        st.info("No burned area statistics available for this run.")


st.divider()

img_width_1 = st.slider(" ", min_value=200, max_value=700, value=550)

columns_2nd = st.columns(3)

spinames = os.listdir(f'{project_datapath}/{run_date}')
with columns_2nd[0]:
    st.subheader('SPI 1')
    spiname = [f for f in spinames if f.startswith('SPI1_')][0]
    spi1_path = f'{project_datapath}/{run_date}/{spiname}'
    plot_img(spi1_path, img_width_1)

with columns_2nd[1]:
    st.subheader('SPI 3')
    spiname = [f for f in spinames if f.startswith('SPI3_')][0]
    spi3_path = f'{project_datapath}/{run_date}/{spiname}'
    plot_img(spi3_path, img_width_1)

with columns_2nd[2]:
    st.subheader('SPI 6')
    spiname = [f for f in spinames if f.startswith('SPI6_')][0]
    spi6_path = f'{project_datapath}/{run_date}/{spiname}'
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



show_burned_pixel_per_susc_class(project_datapath)




  
    




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

    



