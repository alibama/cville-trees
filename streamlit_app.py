import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np
import fiona
import geopandas as gpd
import requests
import datetime
import json, re


"""
# Welcome to The Cville Tree Commission Neighborhood Tree App!
As part of the Charlottesville Tree Commission we're working to help the city of Charlottesville make greater value of the available local, regional, and national datasets in understanding tree ecosystems and canopy as it relates to public health and more equitable living experiences in our shared community.

One of the best local data sets is Charlottesville's own open data portal available here https://opendata.charlottesville.org/pages/download-gis-data-shp-cad
From this dataset hosted in ArcEsri's online data portal we can find files in CSV, geoJSON, .shp and many other standard geospatial data formats
For this example we will be using the neighborhood data to begin better understanding our community actions.


Another local ArcEsri database hosted at the University of Virginia is UVa's Equity Atlas https://equity-atlas-uvalibrary.opendata.arcgis.com/datasets/charlottesville::tree-inventory-point and tools like https://opendata.charlottesville.org/pages/download-gis-data-shp-cad
For this example we are pulling our tree point data (specifically only the publicly owned trees on city proprty... more on that later) to begin our analysis



"""


trees=gpd.read_file("https://opendata.arcgis.com/datasets/e7c856379492408e9543a25d684b8311_79.geojson")


"""
https://gis.stackexchange.com/questions/225586/reading-raw-data-into-geopandas and then i read this fine manual and it's really simple to import shape files straight from zip in to geopandas
"""

zip_url = 'http://widget.charlottesville.org/gis/zip_download/planning_area.zip'
cvillehoods = gpd.read_file(zip_url)


trees_in_hoods=gpd.sjoin(trees, cvillehoods, how="inner", op='intersects')

test=trees_in_hoods.head()
test
#st.map(cvillehoods)


      






today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
start_date = st.date_input('Start date', today)
end_date = st.date_input('End date', tomorrow)
if start_date < end_date:
    st.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
else:
    st.error('Error: End date must fall after start date.')
