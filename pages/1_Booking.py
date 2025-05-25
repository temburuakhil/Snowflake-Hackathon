import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(
    page_title="IndiaTrek Booking",
    page_icon="🎫",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .booking-form {
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        background-color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Book Your IndiaTrek Adventure 🎫")

# Create a form for booking
with st.form("booking_form"):
    st.subheader("Personal Information")
    col1, col2 = st.columns(2)
    
    with col1:
        first_name = st.text_input("First Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
    
    with col2:
        last_name = st.text_input("Last Name")
        nationality = st.text_input("Nationality")
        age = st.number_input("Age", min_value=18, max_value=100)
    
    st.subheader("Trip Details")
    col3, col4 = st.columns(2)
    
    with col3:
        destination = st.selectbox(
            "Select Destination",
            ["Taj Mahal, Agra", "Jaipur Palace", "Kerala Backwaters", "Goa Beaches", "Varanasi Ghats"]
        )
        start_date = st.date_input(
            "Start Date",
            min_value=datetime.now(),
            max_value=datetime.now() + timedelta(days=365)
        )
    
    with col4:
        trip_type = st.selectbox(
            "Trip Type",
            ["Solo", "Couple", "Family", "Group"]
        )
        duration = st.selectbox(
            "Duration",
            ["3 Days", "5 Days", "7 Days", "10 Days", "14 Days"]
        )
    
    st.subheader("Additional Preferences")
    accommodation = st.selectbox(
        "Preferred Accommodation",
        ["Budget", "Standard", "Luxury"]
    )
    
    special_requirements = st.text_area("Special Requirements or Notes")
    
    # Submit button
    submitted = st.form_submit_button("Book Now")
    
    if submitted:
        if first_name and last_name and email and phone and destination:
            st.success("Booking submitted successfully! We'll contact you shortly with the details.")
            # Here you would typically save the booking to a database
        else:
            st.error("Please fill in all required fields.") 