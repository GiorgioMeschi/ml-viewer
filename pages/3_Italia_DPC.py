
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

if 'vs_it' not in st.session_state:
    st.session_state.vs_it = None

def set_vs(v):
    st.session_state.vs_it = v

# create 2 buttons based on the version you want to view
vs_selection_cols = st.columns(4)
with vs_selection_cols[1]:
    normal_version = st.button('single model Version', on_click = set_vs, args=('Single',), key = 'v_1')
with vs_selection_cols[2]:
    models_version = st.button('4-models Version',  on_click = set_vs, args=('4-Models',), key = 'v_2')

vs_it = st.session_state.vs_it

if vs_it == 'Single':
    project_datapath = f'{DATAPATH}/data/italia-dpc'
    if not os.path.isdir(project_datapath):
        st.error(f"No data availble for this project in your dataset.")
        st.stop()

    # change color if selected
    css = '''
    .stElementContainer.element-container.st-key-v_1.st-emotion-cache-zh2fnc.eceldm40 {
        background-color: yellow !important;
        color: red;
        
    }
    .stButton.st-emotion-cache-8atqhb.e1mlolmg0 {
        opacity: 0.8;
        }'''
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

elif vs_it == '4-Models':
    project_datapath = f'{DATAPATH}/data/italia-dpc/4models'
    if not os.path.isdir(project_datapath):
        st.error(f"No data availble for this project in your dataset.")
        st.stop()
    
    # change color if selected
    css = '''
    .stElementContainer.element-container.st-key-v_2.st-emotion-cache-zh2fnc.eceldm40 {
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


run_dates = sorted([f for f in os.listdir(project_datapath) if f not in ['static', 'statistics', '4models']])
# force order of the runs based on month   
run_dates = sorted(run_dates, key=lambda x: (int(x.split('-')[0]), int(x.split('-')[1]))) # xxxx-m: sort based on the xxxx and then -m 
latest = run_dates[-1]

# initiate the country selection 
if 'run' not in st.session_state:
    st.session_state.run = latest

def change_run_id():
    return st.session_state.run

try:
    run_date = st.sidebar.selectbox('RUN DATES', run_dates, index = run_dates.index(st.session_state.run), on_change = change_run_id, key = 'run')
except ValueError: # handle the date in session state if is absent
    run_date = st.sidebar.selectbox('RUN DATES', run_dates, index = 0, on_change = change_run_id, key = 'run')


header_cols = st.columns(3)
with header_cols[1]:
    st.header('Italia 2025 DPC')

st.divider()

columns_1st = st.columns(2)

img_width = st.slider("Image width", min_value=100, max_value=1000, value=550)

with columns_1st[0]:
    fuel_path = f'{project_datapath}/{run_date}'
    fuel_version = st.session_state.get('fuel_sea', False)
    if fuel_version:
        fuel_img = [f for f in os.listdir(fuel_path) if f.startswith('haz_seasonal_plot_')][0]
    else:
        fuel_img = [f for f in os.listdir(fuel_path) if f.startswith('haz_plot_')][0]

    plot_img(f'{fuel_path}/{fuel_img}', img_width)

    if vs_it == '4-Models':
        fuel_version = st.toggle('view seasonal version', key = 'fuel_sea')
    

with columns_1st[1]:

    # vs_susc = st.session_state.susc
    # susc_version = None
    suscept_path = f'{project_datapath}/{run_date}'
    if vs_it == '4-Models':
        susc_version = st.session_state.get('alt', False)
        if susc_version:
            try:
                suscept_img = [f for f in os.listdir(suscept_path) if f.startswith('susc_seasonal')][0]
            except:
                st.info("No seasonal susceptibility map available for this run")
        else:
            suscept_img = [f for f in os.listdir(suscept_path) if f.startswith('susc_alternative')][0]
    else:
        suscept_img = [f for f in os.listdir(suscept_path) if f.startswith('susc_plot')][0]


    plot_img(f'{suscept_path}/{suscept_img}', img_width)

    if vs_it == '4-Models':
        susc_version = st.toggle('view seasonal version', key = 'alt')


# add toggle object - fuel map distribibution
fuel_chart = st.toggle("Show Fuel Class Distribution Pie Chart", key="show_fuel_pie")

if fuel_chart:
    fuel_pie(project_datapath, run_date)

# insert container with stats plot
with st.expander("Statistics"):
    stats_version = st.session_state.get('stats_sea', False)
    if stats_version:
        stats_path = f'{project_datapath}/statistics/sentinel_ba_over_fuel_classes_seasonal.csv'
    else:
        stats_path = f'{project_datapath}/statistics/sentinel_ba_over_fuel_classes.csv'
    if os.path.isfile(stats_path):
        generate_ba_stats_plot(stats_path)
        st.caption("Fuel class distribution in sentinel2 burned area from Autobam")
    else:
        st.info("No burned area statistics available for this run.")
    
    if vs_it == '4-Models':
        stats_version = st.toggle('view seasonal version', key = 'stats_sea')


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

if vs_it == '4-Models':
    st.divider()

    columns_3rd = st.columns(3)

    with columns_3rd[0]:
        st.subheader('SPI 1')
        spiname = [f for f in spinames if f.startswith('SPEI1_')][0]
        spi1_path = f'{project_datapath}/{run_date}/{spiname}'
        plot_img(spi1_path, img_width_1)

    with columns_3rd[1]:
        st.subheader('SPI 3')
        spiname = [f for f in spinames if f.startswith('SPEI3_')][0]
        spi3_path = f'{project_datapath}/{run_date}/{spiname}'
        plot_img(spi3_path, img_width_1)

    with columns_3rd[2]:
        st.subheader('SPI 6')
        spiname = [f for f in spinames if f.startswith('SPEI6_')][0]
        spi6_path = f'{project_datapath}/{run_date}/{spiname}'
        plot_img(spi6_path, img_width_1)


st.divider()

static_path = f'{DATAPATH}/data/italia-dpc/static'
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


# show table/plot of historical stats
show_burned_pixel_per_susc_class(project_datapath) # automaic handle the absence of data


st.divider()






