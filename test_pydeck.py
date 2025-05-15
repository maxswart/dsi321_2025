import streamlit as st
import pydeck as pdk
import pandas as pd
import geopandas as gpd
from datetime import datetime
from shapely.geometry import Point
from streamlit_folium import folium_static
import os

# ---------- Load shapefile function ----------
@st.cache_data
def load_shapefile():
    shapefile_path = r"C:\Users\guy88\private_file\study_file\DSI321\project\heat_spot_map\shape_file\tha_admbnda_adm1_rtsd_20220121.shp"
    gdf = gpd.read_file(shapefile_path)
    gdf = gdf.drop(columns=gdf.select_dtypes(include=['datetime64']).columns)
    gdf = gdf.to_crs(epsg=4326)
    return gdf

# ---------- Load Parquet data function ----------
@st.cache_data
def load_parquet_data_combined():
    dfs = []
    root_dir = r'C:\Users\guy88\private_file\study_file\DSI321\project\heat_spot_map\df_thai'
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.parquet'):
                df = pd.read_parquet(os.path.join(root, file))
                dfs.append(df)
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df['acq_date'] = pd.to_datetime(combined_df['acq_date']).dt.date
    return combined_df


# ---------- Function to generate the heatmap based on selected date ----------
# Function to generate the heatmap with PyDeck
def generate_heatmap(df, filter_mode, start_date, end_date, exact_date, gdf):
    # Filter data by date range or exact date
    if filter_mode == 'range':
        df_filtered = df[(df['acq_date'] >= start_date) & (df['acq_date'] <= end_date)]
    else:
        df_filtered = df[df['acq_date'] == exact_date]
    
    if df_filtered.empty:
        return None

    # Prepare heatmap data (normalize brightness)
    heat_data = df_filtered[['latitude', 'longitude', 'brightness']]
    heat_data['weight'] = (heat_data['brightness'] - 250) / (400 - 250)  # Normalize brightness

    # Create the heatmap layer (PyDeck v0.7+)
    heatmap_layer = pdk.Layer(
        "HeatmapLayer",
        data=heat_data,
        get_position=["longitude", "latitude"],
        get_weight="weight",
        radius_pixels=50,
        opacity=0.8,
        threshold=0.1
    )

    # Set the view for the map
    view_state = pdk.ViewState(
        latitude=13.7367,  # Center on Bangkok
        longitude=100.5231,
        zoom=6,
        pitch=0,
    )

    # Create the deck with the layer
    deck = pdk.Deck(
        initial_view_state=view_state,
        layers=[heatmap_layer],  # Pass the layer as a list
        tooltip={"text": "{weight}"}
    )

    return deck


# ---------- Streamlit App Layout ----------
def main():
    st.set_page_config(layout="wide")

    # Load data
    df = load_parquet_data_combined()
    gdf = load_shapefile()

    # Date filter (we will grab values from session for now)
    filter_mode = st.sidebar.radio("Filter Mode", ['exact', 'range'])
    if filter_mode == 'range':
        start_date = st.sidebar.date_input("Start Date", datetime(2025, 5, 1).date())
        end_date = st.sidebar.date_input("End Date", datetime(2025, 5, 5).date())
        exact_date = None
    else:
        exact_date = st.sidebar.date_input("Exact Date", datetime(2025, 5, 1).date())
        start_date = end_date = None

    # Generate heatmap
    deck = generate_heatmap(df, filter_mode, start_date, end_date, exact_date, gdf)

    if deck:
        st.pydeck_chart(deck)
    else:
        st.write("No data to display for the selected range.")


if __name__ == "__main__":
    main()
