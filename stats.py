



import streamlit as st
import pandas as pd
import altair as alt
import os
import numpy as np
import matplotlib.pyplot as plt

# load your table (or replace with your existing DataFrame variable)
@st.cache_data
def load(path):
    return pd.read_csv(path)

def generate_ba_stats_plot(path):
    df = load(path)

    # slide bar
    months = list(dict.fromkeys(df["Month"].tolist()))
    month = st.radio("Month", months, horizontal=True)    
    sel = df[df["Month"] == month].sort_values("Fuel_Class")

    st.title(f"Burned area by fuel class — {month}")

    c1, c2, c3 = st.columns(3)

    c1.subheader("Area (ha)")
    c1.altair_chart(
        alt.Chart(sel).mark_bar().encode(
            x=alt.X("Fuel_Class:O", title="Fuel class"),
            y=alt.Y("Area_ha:Q", title="Area (ha)"),
            tooltip=["Fuel_Class", "Area_ha"]
        ).properties(height=320, width=300)
    )

    c2.subheader("% of burned area")
    c2.altair_chart(
        alt.Chart(sel).mark_bar().encode(
            x="Fuel_Class:O",
            y=alt.Y("Percentage_of_Burned_Area:Q", title="% of burned area"),
            tooltip=["Fuel_Class", "Percentage_of_Burned_Area"]
        ).properties(height=320, width=300)
    )

    c3.subheader("% of class extent burned")
    c3.altair_chart(
        alt.Chart(sel).mark_bar().encode(
            x="Fuel_Class:O",
            y=alt.Y("Percentage_of_Fuel_Class_Burned:Q", title="% of fuel class burned"),
            tooltip=["Fuel_Class", "Percentage_of_Fuel_Class_Burned"]
        ).properties(height=320, width=300)
    )

    st.caption("Fuel class distribution in sentinel2 burned area from Autobam")


# show large table of stast of historical data
def show_table(path, rounds):

    if not os.path.isfile(path):
        st.info("No historical statistics available for this version/project.")
        available = False
        return available
    df = pd.read_csv(path, index_col=0)
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.round(rounds) # round 2 decimanls
    st.subheader('Burned Area vs Susceptibility Classes')
    st.dataframe(df.T, height=450)   # interactive, scrollable
    available = True
    return available

# plot the data in historical stats exlec
def plot_historical_stats(df):

    df.index.name = 'class'
    df_long = df.reset_index().melt(id_vars='class', var_name='year_month', value_name='value')

    # parse year and month from columns like "2011_1"
    # some columns may have slightly different format; we guard using split('_')
    def parse_ym(s):
        parts = str(s).split('_')
        if len(parts) == 2:
            return int(parts[0]), int(parts[1])
        else:
            return None, None

    df_long[['year', 'month']] = df_long['year_month'].apply(lambda r: pd.Series(parse_ym(r)))
    df_long = df_long.dropna(subset=['year', 'month'])
    df_long['year'] = df_long['year'].astype(int)
    df_long['month'] = df_long['month'].astype(int)
    # make class a string for colors
    df_long['class'] = df_long['class'].astype(str)

    # add month name for nicer x-axis
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    df_long['month_name'] = df_long['month'].apply(lambda m: months[m-1] if 1 <= m <= 12 else str(m))

    # ---- UI: mode and selectors ----
    mode = st.radio("Mode", ['By year (months grouped)', 'By month (years grouped)'])

    if mode.startswith('By year'):
        years = sorted(df_long['year'].unique())
        if not years:
            st.warning("No years found in data.")
            st.stop()
        selected_year = st.selectbox("Select year", years, index=0)

        # aggregate
        df_f = df_long[df_long['year'] == selected_year]
        df_plot = df_f.groupby(['month','month_name','class'], as_index=False)['value'].sum()

        # pivot so classes are columns, months rows
        pivot = df_plot.pivot_table(index='month', columns='class', values='value', aggfunc='sum').fillna(0)

        # ensure months 1..12 order presence
        all_months = list(range(1,13))
        pivot = pivot.reindex(all_months, fill_value=0)

        x_labels = [months[m-1] for m in pivot.index]
        x = np.arange(len(x_labels))
        classes = list(pivot.columns)
        n = len(classes)
        if n == 0:
            st.warning("No class columns found to plot.")
            st.stop()

        bar_w = 0.8 / n
        fig, ax = plt.subplots(figsize=(10, 5))
        for i, cls in enumerate(classes):
            vals = pivot[cls].values
            ax.bar(x + i*bar_w, vals, width=bar_w, label=str(cls))
        ax.set_xticks(x + bar_w*(n-1)/2)
        ax.set_xticklabels(x_labels)
        ax.set_xlabel("Month")
        ax.set_ylabel("Value")
        ax.set_title(f"Values by month for year {selected_year}")
        ax.legend(title="Class")
        plt.tight_layout()
        st.pyplot(fig)

    else:  # By month mode
        month_choice = st.selectbox("Select month", list(enumerate(months, start=1)), format_func=lambda x: x[1])
        if isinstance(month_choice, tuple):
            selected_month = month_choice[0]
        else:
            selected_month = int(month_choice)

        df_f = df_long[df_long['month'] == selected_month]
        if df_f.empty:
            st.warning("No data for that month across years.")

        df_plot = df_f.groupby(['year','class'], as_index=False)['value'].sum()
        pivot = df_plot.pivot_table(index='year', columns='class', values='value', aggfunc='sum').fillna(0)
        years = list(pivot.index)
        x = np.arange(len(years))
        classes = list(pivot.columns)
        n = len(classes)
        if n == 0:
            st.warning("No class columns found to plot.")

        bar_w = 0.8 / n
        fig, ax = plt.subplots(figsize=(10, 5))
        for i, cls in enumerate(classes):
            vals = pivot[cls].values
            ax.bar(x + i*bar_w, vals, width=bar_w, label=str(cls))
        ax.set_xticks(x + bar_w*(n-1)/2)
        ax.set_xticklabels([str(y) for y in years], rotation=45)
        ax.set_xlabel("Year")
        ax.set_ylabel("Value")
        ax.set_title(f"Values by year for month {months[selected_month-1]}")
        ax.legend(title="Class")
        plt.tight_layout()
        st.pyplot(fig)