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
#import osgeo
import overpass
import io
import geojson
#from openrouteservice import client, places

"""

# Welcome to The Cville Tree Commission Neighborhood Tree App!!
Have a nice day Aloha
As part of the Charlottesville Tree Commission we're working to help the city of Charlottesville make greater value of the available local, regional, and national datasets in understanding tree ecosystems and canopy as it relates to public health and more equitable living experiences in our shared community.

One of the best local data sets is Charlottesville's own open data portal available here https://opendata.charlottesville.org

From this dataset hosted in ArcEsri's online data portal we can find files in CSV, geoJSON, .shp and many other standard geospatial data formats
For this example we will be using the neighborhood data to begin better understanding our community actions.
https://opendata.charlottesville.org/datasets/planning-neighborhood-area & thanks @https://twitter.com/jalbertbowdenii for tracking this down 

Another local ArcEsri database hosted at the University of Virginia is UVa's Equity Atlas https://equity-atlas-uvalibrary.opendata.arcgis.com/datasets/charlottesville::tree-inventory-point 

For this example we are pulling our tree point data (specifically only the publicly owned trees on city property... more on that later) to begin our analysis
test this

"""
trees=gpd.read_file("https://opendata.arcgis.com/datasets/e7c856379492408e9543a25d684b8311_79.geojson")
#zip_url = "http://widget.charlottesville.org/gis/zip_download/planning_area.zip"
cvillehoods = gpd.read_file("https://opendata.arcgis.com/datasets/c371ad0b81024822bad1147ff6bb24c4_51.geojson")

#overpass approach
api = overpass.API()
cvilleresult = api.get('way["place"="neighbourhood"](37.964522,-78.573741,38.097572,-78.415126);', responseformat="geojson", verbosity="geom")
#cvillefile = io.StringIO(cvilleresult)
st.write(type(cvilleresult))
#cvillegeo = gpd.read_file(api.get('way["place"="neighbourhood"](37.964522,-78.573741,38.097572,-78.415126);', responseformat="geojson", verbosity="geom"))
#https://gis.stackexchange.com/questions/130963/write-geojson-into-a-geojson-file-with-python




treetype = sorted(trees['Common_Name'].drop_duplicates()) # select all of the trees from the dataframe and filter by unique values and sorted alphabetically to create a useful dropdown menu list
tree_choice = st.sidebar.selectbox('Tree type:', treetype) # render the streamlit widget on the sidebar of the page using the list we created above for the menu
trees=trees[trees['Common_Name'].str.contains(tree_choice)] # create a dataframe for our deck.gl map to use in the layer as the data source and update it based on the selection made above

dotradius = st.sidebar.slider("Tree dot radius",1,100,50,1) # this creates a slider widget called "tree dot radius" with the format of "slider name", followed by the minimum value, the maximum value, the default value, and the incremental movement value
"""
And then we write the deck.gl layers from the geopandas dataframes using streamlit.io widgets to edit the data on the screen
"""

layer = [
    pdk.Layer(
        "GeoJsonLayer",
        data=cvillehoods,
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

"""
Testing geopandas sjoin - assigns a neighborhood to each tree point
"""
trees_in_hoods=gpd.sjoin(trees, cvillehoods, how='left', op='intersects')

"""
Neighborhood tree totals are counted
"""

st.write(trees_in_hoods['NAME'].value_counts())

"""
# Find a tree to see

to test out the open route service with our https://tasks.openstreetmap.us/projects/239/ Cville Sidewalk project we're testing code here from https://openrouteservice.org/


"""
#coords = ((8.34234,48.23424),(8.34423,48.26424), (8.34523,48.24424), (8.41423,48.21424))

#client = openrouteservice.Client(key='5b3ce3597851110001cf62482a2b0678ead546e5a27af36722c330c3') # Specify your personal API key
#routes = client.directions(coords, profile='cycling-regular', optimize_waypoints=True)

#print(routes)
