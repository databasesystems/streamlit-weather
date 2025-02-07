import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# Function to fetch weather data
def get_weather_data(latitude, longitude):
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
        "forecast_days": 1
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {e}")
        return None

# Initialize geolocator
geolocator = Nominatim(user_agent="weather_app")

st.title("Weather App")

# Default map location
default_latitude = 51.5074
default_longitude = 0.1278

# Initialize session state for storing the last clicked marker
if "marker_data" not in st.session_state:
    st.session_state.marker_data = None

# Display the map and capture clicks
m = folium.Map(location=[default_latitude, default_longitude], zoom_start=10)

if st.session_state.marker_data:
    lat = st.session_state.marker_data["lat"]
    lon = st.session_state.marker_data["lon"]
    popup = st.session_state.marker_data["popup"]
    folium.Marker(location=[lat, lon], popup=popup).add_to(m)

# Capture click events
output = st_folium(m, width=700, height=500, key="map")

# Handle map clicks
if output and output.get("last_clicked"):
    clicked_lat = output["last_clicked"]["lat"]
    clicked_lon = output["last_clicked"]["lng"]

    # Get location name
    try:
        location = geolocator.reverse((clicked_lat, clicked_lon))
        place_name = location.address if location else "Unknown Location"
    except Exception as e:
        place_name = f"Error: {e}"

    # Fetch weather data
    weather_data = get_weather_data(clicked_lat, clicked_lon)

    if weather_data:
        current = weather_data.get("current_weather", {})
        temperature = current.get('temperature', 'N/A')
        windspeed = current.get('windspeed', 'N/A')

        popup_content = f"<b>{place_name}</b><br>Temperature: {temperature} °C<br>Wind Speed: {windspeed} m/s"

        # Store marker data in session state
        st.session_state.marker_data = {"lat": clicked_lat, "lon": clicked_lon, "popup": popup_content}

    # **Force page rerun to update the displayed marker**
    st.rerun()
