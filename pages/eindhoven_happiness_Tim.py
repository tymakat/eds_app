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
        geoshape = {'type': 'Feature',
            'properties': {'name': row['NbName']},
            'id': row["NbId"],
            'geometry': row["Geoshape"]}
        features.append(geoshape)
        if len(features) <= 5:
            print(geoshape)
    geojson = {'type': 'FeatureCollection', 'features': features}
    # Create a DataFrame for the locations

   #/* fig = px.choropleth_mapbox(
     #   locations_df,
      #  geojson=geojson,
     #   color="dummy_value",
     #   locations="id",
     #   featureidkey="properties.id",
    #    center={"lat": 51.4416, "lon": 5.4697},  # Adjust as needed
    #    mapbox_style="open-street-map",
   #     zoom=10
  #  ) */
    fig = px.choropleth(df, geojson=geojson, locations='NbId', color='unemp',
                            color_continuous_scale="Viridis",
                            range_color=(0, 12),
                            center={"lat": 51.4416, "lon": 5.4697},  # Adjust as needed
                            labels={'Happiness':'Happiness rate'},
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
