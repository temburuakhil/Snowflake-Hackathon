import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Artisan Support",
    page_icon="🎨",
    layout="wide"
)

st.title("Artisan Support & Craft Integration 🎨")

# Sample data - In production, this would come from actual databases
crafts_data = {
    'Craft': ['Pashmina', 'Blue Pottery', 'Madhubani', 'Kalamkari', 'Bidri'],
    'Region': ['Kashmir', 'Rajasthan', 'Bihar', 'Andhra Pradesh', 'Karnataka'],
    'Artisans': [500, 300, 400, 350, 250],
    'GeM_Listings': [45, 30, 25, 20, 15],
    'Revenue': [5000000, 3000000, 4000000, 3500000, 2500000]
}

schemes = [
    {
        "name": "Hunar Se Rozgar Tak",
        "description": "Skill development program for artisans",
        "eligibility": "Traditional artisans",
        "benefits": "Training, marketing support, and market linkage",
        "status": "Active"
    },
    {
        "name": "Craft Revival Program",
        "description": "Preservation and promotion of traditional crafts",
        "eligibility": "Craft clusters and cooperatives",
        "benefits": "Financial assistance and technical support",
        "status": "Active"
    },
    {
        "name": "GeM Integration Support",
        "description": "Help artisans list products on Government e-Marketplace",
        "eligibility": "Registered artisans and cooperatives",
        "benefits": "Technical support and marketing assistance",
        "status": "Active"
    }
]

# Create tabs
tab1, tab2, tab3 = st.tabs(["Craft Analytics", "GeM Integration", "Government Schemes"])

with tab1:
    st.subheader("Craft Analytics")
    
    # Craft distribution
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(crafts_data, values='Artisans', names='Craft',
                    title='Distribution of Artisans by Craft')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(crafts_data, x='Craft', y='Revenue',
                    title='Revenue by Craft Type')
        st.plotly_chart(fig, use_container_width=True)
    
    # Key metrics
    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Artisans", "1,800", "+150")
    with col2:
        st.metric("Total Revenue", "₹18M", "+2M")
    with col3:
        st.metric("GeM Listings", "135", "+25")

with tab2:
    st.subheader("GeM Integration Status")
    
    # GeM listings
    fig = px.scatter(crafts_data, x='Artisans', y='GeM_Listings',
                    size='Revenue', color='Craft',
                    title='Artisans vs GeM Listings by Craft')
    st.plotly_chart(fig, use_container_width=True)
    
    # GeM integration guide
    st.subheader("How to List on GeM")
    steps = [
        "1. Register as a seller on GeM portal",
        "2. Complete seller profile and documentation",
        "3. List your products with detailed descriptions",
        "4. Set competitive pricing",
        "5. Respond to government tenders"
    ]
    for step in steps:
        st.write(step)
    
    if st.button("Start GeM Registration"):
        st.write("Redirecting to GeM portal...")

with tab3:
    st.subheader("Available Government Schemes")
    
    # Display schemes
    for scheme in schemes:
        with st.expander(f"{scheme['name']} - {scheme['status']}"):
            st.write(f"**Description:** {scheme['description']}")
            st.write(f"**Eligibility:** {scheme['eligibility']}")
            st.write(f"**Benefits:** {scheme['benefits']}")
            if st.button("Apply Now", key=f"apply_{scheme['name']}"):
                st.write("Application form would be shown here")
    
    # Scheme statistics
    st.subheader("Scheme Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Active Schemes", "3", "+1")
        st.metric("Total Beneficiaries", "2,500", "+300")
    with col2:
        st.metric("Funds Disbursed", "₹25M", "+5M")
        st.metric("Success Rate", "85%", "+5%")

# Add a search functionality
st.sidebar.subheader("Search Artisans")
search_query = st.sidebar.text_input("Search by craft or region")
if search_query:
    filtered_crafts = [craft for craft in crafts_data['Craft'] 
                      if search_query.lower() in craft.lower()]
    filtered_regions = [region for region in crafts_data['Region'] 
                       if search_query.lower() in region.lower()]
    
    if filtered_crafts or filtered_regions:
        st.sidebar.write("Found matches:")
        for craft in filtered_crafts:
            st.sidebar.write(f"🎨 {craft}")
        for region in filtered_regions:
            st.sidebar.write(f"📍 {region}")
    else:
        st.sidebar.write("No matches found") 