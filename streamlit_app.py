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
