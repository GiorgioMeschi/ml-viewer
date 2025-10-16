



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


def plot_historical_stats(df):
    """
    Interactive chart version using Altair.
    """

    # ---------- reshape / parse ----------
    df.index.name = 'class'
    df_long = df.reset_index().melt(id_vars='class', var_name='year_month', value_name='value')

    def parse_ym(s):
        parts = str(s).split('_')
        if len(parts) == 2:
            try:
                return int(parts[0]), int(parts[1])
            except Exception:
                return None, None
        return None, None

    ym = df_long['year_month'].apply(lambda r: pd.Series(parse_ym(r)))
    ym.columns = ['year', 'month']
    df_long = pd.concat([df_long, ym], axis=1)
    df_long = df_long.dropna(subset=['year', 'month'])
    df_long['year'] = df_long['year'].astype(int)
    df_long['month'] = df_long['month'].astype(int)
    df_long['class'] = df_long['class'].astype(str)

    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    df_long['month_name'] = df_long['month'].apply(lambda m: months[m-1] if 1 <= m <= 12 else str(m))

    # ---------- UI ----------
    mode = st.radio("Mode", ['By year (months grouped)', 'By month (years grouped)'])

    # small helper to ensure there are classes
    if df_long['class'].nunique() == 0:
        st.warning("No class data available.")
        return

    # allow user to pick classes (optional)
    all_classes = sorted(df_long['class'].unique())
    chosen_classes = st.multiselect("Select classes to show (leave empty -> all)", options=all_classes, default=all_classes)
    if chosen_classes:
        df_long = df_long[df_long['class'].isin(chosen_classes)]
    else:
        st.warning("No classes selected. Showing all.")
        # (if empty selection, we keep original. you can also stop)

    if mode.startswith('By year'):
        years = sorted(df_long['year'].unique())
        if not years:
            st.warning("No years found in data.")
            return
        selected_year = st.selectbox("Select year", years, index=0)

        # aggregate
        df_f = df_long[df_long['year'] == selected_year]
        df_plot = df_f.groupby(['month','month_name','class'], as_index=False)['value'].sum()

        # ensure months 1..12 order presence (we'll use this order for x-axis)
        all_months = list(range(1,13))
        month_labels = [months[m-1] for m in all_months]

        if df_plot.empty:
            st.warning("No data for the selected year.")
            return

        # choose grouped or stacked
        barmode = st.selectbox("Bar mode", ["group", "stack"], index=0, help="group = side-by-side, stack = stacked bars")

        # prepare for Altair: month as ordered categorical so axis sorts correctly
        df_plot['month_ord'] = pd.Categorical(df_plot['month'].astype(int), categories=all_months, ordered=True)
        df_plot['month_label'] = df_plot['month_name'].astype(str)  # for tooltip

        # Altair grouped vs stacked
        if barmode == "group":
            # xOffset gives side-by-side grouped bars (requires altair/vega-lite support)
            chart = alt.Chart(df_plot).mark_bar().encode(
                x=alt.X('month_ord:O', title='Month',
                        axis=alt.Axis(labelAngle=0, tickCount=12, labelExpr="datum.label")),
                y=alt.Y('value:Q', title='Value'),
                color=alt.Color('class:N', title='Class'),
                tooltip=[alt.Tooltip('class:N'), alt.Tooltip('month_label:N', title='Month'), alt.Tooltip('value:Q')],
                xOffset='class:N'
            ).properties(
                width='container',
                height=450,
                title=f"Values by month for year {selected_year}"
            )
        else:
            # stacked bars
            chart = alt.Chart(df_plot).mark_bar().encode(
                x=alt.X('month_ord:O', title='Month',
                        axis=alt.Axis(labelAngle=0, tickCount=12)),
                y=alt.Y('value:Q', title='Value', stack='zero'),
                color=alt.Color('class:N', title='Class'),
                tooltip=[alt.Tooltip('class:N'), alt.Tooltip('month_label:N', title='Month'), alt.Tooltip('value:Q')]
            ).properties(
                width='container',
                height=450,
                title=f"Values by month for year {selected_year}"
            )

        # tidy up x-axis labels to actual month names
        # chart = chart.configure_axisX(labelFontSize=11)
        # show chart
        st.altair_chart(chart, use_container_width=True)

    else:  # By month mode
        month_options = [(i, months[i-1]) for i in range(1,13)]
        month_choice = st.selectbox("Select month", month_options, format_func=lambda x: x[1])
        if isinstance(month_choice, tuple):
            selected_month = month_choice[0]
        else:
            selected_month = int(month_choice)

        df_f = df_long[df_long['month'] == selected_month]
        if df_f.empty:
            st.warning("No data for that month across years.")
            return

        df_plot = df_f.groupby(['year','class'], as_index=False)['value'].sum()
        df_plot['year'] = df_plot['year'].astype(int)
        df_plot = df_plot.sort_values('year')

        years = sorted(df_plot['year'].unique())
        if len(years) == 0:
            st.warning("No year data for this month.")
            return

        barmode = st.selectbox("Bar mode", ["group", "stack"], index=0, help="group = side-by-side, stack = stacked bars")

        # prepare for Altair
        df_plot['year_ord'] = pd.Categorical(df_plot['year'].astype(str), categories=[str(y) for y in years], ordered=True)

        if barmode == "group":
            chart = alt.Chart(df_plot).mark_bar().encode(
                x=alt.X('year_ord:O', title='Year', axis=alt.Axis(labelAngle=0)),
                y=alt.Y('value:Q', title='Value'),
                color=alt.Color('class:N', title='Class'),
                tooltip=[alt.Tooltip('class:N'), alt.Tooltip('year:O', title='Year'), alt.Tooltip('value:Q')],
                xOffset='class:N'
            ).properties(width='container', height=450, title=f"Values by year for month {months[selected_month-1]}")
        else:
            chart = alt.Chart(df_plot).mark_bar().encode(
                x=alt.X('year_ord:O', title='Year', axis=alt.Axis(labelAngle=0)),
                y=alt.Y('value:Q', title='Value', stack='zero'),
                color=alt.Color('class:N', title='Class'),
                tooltip=[alt.Tooltip('class:N'), alt.Tooltip('year:O', title='Year'), alt.Tooltip('value:Q')],
            ).properties(width='container', height=450, title=f"Values by year for month {months[selected_month-1]}")

        st.altair_chart(chart, use_container_width=True)

