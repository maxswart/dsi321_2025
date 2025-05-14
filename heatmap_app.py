import streamlit as st
import streamlit.components.v1 as components
import folium
from folium import Map
import geopandas as gpd
import pandas as pd
from datetime import datetime
from shapely.geometry import Point
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import os
import io

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

    return mymap, province_counts

# ---------- Streamlit App Layout ----------
def main():
    st.set_page_config(layout="wide")
    
    # Load data
    gdf = load_shapefile()
    parquet_files = load_parquet_data()

    # Date filter (we will grab values from session for now)
    filter_mode = st.sidebar.radio("Filter Mode", ['exact', 'range'])
    if filter_mode == 'range':
        start_date = st.sidebar.date_input("Start Date", datetime(2025, 5, 1))
        end_date = st.sidebar.date_input("End Date", datetime(2025, 5, 5))
        exact_date = None
    else:
        exact_date = st.sidebar.date_input("Exact Date", datetime(2025, 5, 1))
        start_date = end_date = None

    # Generate map and data
    mymap, province_counts_sorted = generate_heatmap(filter_mode, start_date, end_date, exact_date, gdf, parquet_files)

    # Get map HTML as string
    map_html = mymap.get_root().render()

    # Build overlay HTML
    overlay_html = f"""
    <div style="position: relative; width: 100%; height: 90vh;">
        {map_html}
        
        <!-- Floating Date UI -->
        <div style="position: absolute; top: 20px; left: 20px; background-color: rgba(255,255,255,0.9); padding: 15px; border-radius: 10px; z-index:9999; width: 280px; font-family: Arial;">
            <h4 style="margin-top:0;">📅 ตัวกรองวันที่</h4>
            <p style="margin: 0;"><b>โหมด:</b> {filter_mode}</p>
            <p style="margin: 0;"><b>เริ่ม:</b> {start_date if start_date else '-'}</p>
            <p style="margin: 0;"><b>สิ้นสุด:</b> {end_date if end_date else '-'}</p>
            <p style="margin: 0;"><b>วันที่:</b> {exact_date if exact_date else '-'}</p>
        </div>

        <!-- Floating Table -->
        <div style="position: absolute; top: 20px; right: 20px; background-color: rgba(255,255,255,0.9); padding: 15px; border-radius: 10px; z-index:9999; width: 300px; max-height: 80vh; overflow-y: auto; font-family: Arial;">
            <h4 style="margin-top:0;">🔥 จุดความร้อนรายจังหวัด</h4>
            <table style="width: 100%; border-collapse: collapse;">
                <thead><tr><th style="text-align:left;">จังหวัด</th><th>จำนวน</th></tr></thead>
                <tbody>
    """

    for _, row in province_counts_sorted.iterrows():
        overlay_html += f"<tr><td>{row['ADM1_TH']}</td><td>{row['heat_spot_count']}</td></tr>"

    overlay_html += """
                </tbody>
            </table>
        </div>
    </div>
    """

    # Show in Streamlit as raw HTML
    components.html(overlay_html, height=800, scrolling=False)

if __name__ == "__main__":
    main()
