import streamlit as st
from streamlit_folium import folium_static
import folium
import pandas as pd
import json

# Function to create the folium map
def create_map(df):
    # Initialize a map. You might want to set a default location
    m = folium.Map(location=[51.4416, 5.4697], zoom_start=12, tiles="cartodb positron")

    # Loop through each neighborhood in the DataFrame
    for _, row in df.iterrows():
        # Extract GeoShape data
        geoshape_json = row['Geoshape']
        geoshape = json.loads(geoshape_json)

        # Create a polygon for each neighborhood and add it to the map
        folium.GeoJson(geoshape, name=row['NeighborhoodName']).add_to(m)  # Replace 'NeighborhoodName' with the actual column name

    return m

# Streamlit app
def app():
    st.title('Happiness in Eindhoven neighbourhoods')

    # Load your dataset
    df = pd.read_csv("data/tim_main_dataset.csv")  # Replace with your actual file path and name

    st_map = create_map(df)
    folium_static(st_map)

app()
