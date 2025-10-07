



# app.py
import streamlit as st
import pandas as pd
import altair as alt

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
