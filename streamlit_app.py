import math
import pandas as pd
import streamlit as st
import numpy as np
import fiona
import geopandas as gpd
import requests
import datetime
import json, re
import pydeck as pdk

"""
# Welcome to The Cville Neighborhood Tree App!

First up a thank you to the Claude Moore Health Science Library for supporting open source and open science. For anyone interested in learning more I'm teaching a short course on this coming up in January

https://cal.hsl.virginia.edu/event/7280134

The Charlottesville Tree Commission is helping the City of Charlottesville understand our tree ecosystems to better public health and provide more equitable living experiences. 
To do this we are merging the available local, regional, and national tree canopy and municiple datasets.

One of the best local data sets is Charlottesville's own open data portal available here https://opendata.charlottesville.org/pages/download-gis-data-shp-cad
From this dataset hosted in ArcEsri's online data portal we can find files in CSV, geoJSON, .shp and many other standard geospatial data formats
For this example we will be using the neighborhood data to begin better understanding our community actions.

Another local ArcEsri database hosted at the University of Virginia is UVa's Equity Atlas https://equity-atlas-uvalibrary.opendata.arcgis.com/datasets/charlottesville::tree-inventory-point and tools like https://opendata.charlottesville.org/pages/download-gis-data-shp-cad
For this example we are pulling our tree point data (specifically only the publicly owned trees on city property... more on that later) to begin our analysis

For information on how this app was built https://guides.hsl.virginia.edu/it-services-blog/zoombites/Geopandas-and-streamlit-to-display-local-tree-data-in-deckgl

https://gis.stackexchange.com/questions/225586/reading-raw-data-into-geopandas is a tutorial for getting data in to https://geopandas.org/ 

This is a quick look at finding publicly managed trees in cville using the https://deck.gl/ library & https://www.streamlit.io/

"""
trees=gpd.read_file("https://opendata.arcgis.com/datasets/e7c856379492408e9543a25d684b8311_79.geojson")
zip_url = "http://widget.charlottesville.org/gis/zip_download/planning_area.zip"
cvillehoods = gpd.read_file(zip_url)


"""
Testing geopandas & libspatialindex
"""
trees_in_hoods=gpd.sjoin(trees, cvillehoods, how='inner', op='contains')

treetype = sorted(trees['Common_Name'].drop_duplicates()) # select all of the trees from the dataframe and filter by unique values and sorted alphabetically to create a useful dropdown menu list
tree_choice = st.sidebar.selectbox('Tree type:', treetype) # render the streamlit widget on the sidebar of the page using the list we created above for the menu
trees=trees[trees['Common_Name'].str.contains(tree_choice)] # create a dataframe for our deck.gl map to use in the layer as the data source and update it based on the selection made above

dotradius = st.sidebar.slider("Tree dot radius",1,100,50,1) # this creates a slider widget called "tree dot radius" with the format of "slider name", followed by the minimum value, the maximum value, the default value, and the incremental movement value

layer = [
    pdk.Layer(
        "GeoJsonLayer",
        data=trees,
        getFillColor=[60, 220, 255],
        getRadius=dotradius, #here's the streamlit slider widget being used to determine the size of the point on the deckgl map
    ),

]

# Set the viewport location
view_state = pdk.ViewState(
    longitude=-78.507980, latitude=38.033554, zoom=12, min_zoom=5, max_zoom=15, pitch=20.5, bearing=27.36
)

# Combined all of it and render a viewport
r = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    layers=[layer],
    initial_view_state=view_state,
)
st.pydeck_chart(r)
