import streamlit as st
import pandas as pd
import plotly.express as px
import json

# Function to create the Plotly map with GeoJSON
def create_map(df):
    # Assuming 'Geoshape' column contains stringified GeoJSON and 'NbName' is the identifier
    features = []
    for _, row in df.iterrows():
        geoshape_json = row['Geoshape']
        geoshape = json.loads({'type': 'Feature',
            'properties': {'name': row['NbName']},
            'geometry': json.loads(geoshape_json),
            'id': row["NbId"]})
        features.append(geoshape)
        if len(features) <= 5:
            print(geoshape)
    geojson = {'type': 'FeatureCollection', 'features': features}
    # Create a DataFrame for the locations
    locations_df = pd.DataFrame({
        'id': [feature['properties']['id'] for feature in features],
        'dummy_value': [1] * len(features)  # Plotly requires a value to color the shapes
    })

    fig = px.choropleth_mapbox(
        locations_df,
        geojson=geojson,
        color="dummy_value",
        locations="id",
        featureidkey="properties.id",
        center={"lat": 51.4416, "lon": 5.4697},  # Adjust as needed
        mapbox_style="open-street-map",
        zoom=10
    )

    return fig

# Streamlit app
def app():
    st.title('Happiness in Eindhoven Neighbourhoods')

    # Load your dataset
    df = pd.read_csv("data/tim_main_dataset.csv")  # Replace with your actual file path and name

    st_map = create_map(df)
    st.plotly_chart(st_map, use_container_width=True)

app()
