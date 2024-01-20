import streamlit as st
import pandas as pd
import plotly.express as px
import json
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

plt.rcParams['text.color'] = 'black'
plt.rcParams['axes.labelcolor'] = 'black'
plt.rcParams['xtick.color'] = 'black'
plt.rcParams['ytick.color'] = 'black'

st.set_page_config(layout="wide")
# Function to create the Plotly map with GeoJSON
def create_map(df):
    # Assuming 'Geoshape' column contains stringified GeoJSON and 'NbName' is the identifier
    features = []
    for _, row in df.iterrows():
        geoshape_json = json.loads(row["Geoshape"])
        geoshape = {'type': 'Feature',
            'properties': {'name': row['Neighbourhood']},
            'id': row["NbId"],
            'geometry': geoshape_json}
        features.append(geoshape)
        if len(features) <= 5:
            print(geoshape)
    geojson = {'type': 'FeatureCollection', 'features': features}
    # Create a DataFrame for the locations
    color_scale = [
    (0, "grey"),  # Color for 0 values
    # Define other colors for the rest of your scale
    (0.72, "red"),  # Example: Color for values > 0
    (0.88, "white"),
    (1, "green") # Ensure the scale covers the full range of your data
    ]
    fig = px.choropleth_mapbox(
        df,
        geojson=geojson,
        color='Happiness score',
        color_continuous_scale=color_scale,
        locations="NbId",
        featureidkey="id",
        center={"lat": 51.4416, "lon": 5.4697},
        hover_data=['Neighbourhood', 'Happiness', "Happiness rank", "Happiness score"], # Adjust as needed
        mapbox_style="open-street-map",
        zoom=11.8,
        opacity=0.8
    )
    
    fig.update_layout(
        height=1000,  # Set the height of the map in pixels
        width=1000    # Set the width of the map in pixels
    )
    fig.update_traces(
    hoverlabel=dict(font_size=15)  
    # Adjust the font size as needed
    )

    return fig

# Streamlit app
def app():
    st.title('Happiness in Eindhoven Neighbourhoods')

    # Load your dataset
    df = pd.read_csv("data/tim_main_dataset.csv")  # Replace with your actual file path and name
    df_top_30 = df.head(30)
    value_counts = df_top_30['Preferrable type of transport'].value_counts()
    st_map = create_map(df)
    st.plotly_chart(st_map, use_container_width=True)
    st.markdown("#### Preferrable transport type of top-30 happiest Eindhoven districts")
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_facecolor('#0E1117')
    explode = (0, 0.1, 0, 0)
    colors = ['#e1e9f5','#7792bd','#2f4f82','#062454']
    
    # Create a pie chart on the axis
    ax.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%', explode=explode, shadow=True, startangle=90, colors = colors)
    ax.legend()
    # Display the plot in Streamlit
    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.image(buf)
    
app()
