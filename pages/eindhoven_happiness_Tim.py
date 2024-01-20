import streamlit as st
import pandas as pd
import plotly.express as px
import json

# Function to create the Plotly map with GeoJSON
def create_map(df):
    # List to hold the GeoJSON features
    features = []

    # Loop through DataFrame and convert each row's GeoJSON to a feature
    for _, row in df.iterrows():
        geoshape_json = row['Geoshape']
        geoshape = json.loads(geoshape_json)

        # Add the neighborhood name as a property (for the hover information)
        geoshape['properties'] = {'name': row['NbName']}

        features.append(geoshape)
    
    if len(features) <= 5:
        print(geoshape)

    # Create a GeoJSON object with all the features
    geojson = {'type': 'FeatureCollection', 'features': features}

    # Create the map using Plotly
    fig = px.choropleth_mapbox(geojson,
                               geojson=geojson,
                               locations=[feature['properties']['name'] for feature in features],
                               featureidkey="properties.name",
                               center={"lat": 51.4416, "lon": 5.4697},  # Center of the map
                               mapbox_style="open-street-map",
                               zoom=10,
                               
                               opacity=0.5)

    return fig

# Streamlit app
def app():
    st.title('Happiness in Eindhoven Neighbourhoods')

    # Load your dataset
    df = pd.read_csv("data/tim_main_dataset.csv")  # Replace with your actual file path and name

    st_map = create_map(df)
    st.plotly_chart(st_map, use_container_width=True)

app()
