Flight Market Demand Web Application - Project Description

In order to study the tendency of market demand on airline booking, I created a full-fledged Python web application based on Streamlit, Pandas, and Plotly. The application enables one to play with the dataset and see what it tells:

Leading air routes by demand in booking

Price and number of days left to go

Average pricing by city and travel fare

Also, the app is connected to two live APIs, which can retrieve and show live data about aviation:

Aviationstack API: displays the most frequent departure airports in the world.

OpenSky API: displays the live location of aircraft as they occur.

Important features are:

Data cleaning, and verification

Plotly Dynamic visualizations

Fallback messaging And API error handling

Streamlit user-friendly interface

The solution has showcased the end-to-end ability in handling data, integration with the API, and development of dashboard in a realistic environment all developed utilising free tools.

Setup Instructions (for Local Use in VS Code)

1. Install required libraries
pip install streamlit pandas plotly requests

2. Save the Python script 
flight_demand_app.py

3.Run the app with Streamlit
streamlit run flight_demand_app.py

4.Upload a CSV Dataset
Clean_Dataset.csv

5. API Keys & Notes
Aviationstack API Key is already included.
OpenSky API is free and does not require an API key.
 If any API is down or unreachable, the app will still work and show a warning.


