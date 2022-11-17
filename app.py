import streamlit as st
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
from streamlit_folium import st_folium
import folium
import requests
import json
from datetime import timedelta
from geopy import Nominatim
# import certifi


st.set_page_config()

st.title('Capstone')
st.markdown("""
Description ....


**Data source:** link
""")

# load the data
@st.cache
def get_data(filename):
	df = pd.read_csv(filename)
	return df

# 1st data set
df = get_data('usgs_data.csv')

# 2nd data set
df2 = get_data('nyserda_data.csv')

st.header("Map 1")


mmap = folium.Map(location = [windfarm1.latitude.mean(), windfarm1.longitude.mean()], zoom_start=7, control_scale=True)

group0 = folium.FeatureGroup(name='<span style=\\"color: blue;\\">Exist Projects</span>')
for index, location_info in windfarm1.iterrows():

    folium.CircleMarker(
        location = [location_info["latitude"], location_info["longitude"]], 
        radius = location_info['numb_turbines']/2,
        fill_color ='blue',
        popup = folium.Popup(location_info["text"], min_width=250, max_width=250)
        ).add_to(group0)
group0.add_to(map)

group1 = folium.FeatureGroup(name='<span style=\\"color: orange;\\">Future Projects</span>')
for index, location_info in windfarm2.iterrows():
    if pd.notnull(location_info['latitude']):
        folium.CircleMarker(
        location = [location_info["latitude"], location_info["longitude"]], 
        radius = 5,
        color = 'orange',
        fill_color ='red',
        popup = folium.Popup(location_info["text"], min_width=250, max_width=250)
        ).add_to(group1)
group1.add_to(map)

folium.map.LayerControl('topleft', collapsed=False).add_to(map)
map


st_data = st_folium(map, width = 725)


st.header("Map 2")

# add the 1st selectbox for selecting the project
column1 = df['p_name'].unique().tolist()
option1 = st.selectbox(
    'Select a project',
    column1)
df_selected1 = df.loc[df.p_name == option1]

# add the 2nd selectbox for selecting the exact turbine of the selecting project
column2 = df.loc[df['p_name'] == option1]['case_id'].tolist()
option2 = st.selectbox(
    'Select a case ID',
    column2)  
df_selected2 = df_selected1.loc[df.case_id == option2]
st.write(df_selected2)

df_selected2.rename(columns={'xlong':'longitude', 'ylat':'latitude'}, inplace=True)
Origin = float(df_selected2.latitude),float(df_selected2.longitude)

# add a text input box for inputing a destination location
input = st.text_input("Input a destination (For example, 'Delaware Park, Buffalo, NY') ")
locator = Nominatim(user_agent='myGeocoder')
location = locator.geocode(str(input))

# get latitude, longitude and distance of the destination
def TravelInfo(origin, destination):
  
  """
  orgin: (x,y) where x and y represent latitude and longitude respectively
  destination: (x,y) where x and y represent latitude and longitude respectively
  """
  # Unpack the latitudes and longitudes
  (lat1, lon1) = origin
  (lat2, lon2) = destination
  # Make API call to OSRM (Open Source Routing Machine) for travel info
  r = requests.get(f"""http://router.project-osrm.org/route/v1/car/{lon1},{lat1};{lon2},{lat2}?overview=false""")
  # Unpack desired info
  route_1 = json.loads(r.content)["routes"][0]
  distance = route_1['distance']
  duration = route_1['duration']
  # Print output
  st.write(f"Driving Distance (mi): {distance/1609}")
  st.write(f"Driving Time: {str(timedelta(seconds=duration))}")
  return None

# create a map
if location is None:
    map = folium.Map(location = Origin, zoom_start=7, control_scale=True)
    folium.Marker(Origin, popup="Origin").add_to(map)
    st.write("Please Enter a Destination")
else:
    Destination = float(location.latitude),float(location.longitude)
    TravelInfo(Origin, Destination)
    map = folium.Map(location = Origin, zoom_start=7, control_scale=True)
    folium.Marker(Origin, popup="Origin").add_to(map)
    folium.Marker(Destination, popup="Destination").add_to(map)
    folium.PolyLine([Origin, Destination],color='red').add_to(map)
    
st_data = st_folium(map, width = 725)










