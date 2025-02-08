import streamlit as st

st.title("Weather map")
st.subheader("Click on the map to see weather details")
with st.sidebar:  # Use 'with' to define sidebar content block
    st.header("Weather map")  # Add a header to the sidebar
    st.write("more controls here...")



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

        // Define different tile layers
        var osmLayer = L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }});

        var satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}', {{
            attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, GetImagery, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
        }});

        // Add the default layer to the map
        osmLayer.addTo(map);  // OpenStreetMap is the default

        // Create a layer control
        var baseLayers = {{
            "OpenStreetMap": osmLayer,
            "Satellite": satelliteLayer
            }};
        L.control.layers(baseLayers).addTo(map);

        var markerGroup = L.layerGroup().addTo(map);

        map.on('click', function(e) {{
            var lat = e.latlng.lat;
            var lon = e.latlng.lng;

            markerGroup.clearLayers();

            // 1. Reverse Geocoding (Get Place Name)
            fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${{lat}}&lon=${{lon}}`) 
                .then(response => response.json())
                .then(geocodingData => {{
                    var placeName = "Location Not Found";
                    if (geocodingData && geocodingData.address) {{
                        placeName = geocodingData.address.city || geocodingData.address.town || geocodingData.address.village;
                        if (!placeName) {{
                            placeName = geocodingData.address.county || geocodingData.address.region;
                        }}
                        if (!placeName) {{
                            placeName = geocodingData.address.country;
                        }}
                        if (!placeName) {{
                            placeName = "Location";
                        }}
                    }}

                    // 2. Fetch Weather Data
                    fetch('{API_ENDPOINT}?latitude=' + lat + '&longitude=' + lon + '&current_weather=true&forecast_days=1')
                        .then(response => response.json())
                        .then(data => {{
                            if (data && data.current_weather) {{
                                var temp = data.current_weather.temperature;
                                var windspeed = data.current_weather.windspeed;

                        var popupContent =   "<table><tr><td>Temp</td><td> <span style='font-size: 2em;'>" + temp + "°C </span></td></tr> <tr><td>Winds</td><td> " + windspeed+ " m/s</td></tr> <tr><td>Place</td><td><b>" + placeName + "</b></td></tr></table>";


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
        }});
    </script>
</body>
</html>
"""

st.components.v1.html(leaflet_code, width=700, height=500)
st.write("Weather data is provided by open-meteo.com API")
st.write("Maps are Leaflet maps")
st.write("done by - www.databasesystems.info")