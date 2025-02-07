import streamlit as st

st.title("Map with Weather Popup")

# Open-Meteo API endpoint
API_ENDPOINT = "https://api.open-meteo.com/v1/forecast"

leaflet_code = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Leaflet Map</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        #map {{ height: 500px; width: 700px; }}
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        var map = L.map('map').setView([51.5074, 0.1278], 10);
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }}).addTo(map);

        var markerGroup = L.layerGroup().addTo(map);

        map.on('click', function(e) {{
            var lat = e.latlng.lat;
            var lon = e.latlng.lng;

            markerGroup.clearLayers();

            fetch('{API_ENDPOINT}?latitude=' + lat + '&longitude=' + lon + '&current_weather=true&forecast_days=1')
                .then(response => response.json())
                .then(data => {{
                    if (data && data.current_weather) {{
                        var temp = data.current_weather.temperature;
                        var windspeed = data.current_weather.windspeed;

                        // Construct popup content using concatenation
                        var popupContent = "Lat: " +lat+ "<br>Lon: "+lon+"<br>Temperature: " + temp + " °C<br>Wind Speed: " + windspeed + " m/s";

                        L.marker([lat, lon]).addTo(markerGroup).bindPopup(popupContent).openPopup();
                    }} else {{
                        alert("Could not retrieve weather data.");
                        console.error("API Response:", data);
                    }}
                }})
                .catch(error => {{
                    console.error("Error fetching data:", error);
                    alert("An error occurred while fetching data.");
                }});
        }});
    </script>
</body>
</html>
"""

st.components.v1.html(leaflet_code, width=700, height=500)