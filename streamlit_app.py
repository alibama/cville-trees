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
import pyproj
from shapely.ops import orient # https://gis.stackexchange.com/questions/336477/how-to-apply-the-orient-function-on-the-geometry-of-a-geopandas-dataframe
import osgeo
#from osgeo import gdal
#import gdal
import overpass
import io
"""
# Welcome to The Cville Tree Commission Neighborhood Tree App!
As part of the Charlottesville Tree Commission we're working to help the city of Charlottesville make greater value of the available local, regional, and national datasets in understanding tree ecosystems and canopy as it relates to public health and more equitable living experiences in our shared community.

One of the best local data sets is Charlottesville's own open data portal available here https://opendata.charlottesville.org/pages/download-gis-data-shp-cad
From this dataset hosted in ArcEsri's online data portal we can find files in CSV, geoJSON, .shp and many other standard geospatial data formats
For this example we will be using the neighborhood data to begin better understanding our community actions.


Another local ArcEsri database hosted at the University of Virginia is UVa's Equity Atlas https://equity-atlas-uvalibrary.opendata.arcgis.com/datasets/charlottesville::tree-inventory-point and tools like https://opendata.charlottesville.org/pages/download-gis-data-shp-cad
For this example we are pulling our tree point data (specifically only the publicly owned trees on city property... more on that later) to begin our analysis

https://gis.stackexchange.com/questions/225586/reading-raw-data-into-geopandas is a quick tutorial for getting data in to https://geopandas.org/ 

This is a quick look at finding publicly managed trees in cville using the https://deck.gl/ library & https://www.streamlit.io/

"""
trees=gpd.read_file("https://opendata.arcgis.com/datasets/e7c856379492408e9543a25d684b8311_79.geojson")
#zip_url = "http://widget.charlottesville.org/gis/zip_download/planning_area.zip"

api = overpass.API()
cvilleresult = api.get('way["place"="neighbourhood"](37.964522,-78.573741,38.097572,-78.415126);', responseformat="geojson", verbosity="geom")
#cvillefile = io.StringIO(cvilleresult)
st.write(type(cvilleresult))

"""
Testing geopandas & libspatialindex
"""
#trees_in_hoods=gpd.sjoin(trees, cvillegeo, how='inner', op='contains')
#trees_in_hoods
treetype = sorted(trees['Common_Name'].drop_duplicates()) # select all of the trees from the dataframe and filter by unique values and sorted alphabetically to create a useful dropdown menu list
tree_choice = st.sidebar.selectbox('Tree type:', treetype) # render the streamlit widget on the sidebar of the page using the list we created above for the menu
trees=trees[trees['Common_Name'].str.contains(tree_choice)] # create a dataframe for our deck.gl map to use in the layer as the data source and update it based on the selection made above

dotradius = st.sidebar.slider("Tree dot radius",1,100,50,1) # this creates a slider widget called "tree dot radius" with the format of "slider name", followed by the minimum value, the maximum value, the default value, and the incremental movement value
"""
this should work. #https://gis.stackexchange.com/questions/255586/gdal-vectortranslate-returns-empty-object
"""


layer = [
    pdk.Layer(
        "GeoJsonLayer",
        data=cvilleresult,
        getFillColor=[60, 220, 255],
 
    ),
    pdk.Layer(
        "GeoJsonLayer",
        data=trees,
        getFillColor=[20, 20, 123],
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
    tooltip={"html": "<b>Tree species:</b> {tree_choice}", "style": {"color": "white"}},
)
st.pydeck_chart(r)

import os
import base64


def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href
st.markdown(get_binary_file_downloader_html('cvillehoods.geojson', 'data'), unsafe_allow_html=True)
