
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

# page code
project_datapath = f'{DATAPATH}/data/ethiopia-medwesa'

if not os.path.isdir(project_datapath):
    st.error(f"No data availble for this project in your dataset.")
    st.stop()


run_dates = sorted([f for f in os.listdir(project_datapath) if f not in ['static', 'statistics']])

latest = run_dates[0]

# initiate the country selection 
if 'run' not in st.session_state:
    st.session_state.run = latest

def change_run_id():
    return st.session_state.run

try:
    run_date = st.sidebar.selectbox('RUN DATES', run_dates, index = run_dates.index(st.session_state.run), on_change = change_run_id, key = 'run')
except ValueError: # handle the first date in session state that is absent in italy
    run_date = st.sidebar.selectbox('RUN DATES', run_dates, index = 0, on_change = change_run_id, key = 'run')

header_cols = st.columns([1,2,1])
with header_cols[1]:
    st.header('Ethiopia MEDEWSA 2025')

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
fuel_chart = st.toggle("Show Fuel Class Distribution Pie Chart", key="show_fuel_pie_page5")

if fuel_chart:
    fuel_pie(project_datapath, run_date)

# st.divider()


# insert container with stats plot
with st.expander("Statistics"):
    stats_path = f'{project_datapath}/statistics/sentinel_ba_over_fuel_classes.csv'
    if os.path.isfile(stats_path):
        generate_ba_stats_plot(stats_path)
        st.caption("Fuel class distribution in sentinel2 burned area from Autobam")
    else:
        st.info("No fire data for validate the year 2025 available yet...")


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


st.divider()






