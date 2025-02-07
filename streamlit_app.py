import streamlit as st
import pandas as pd
import requests
import pydeck as pdk
import geopy
from geopy.geocoders import Nominatim

# Function to fetch weather data from Open-Meteo API
def get_weather_data(latitude, longitude):
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
        "hourly": "temperature_2m,relativehumidity_2m,windspeed_10m",
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

# Initialize geolocator for address lookup
geolocator = Nominatim(user_agent="weather_app")  # Important: Provide a user agent

st.title("Weather App")

# Default map location (London)
default_latitude = 51.5074
default_longitude = 0.1278

# Initialize clicked_point in session state
if "clicked_point" not in st.session_state:
    st.session_state.clicked_point = None

# Create Pydeck map
view_state = pdk.ViewState(latitude=default_latitude, longitude=default_longitude, zoom=10)
layers = [
    pdk.Layer(
        "ScatterplotLayer",
        data=[],  # Empty initially
        get_position=lambda x: [x["lon"], x["lat"]],
        get_radius=500,
        get_fill_color=[255, 0, 0, 100],
        pickable=True,
    ),
]

# Display the Pydeck map
st.pydeck_chart(
    pdk.Deck(layers=layers, initial_view_state=view_state),
    events=["click"],
)


# Address input
address = st.text_input("Enter an address:")

if address:
    try:
        location = geolocator.geocode(address)
        if location:
            latitude = location.latitude
            longitude = location.longitude

            # Update map view
            view_state = pdk.ViewState(latitude=latitude, longitude=longitude, zoom=10)
            st.pydeck_chart(pdk.Deck(layers=layers, initial_view_state=view_state)) # Update the map to the new location

            weather_data = get_weather_data(latitude, longitude)
            if weather_data:
                # ... (display weather data - same as before)
                st.subheader(f"Weather at: {latitude:.2f}, {longitude:.2f} (from address)")
                current = weather_data.get("current_weather", {})
                if current:
                    st.write(f"Temperature: {current.get('temperature', 'N/A')} °C")
                    st.write(f"Wind Speed: {current.get('windspeed', 'N/A')} m/s")

                hourly = weather_data.get("hourly", {})
                if hourly:
                  st.subheader("Hourly Forecast")
                  hourly_data = pd.DataFrame(hourly)
                  st.dataframe(hourly_data)

        else:
            st.error("Address not found.")
    except Exception as e:
        st.error(f"Geocoding error: {e}")



# Handle map clicks (same as before)
if st.session_state.get("pydeck_click"):
    click_info = st.session_state.pydeck_click
    latitude = click_info.get("latitude")
    longitude = click_info.get("longitude")

    if latitude and longitude:
        st.session_state.clicked_point = {"lat": latitude, "lon": longitude}

        weather_data = get_weather_data(latitude, longitude)

        if weather_data:
            st.subheader(f"Weather at: {latitude:.2f}, {longitude:.2f} (from click)") # Indicate it's from a click

            current = weather_data.get("current_weather", {})
            if current:
                st.write(f"Temperature: {current.get('temperature', 'N/A')} °C")
                st.write(f"Wind Speed: {current.get('windspeed', 'N/A')} m/s")

            hourly = weather_data.get("hourly", {})
            if hourly:
              st.subheader("Hourly Forecast")
              hourly_data = pd.DataFrame(hourly)
              st.dataframe(hourly_data)

        st.session_state.pydeck_click = None