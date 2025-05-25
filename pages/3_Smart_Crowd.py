import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Basic page configuration
st.set_page_config(
    page_title="Smart Crowd Management",
    page_icon="👥",
    layout="wide"
)

# Simple title to test if the page loads
st.title("Smart Crowd Management")

# Add a simple element to verify the page is working
st.write("Loading crowd management features...")

# If the page loads successfully, we'll add the rest of the functionality
try:
    # Sidebar filters
    st.sidebar.header("Filters")
    selected_location = st.sidebar.selectbox(
        "Select Location",
        ["Taj Mahal", "Red Fort", "Qutub Minar", "Gateway of India"]
    )

    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(datetime.now() - timedelta(days=7), datetime.now())
    )

    # Main content
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Real-time Crowd Status")
        
        # Simulate real-time crowd data
        current_crowd = np.random.randint(100, 1000)
        capacity = 1000
        crowd_percentage = (current_crowd / capacity) * 100
        
        # Create gauge chart for crowd level
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=crowd_percentage,
            title={'text': "Current Crowd Level"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 30], 'color': "lightgreen"},
                    {'range': [30, 70], 'color': "yellow"},
                    {'range': [70, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        ))
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Crowd alerts
        st.subheader("Crowd Alerts")
        if crowd_percentage > 80:
            st.error("⚠️ High crowd alert! Consider implementing crowd control measures.")
        elif crowd_percentage > 50:
            st.warning("⚠️ Moderate crowd level. Monitor the situation.")
        else:
            st.success("✅ Crowd level is manageable.")

    with col2:
        st.subheader("Smart Routing Suggestions")
        
        # Generate sample routing data
        routes = pd.DataFrame({
            'Route': ['Main Entrance', 'Alternative Entry', 'VIP Gate', 'Group Entry'],
            'Current Wait Time (min)': [15, 5, 2, 10],
            'Distance (m)': [100, 150, 200, 120],
            'Crowd Level': ['High', 'Low', 'Medium', 'Medium']
        })
        
        # Display routing table
        st.dataframe(routes, use_container_width=True)
        
        # Best route recommendation
        best_route = routes.loc[routes['Current Wait Time (min)'].idxmin()]
        st.info(f"💡 Recommended Route: {best_route['Route']} (Wait time: {best_route['Current Wait Time (min)']} minutes)")

    # Historical crowd trends
    st.subheader("Historical Crowd Trends")
    dates = pd.date_range(start=date_range[0], end=date_range[1], freq='H')
    crowd_data = pd.DataFrame({
        'Timestamp': dates,
        'Crowd Level': np.random.randint(100, 1000, size=len(dates))
    })

    fig = px.line(crowd_data, x='Timestamp', y='Crowd Level',
                  title='Crowd Level Over Time')
    st.plotly_chart(fig, use_container_width=True)

    # Crowd management tips
    st.subheader("Crowd Management Tips")
    tips = [
        "Plan your visit during off-peak hours (early morning or late afternoon)",
        "Use the alternative entry points when main entrance is crowded",
        "Consider booking tickets online to avoid long queues",
        "Follow the recommended routes for the best experience",
        "Stay updated with real-time crowd alerts"
    ]

    for tip in tips:
        st.markdown(f"- {tip}")

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center'>
            <p>Smart Crowd Management System | Real-time Monitoring</p>
        </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.write("Please check if all required packages are installed.") 