import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Cultural Dashboard",
    page_icon="🏛️",
    layout="wide"
)

st.title("Unified Cultural Dashboard 🏛️")

# Sample data - In production, this would come from actual APIs/databases
tourism_data = {
    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    'Tourists': [5000, 6000, 7000, 8000, 9000, 10000],
    'Revenue': [500000, 600000, 700000, 800000, 900000, 1000000]
}

heritage_sites = {
    'Site': ['Taj Mahal', 'Red Fort', 'Khajuraho', 'Hampi', 'Konark'],
    'Visitors': [10000, 8000, 6000, 5000, 4000],
    'Conservation_Status': ['Good', 'Fair', 'Good', 'Poor', 'Fair']
}

# Create tabs for different sections
tab1, tab2, tab3 = st.tabs(["Tourism Analytics", "Heritage Status", "Government Schemes"])

with tab1:
    st.subheader("Tourism Analytics")
    
    # Tourism trends
    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(tourism_data, x='Month', y='Tourists', 
                     title='Monthly Tourist Inflow')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(tourism_data, x='Month', y='Revenue',
                    title='Monthly Tourism Revenue')
        st.plotly_chart(fig, use_container_width=True)
    
    # Key metrics
    st.subheader("Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Tourists", "45,000", "+15%")
    with col2:
        st.metric("Revenue", "₹4.5M", "+20%")
    with col3:
        st.metric("Average Stay", "4.5 days", "+0.5")
    with col4:
        st.metric("Satisfaction", "4.2/5", "+0.3")

with tab2:
    st.subheader("Heritage Site Status")
    
    # Heritage site status
    fig = px.bar(heritage_sites, x='Site', y='Visitors',
                 color='Conservation_Status',
                 title='Heritage Site Visitors and Conservation Status')
    st.plotly_chart(fig, use_container_width=True)
    
    # Conservation metrics
    st.subheader("Conservation Metrics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Sites Monitored", "150", "+5")
        st.metric("Conservation Projects", "25", "+3")
    with col2:
        st.metric("Funds Allocated", "₹50M", "+10M")
        st.metric("Projects Completed", "15", "+2")

with tab3:
    st.subheader("Government Schemes and Initiatives")
    
    # Active schemes
    schemes = [
        {
            "name": "Swadesh Darshan",
            "budget": "₹100M",
            "status": "Active",
            "beneficiaries": "500+ sites"
        },
        {
            "name": "PRASAD",
            "budget": "₹50M",
            "status": "Active",
            "beneficiaries": "12 cities"
        },
        {
            "name": "Heritage City Development",
            "budget": "₹75M",
            "status": "Planning",
            "beneficiaries": "8 cities"
        }
    ]
    
    for scheme in schemes:
        with st.expander(f"{scheme['name']} - {scheme['status']}"):
            st.write(f"Budget: {scheme['budget']}")
            st.write(f"Beneficiaries: {scheme['beneficiaries']}")
            st.progress(0.7 if scheme['status'] == 'Active' else 0.3) 