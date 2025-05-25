import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
from PIL import Image
import json
import webbrowser
from data import LOCATIONS, STATE_POLLUTION, get_pollution_color
import requests
import os
from folium.plugins import Draw
from folium import plugins
import math

# Set page configuration
st.set_page_config(
    page_title="IndiaTrek Vista Explorer",
    page_icon="🗺️",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .category-button {
        margin: 5px;
        padding: 8px 16px;
        border-radius: 20px;
        border: 1px solid #ddd;
        background-color: white;
        cursor: pointer;
    }
    .category-button.active {
        background-color: #4CAF50;
        color: white;
    }
    .location-card {
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Fetch India state boundaries
@st.cache_data
def get_india_states():
    # Load local GeoJSON for India's boundaries
    with open(os.path.join(os.path.dirname(__file__), 'k.json'), 'r', encoding='utf-8') as f:
        return json.load(f)

# Initialize session state
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None
if 'selected_location' not in st.session_state:
    st.session_state.selected_location = None

# Header
st.title("IndiaTrek Vista Explorer")

# Sidebar
with st.sidebar:
    st.header("Search & Filter")
    search_query = st.text_input("Search locations...", "")
    
    # Add state selection
    st.subheader("States")
    # Define all Indian states and union territories
    all_indian_states = [
        "All States",
        "Andaman and Nicobar Islands",
        "Andhra Pradesh",
        "Arunachal Pradesh",
        "Assam",
        "Bihar",
        "Chandigarh",
        "Chhattisgarh",
        "Dadra and Nagar Haveli and Daman and Diu",
        "Delhi",
        "Goa",
        "Gujarat",
        "Haryana",
        "Himachal Pradesh",
        "Jammu and Kashmir",
        "Jharkhand",
        "Karnataka",
        "Kerala",
        "Ladakh",
        "Lakshadweep",
        "Madhya Pradesh",
        "Maharashtra",
        "Manipur",
        "Meghalaya",
        "Mizoram",
        "Nagaland",
        "Odisha",
        "Puducherry",
        "Punjab",
        "Rajasthan",
        "Sikkim",
        "Tamil Nadu",
        "Telangana",
        "Tripura",
        "Uttar Pradesh",
        "Uttarakhand",
        "West Bengal"
    ]
    
    # Get states from locations
    location_states = sorted(list(set(loc["state"] for loc in LOCATIONS if "state" in loc)))
    
    # Combine both lists and remove duplicates while maintaining order
    all_states = ["All States"] + [state for state in all_indian_states[1:] if state in location_states]
    selected_state = st.selectbox("Select State", all_states)
    
    st.subheader("Categories")
    categories = sorted(list(set(loc["category"] for loc in LOCATIONS)))
    selected_category = st.radio("Select Category", ["All"] + categories)

    # Add pollution legend
    st.subheader("Air Quality Index (AQI)")
    st.markdown("""
    - 🟢 Good (0-50)
    - 🟡 Moderate (51-100)
    - 🟠 Unhealthy (101-200)
    - 🔴 Very Unhealthy (201-300)
    - 🟣 Hazardous (301-400)
    - ⚫ Very Hazardous (401+)
    """)

# Filter locations based on search, state, and category
filtered_locations = LOCATIONS
if search_query:
    filtered_locations = [loc for loc in filtered_locations 
                         if search_query.lower() in loc["name"].lower()]
if selected_state != "All States":
    filtered_locations = [loc for loc in filtered_locations 
                         if loc.get("state") == selected_state]
if selected_category != "All":
    filtered_locations = [loc for loc in filtered_locations 
                         if loc["category"] == selected_category]

# Create the map
m = folium.Map(
    location=[20.5937, 78.9629],
    zoom_start=5,
    tiles='CartoDB positron'
)

# Add drawing tools with custom position and styling
draw = Draw(
    draw_options={
        'polyline': False,
        'polygon': False,
        'circlemarker': False,
        'rectangle': False,
        'marker': False,
        'circle': True,  # Only enable circle drawing
    },
    edit_options={
        'edit': True,
        'remove': True
    },
    position='topleft'  # Position the drawing tools on the top-left
)
draw.add_to(m)

# Add custom CSS to make the drawing tools more visible and style the results
st.markdown("""
<style>
    .leaflet-draw-toolbar {
        margin-top: 12px !important;
        margin-left: 12px !important;
    }
    .leaflet-draw-toolbar a {
        background-color: white !important;
        border: 2px solid rgba(0,0,0,0.2) !important;
        border-radius: 4px !important;
        margin-bottom: 5px !important;
    }
    .leaflet-draw-toolbar a:hover {
        background-color: #f4f4f4 !important;
    }
    .area-results {
        position: fixed;
        top: 50%;
        right: 20px;
        transform: translateY(-50%);
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        max-width: 400px;
        max-height: 80vh;
        overflow-y: auto;
        z-index: 1000;
    }
    .category-section {
        margin-bottom: 15px;
        padding: 10px;
        border-radius: 5px;
        background: #f8f9fa;
    }
    .category-title {
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 5px;
    }
    .place-item {
        padding: 5px;
        margin: 5px 0;
        border-left: 3px solid #3498db;
        background: white;
        cursor: pointer;
    }
    .place-item:hover {
        background: #f0f0f0;
    }
    .place-details {
        margin-top: 10px;
        padding: 15px;
        background: #fff;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .place-details h4 {
        margin: 0 0 10px 0;
        color: #2c3e50;
        font-size: 18px;
    }
    .place-details p {
        margin: 5px 0;
        font-size: 14px;
        line-height: 1.5;
    }
    .place-details .wiki-content {
        margin-top: 15px;
        padding-top: 15px;
        border-top: 1px solid #eee;
    }
    .place-details .wiki-content h5 {
        color: #2c3e50;
        margin: 0 0 10px 0;
    }
    .place-details .wiki-content p {
        color: #666;
    }
    .close-details {
        float: right;
        cursor: pointer;
        color: #666;
        font-size: 18px;
        padding: 5px;
    }
    .close-details:hover {
        color: #333;
    }
    .loading {
        text-align: center;
        padding: 20px;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# Add state boundaries with pollution coloring
states_geojson = get_india_states()
for feature in states_geojson['features']:
    # Get state name from the correct property
    state_name = feature['properties'].get('NAME_1', feature['properties'].get('state_name', 'Unknown'))
    
    # Map state names to match our pollution data
    state_name_mapping = {
        'Delhi': 'Delhi',
        'Haryana': 'Haryana',
        'Punjab': 'Punjab',
        'Uttar Pradesh': 'Uttar Pradesh',
        'Rajasthan': 'Rajasthan',
        'Madhya Pradesh': 'Madhya Pradesh',
        'Gujarat': 'Gujarat',
        'Maharashtra': 'Maharashtra',
        'Karnataka': 'Karnataka',
        'Tamil Nadu': 'Tamil Nadu',
        'Kerala': 'Kerala',
        'Andhra Pradesh': 'Andhra Pradesh',
        'Telangana': 'Telangana',
        'Odisha': 'Odisha',
        'West Bengal': 'West Bengal',
        'Bihar': 'Bihar',
        'Jharkhand': 'Jharkhand',
        'Chhattisgarh': 'Chhattisgarh',
        'Assam': 'Assam',
        'Arunachal Pradesh': 'Arunachal Pradesh',
        'Nagaland': 'Nagaland',
        'Manipur': 'Manipur',
        'Mizoram': 'Mizoram',
        'Tripura': 'Tripura',
        'Meghalaya': 'Meghalaya',
        'Sikkim': 'Sikkim',
        'Goa': 'Goa',
        'Himachal Pradesh': 'Himachal Pradesh',
        'Uttarakhand': 'Uttarakhand',
        'Jammu and Kashmir': 'Jammu and Kashmir'
    }
    
    mapped_state_name = state_name_mapping.get(state_name, state_name)
    
    if mapped_state_name in STATE_POLLUTION:
        aqi = STATE_POLLUTION[mapped_state_name]
        color = get_pollution_color(aqi)
        
        folium.GeoJson(
            feature,
            style_function=lambda x, color=color: {
                'fillColor': color,
                'color': '#000000',
                'weight': 2,
                'fillOpacity': 0.7
            },
            tooltip=f"{mapped_state_name}<br>AQI: {aqi}",
            popup=f"<b>{mapped_state_name}</b><br>Air Quality Index: {aqi}"
        ).add_to(m)

# Add markers to the map with custom icons
for location in filtered_locations:
    # Create popup content with Wikipedia link
    popup_content = f"""
    <div style='width: 200px'>
        <h4>{location['name']}</h4>
        <p>{location['description']}</p>
        <a href='{location['wikipedia_url']}' target='_blank'>Read more on Wikipedia</a>
    </div>
    """
    
    folium.Marker(
        location["coordinates"],
        popup=folium.Popup(popup_content, max_width=300),
        tooltip=location["name"],
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

# Display the map
folium_static(m, width=1200, height=600)

# Add JavaScript to handle circle drawing and show places within the circle
st.markdown("""
<script>
    // Function to calculate distance between two points using Haversine formula
    function getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2) {
        var R = 6371; // Radius of the earth in km
        var dLat = deg2rad(lat2-lat1);
        var dLon = deg2rad(lon2-lon1);
        var a = 
            Math.sin(dLat/2) * Math.sin(dLat/2) +
            Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) * 
            Math.sin(dLon/2) * Math.sin(dLon/2); 
        var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
        var d = R * c; // Distance in km
        return d;
    }

    function deg2rad(deg) {
        return deg * (Math.PI/180);
    }

    // Function to create or update the results panel
    function updateResultsPanel(placesInCircle) {
        // Remove existing results panel if any
        var existingPanel = document.querySelector('.area-results');
        if (existingPanel) {
            existingPanel.remove();
        }

        // Group places by category
        var placesByCategory = {};
        placesInCircle.forEach(function(marker) {
            var popupContent = marker.getPopup().getContent();
            var category = popupContent.match(/Category: (.*?)<br>/)[1];
            if (!placesByCategory[category]) {
                placesByCategory[category] = [];
            }
            placesByCategory[category].push({
                name: marker.getTooltip().getContent(),
                popup: popupContent,
                latlng: marker.getLatLng()
            });
        });

        // Create new results panel
        var panel = document.createElement('div');
        panel.className = 'area-results';
        panel.innerHTML = '<h3>Places in Selected Area</h3>';

        // Add places grouped by category
        for (var category in placesByCategory) {
            var categorySection = document.createElement('div');
            categorySection.className = 'category-section';
            categorySection.innerHTML = '<div class="category-title">' + category + '</div>';
            
            placesByCategory[category].forEach(function(place) {
                var placeItem = document.createElement('div');
                placeItem.className = 'place-item';
                placeItem.textContent = place.name;
                placeItem.onclick = function() {
                    showPlaceDetails(place, panel);
                };
                categorySection.appendChild(placeItem);
            });

            panel.appendChild(categorySection);
        }

        document.body.appendChild(panel);
    }

    // Function to show place details
    function showPlaceDetails(place, panel) {
        // Remove existing details if any
        var existingDetails = panel.querySelector('.place-details');
        if (existingDetails) {
            existingDetails.remove();
        }

        // Create details section
        var details = document.createElement('div');
        details.className = 'place-details';
        
        // Extract information from popup content
        var popupContent = place.popup;
        var name = popupContent.match(/<h4>(.*?)<\/h4>/)[1];
        var description = popupContent.match(/<p>(.*?)<\/p>/)[1];
        var wikiUrl = popupContent.match(/href='(.*?)'/)[1];

        // Create details HTML with loading state
        details.innerHTML = `
            <span class="close-details" onclick="this.parentElement.remove()">×</span>
            <h4>${name}</h4>
            <p>${description}</p>
            <div class="wiki-content">
                <div class="loading">Loading Wikipedia content...</div>
            </div>
        `;

        // Add details to panel
        panel.insertBefore(details, panel.firstChild.nextSibling);
        
        // Scroll to details
        details.scrollIntoView({ behavior: 'smooth', block: 'start' });

        // Fetch Wikipedia content
        fetch(wikiUrl)
            .then(response => response.text())
            .then(html => {
                // Extract the main content
                var parser = new DOMParser();
                var doc = parser.parseFromString(html, 'text/html');
                var content = doc.querySelector('.mw-parser-output');
                
                if (content) {
                    // Get the first few paragraphs
                    var paragraphs = content.querySelectorAll('p');
                    var wikiText = '';
                    for (var i = 0; i < Math.min(3, paragraphs.length); i++) {
                        if (paragraphs[i].textContent.trim()) {
                            wikiText += '<p>' + paragraphs[i].textContent.trim() + '</p>';
                        }
                    }
                    
                    // Update the wiki content section
                    var wikiContent = details.querySelector('.wiki-content');
                    wikiContent.innerHTML = `
                        <h5>From Wikipedia</h5>
                        ${wikiText}
                        <p><a href="${wikiUrl}" target="_blank">Read full article on Wikipedia</a></p>
                    `;
                }
            })
            .catch(error => {
                var wikiContent = details.querySelector('.wiki-content');
                wikiContent.innerHTML = `
                    <h5>From Wikipedia</h5>
                    <p>Unable to load Wikipedia content. <a href="${wikiUrl}" target="_blank">Read on Wikipedia</a></p>
                `;
            });
    }

    // Listen for circle drawing events
    map.on('draw:created', function(e) {
        var type = e.layerType;
        var layer = e.layer;
        
        if (type === 'circle') {
            var center = layer.getLatLng();
            var radius = layer.getRadius() / 1000; // Convert to km
            
            // Get all markers
            var markers = [];
            map.eachLayer(function(layer) {
                if (layer instanceof L.Marker) {
                    markers.push(layer);
                }
            });
            
            // Find markers within the circle
            var placesInCircle = markers.filter(function(marker) {
                var distance = getDistanceFromLatLonInKm(
                    center.lat, center.lng,
                    marker.getLatLng().lat, marker.getLatLng().lng
                );
                return distance <= radius;
            });
            
            // Update the results panel
            if (placesInCircle.length > 0) {
                updateResultsPanel(placesInCircle);
            }
        }
    });

    // Remove results panel when circle is removed
    map.on('draw:deleted', function() {
        var panel = document.querySelector('.area-results');
        if (panel) {
            panel.remove();
        }
    });
</script>
""", unsafe_allow_html=True)

# Display location details
if filtered_locations:
    st.subheader("Location Details")
    cols = st.columns(2)
    for idx, location in enumerate(filtered_locations):
        with cols[idx % 2]:
            with st.expander(location["name"], expanded=True):
                st.markdown(f"**Category:** {location['category']}")
                st.markdown(f"**Description:** {location['description']}")
                st.markdown(f"**Coordinates:** {location['coordinates']}")
                if st.button(f"Open Wikipedia - {location['name']}", key=f"wiki_{idx}"):
                    webbrowser.open(location['wikipedia_url']) 