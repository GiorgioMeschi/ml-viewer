import geopandas as gpd
import pandas as pd
import folium
import branca
import streamlit.components.v1 as components

import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
import branca
import streamlit.components.v1 as components

st.title("RISK MAP")

uploaded = st.file_uploader("Upload GeoJSON", type=["geojson", "json"])
if not uploaded:
    st.info("Upload a GeoJSON file")
else:
    gdf = gpd.read_file(uploaded).to_crs("EPSG:4326")
    col = st.selectbox("Choose column to classify (5 classes)", ['risk', 'priority'])
    vals = gdf[col].astype(int, errors="ignore")

    # palette and colormap
    if col == 'risk':
        palette = ["#16f6e3", "#2abf13", "#f8c808", "#ec2712", "#6e0e10"]
        vmax = 5
    elif col == 'priority':
        palette = [ "#2abf13", "#f8c808", "#ec2712", "#6e0e10"]
        vmax = 4
    cmap = branca.colormap.StepColormap(colors=palette, vmin=1, vmax=vmax,
                                        index=list(range(1,vmax+1)), caption=f"{col}")

    # build map
    centroid = gdf.geometry[0].centroid
    m = folium.Map(location=[centroid.y, centroid.x], zoom_start=8)

    def style_fn(feat):
        cls = int(feat["properties"].get(col, 0) or 0)
        return {
            "fillColor": "#8c8c8c" if cls == 0 else cmap(cls),
            "color": "#444444",
            "weight": 0.6,
            "fillOpacity": 0.7,
        }

    tooltip = folium.GeoJsonTooltip(fields=["nome_comun", col],
                                    aliases=['comune', col], localize=True)

    folium.GeoJson(gdf.to_json(), name="Risk Liguria", style_function=style_fn, tooltip=tooltip, prefer_canvas=True).add_to(m) #prefer_canvas can speed up the loading 
    cmap.add_to(m)
    folium.LayerControl().add_to(m)

    components.html(m.get_root().render(), height=700, width = 2000, scrolling=True)


