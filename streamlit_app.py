import streamlit as st

# Streamlit page settings
st.set_page_config(layout="wide")

st.title("🌍 Interactive Weather Map")
st.subheader("Click on the map to get weather details")

with st.sidebar:
    st.header("⚙️ Map Controls")
    st.write("More controls will be added here.")

# Open-Meteo API endpoint
API_ENDPOINT = "https://api.open-meteo.com/v1/forecast"

# HTML + JavaScript for Leaflet Map
leaflet_code = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Weather Map</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        .map-container {{
            width: 100% !important;
            height: 75vh !important;
        }}
    </style>
</head>
<body>
    <div id="map-container" class="map-container"></div>
    <script>
        var map = L.map('map-container').setView([51.5074, 0.1278], 6);

        // Tile Layers
        var osmLayer = L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '&copy; OpenStreetMap contributors'
        }}).addTo(map);

        var satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}', {{
            attribution: 'Tiles &copy; Esri'
        }});

        var baseLayers = {{
            "OpenStreetMap": osmLayer,
            "Satellite": satelliteLayer
        }};
        L.control.layers(baseLayers).addTo(map);

        var markerGroup = L.layerGroup().addTo(map);

        map.on('click', function(e) {{
            var lat = e.latlng.lat;
            var lon = (e.latlng.lng + 180) % 360 - 180; // Normalize longitude

            markerGroup.clearLayers();

            // Reverse Geocoding
            fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${{lat}}&lon=${{lon}}`)
                .then(response => response.json())
                .then(geocodingData => {{
                    var placeName = "Unknown Location";
                    if (geocodingData && geocodingData.address) {{
                        placeName = geocodingData.address.road || 
                                    geocodingData.address.suburb || 
                                    geocodingData.address.city || 
                                    geocodingData.address.county || 
                                    geocodingData.address.country ||
                                    "Unnamed Place";
                    }}

                    // Fetch Weather Data
                    fetch('{API_ENDPOINT}?latitude=' + lat + '&longitude=' + lon + '&current_weather=true&forecast_days=1')
                        .then(response => response.json())
                        .then(data => {{
                            if (data && data.current_weather) {{
                                var temp = data.current_weather.temperature;
                                var windspeed = data.current_weather.windspeed;

                                var popupContent = `
                                    <div style="font-family: Arial, sans-serif; font-size: 14px; padding: 5px; text-align: center;">
                                        <b style="font-size: 16px; color: #333;">📍 ${{placeName}}</b>
                                        <hr style="margin: 5px 0;">
                                        <div style="display: flex; align-items: center; justify-content: space-between;">
                                            <span style="font-size: 18px;">🌡️ <b>${{temp}}°C</b></span>
                                            <span style="font-size: 18px;">🌬️ <b>${{windspeed}} m/s</b></span>
                                        </div>
                                    </div>
                                `;

                                L.marker([lat, lon]).addTo(markerGroup).bindPopup(popupContent).openPopup();
                            }} else {{
                                console.error("Weather data unavailable.");
                            }}
                        }})
                        .catch(error => console.error("Weather API Error:", error));
                }})
                .catch(error => console.error("Geocoding Error:", error));
        }});
    </script>
</body>
</html>
"""

# Display the map in Streamlit
st.components.v1.html(leaflet_code, height=600)

# Credits
st.write("🌦️ Weather data: [Open-Meteo](https://open-meteo.com)")
st.write("🗺️ Maps powered by [Leaflet.js](https://leafletjs.com)")
st.write("👨‍💻 Developer: [Database Systems](https://www.databasesystems.info)")
