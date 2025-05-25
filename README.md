# IndiaTrek Vista Explorer

An interactive web application for exploring various locations across India, built with Streamlit.

## Features

- Interactive map showing various locations
- Search functionality
- Category filtering
- Detailed location information
- Responsive design

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

To run the application, use the following command:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## Data Structure

The application uses a simple JSON structure for location data. Each location should have:
- name: Name of the location
- category: Category of the location
- coordinates: [latitude, longitude]
- description: Brief description of the location

You can modify the `LOCATIONS` list in `app.py` to add your own locations. 