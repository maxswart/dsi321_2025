import streamlit as st
import folium
import geopandas as gpd
import pandas as pd
from datetime import datetime
from shapely.geometry import Point
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import os

# ---------- Load shapefile function ----------
@st.cache_data
def load_shapefile():
    shapefile_path = r"C:\Users\guy88\private_file\study_file\DSI321\project\heat_spot_map\shape_file\tha_admbnda_adm1_rtsd_20220121.shp"
    gdf = gpd.read_file(shapefile_path)
    gdf = gdf.drop(columns=gdf.select_dtypes(include=['datetime64']).columns)
    gdf = gdf.to_crs(epsg=4326)  # Ensure CRS is WGS84 (lat, lon)
    return gdf

# ---------- Load Parquet data function ----------
@st.cache_data
def load_parquet_data():
    parquet_files = set()
    root_dir = r'C:\Users\guy88\private_file\study_file\DSI321\project\heat_spot_map\df_thai'
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.parquet'):
                file_path = os.path.join(root, file)
                parquet_files.add(file_path)
    return parquet_files


# ---------- Function to generate the heatmap based on selected date ----------
def generate_heatmap(filter_mode, filter_date_start, filter_date_end, filter_date_exact, gdf, parquet_files):
    # Initialize the folium map
    map_center = [13.7367, 100.5231]  # Bangkok
    zoom_level = 6
    mymap = folium.Map(location=map_center, zoom_start=zoom_level)

    # Prepare fire points data for heatmap
    heat_data = []
    
    for file_path in parquet_files:
        try:
            df = pd.read_parquet(file_path)
            df['acq_date'] = pd.to_datetime(df['acq_date']).dt.date

            # Apply the date filter
            if filter_mode == 'exact':
                df = df[df['acq_date'] == filter_date_exact]
            elif filter_mode == 'range':
                df = df[(df['acq_date'] >= filter_date_start) & (df['acq_date'] <= filter_date_end)]

            if 'latitude' in df.columns and 'longitude' in df.columns and not df.empty:
                for _, row in df.iterrows():
                    lat = row['latitude']
                    lon = row['longitude']
                    brightness = row['brightness'] if 'brightness' in row else 1
                    heat_data.append([lat, lon, brightness])

        except Exception as e:
            st.error(f"Error processing {file_path}: {e}")
    
    # Create GeoDataFrame for heat points
    heat_points = gpd.GeoDataFrame(
        geometry=[Point(lon, lat) for lat, lon, _ in heat_data],
        crs="EPSG:4326"
    )

    # Spatial join to get heat spots within provinces
    joined = gpd.sjoin(heat_points, gdf, how="left", predicate="within")

    # Count heat spots per province
    province_counts = joined['ADM1_TH'].value_counts().reset_index()
    province_counts.columns = ['ADM1_TH', 'heat_spot_count']

    # Merge heat counts with the original GeoDataFrame
    gdf = gdf.merge(province_counts, on='ADM1_TH', how='left')
    gdf['heat_spot_count'] = gdf['heat_spot_count'].fillna(0).astype(int)

    # Add Province boundaries to the map
    folium.GeoJson(
        gdf,
        name='Provinces',
        tooltip=folium.GeoJsonTooltip(fields=['ADM1_TH', 'heat_spot_count'], aliases=['Province', 'Heat Spots']),
        style_function=lambda x: {
            'fillColor': '#e6bead',
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 0.1
        }
    ).add_to(mymap)

    # Normalize and add HeatMap layer
    min_b, max_b = 250, 400
    normalized_heat_data = []
    for lat, lon, brightness in heat_data:
        b = max(min_b, min(brightness, max_b))
        weight = (b - min_b) / (max_b - min_b)
        normalized_heat_data.append([lat, lon, weight])

    gradient = {
        "0.2": "#FFA500",
        "0.5": "#FF4500",
        "0.8": "#FF0000",
        "1.0": "#8B0000"
    }

    if normalized_heat_data:
        HeatMap(
            normalized_heat_data,
            radius=10,
            blur=15,
            max_zoom=7,
            gradient=gradient
        ).add_to(mymap)

    return mymap

# ---------- Streamlit App Layout ----------
def main():
    st.title("Thailand Heat Spot Map")

    # Load data
    gdf = load_shapefile()
    parquet_files = load_parquet_data()

    # Sidebar Date Filters
    filter_mode = st.sidebar.radio("Select Date Filter Mode", ('exact', 'range'))

    if filter_mode == 'range':
        filter_date_start = st.sidebar.date_input("Start Date", datetime(2025, 5, 1))
        filter_date_end = st.sidebar.date_input("End Date", datetime(2025, 5, 5))
        filter_date_exact = None
    elif filter_mode == 'exact':
        filter_date_exact = st.sidebar.date_input("Select Date", datetime(2025, 4, 2))
        filter_date_start = filter_date_end = None

    # Generate heatmap based on user input
    mymap = generate_heatmap(filter_mode, filter_date_start, filter_date_end, filter_date_exact, gdf, parquet_files)

    # Display the map
    folium_static(mymap)

if __name__ == "__main__":
    main()
