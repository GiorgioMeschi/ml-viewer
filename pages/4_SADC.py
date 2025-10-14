
import streamlit as st
import sys
import os
from PIL import Image
import shutil
import pandas as pd

p = os.path.dirname(os.path.dirname(__file__) )
sys.path.append(p)

from utils import plot_img, access_data
from stats import generate_ba_stats_plot, show_table, plot_historical_stats

#%%

DATAPATH = access_data()

# page code
project_datapath = f'{DATAPATH}/data/sadc'

if not os.path.isdir(project_datapath):
    st.error(f"No data availble for this project in your dataset.")
    st.stop()


run_dates = sorted([f for f in os.listdir(project_datapath) if f not in ['static', 'statistics', 'ba']])

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

header_cols = st.columns(3)
with header_cols[1]:
    st.header('Africa Union')

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


ba_cols = st.columns([0.2,0.6,0.2])
with ba_cols[1]:
    m = int(run_date.split('-')[1])+1
    y = int(run_date.split('-')[0])
    if y == 2024:
        ba_path = f'{project_datapath}/ba/BA_{m}.png'
    else:
        ba_path = f'{project_datapath}/ba/-.png'  # for 2023 show december
    plot_img(ba_path, 600)

    

with st.expander("Statistics"):
    stats_path = f'{project_datapath}/statistics/sentinel_ba_over_fuel_classes.csv'
    if os.path.isfile(stats_path):
        generate_ba_stats_plot(stats_path)
        st.caption("Fuel class distribution for the year 2024")
    else:
        st.info("No burned area statistics available for this run.")


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



with st.expander("View Historical Stats Table"):

    # create 3 columsn the ceter 75% wide
    endcols = st.columns([1,6,1])
    with endcols[1]:

        # radio button with showing the table in percentage or not
        show_perc = st.radio("Show values as percentage?", ('No', 'Yes'), index=0, horizontal=True)
        if show_perc == 'Yes':
            table_file = f'{project_datapath}/statistics/table_ba_susc_perc.csv'
            rounds = 2
            show_table(table_file, rounds)
            with st.expander("Plot Historical Stats"):
                plot_historical_stats(pd.read_csv(table_file, index_col=0))

        else:
            table_file = f'{project_datapath}/statistics/table_ba_susc.csv'
            rounds = 0
            show_table(table_file, rounds)
            with st.expander("Plot Historical Stats"):
                plot_historical_stats(pd.read_csv(table_file, index_col=0))

