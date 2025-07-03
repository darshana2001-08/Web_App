# flight_demand_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import requests

res = requests.get("https://opensky-network.org/api/states/all")
print(res.status_code)  # Should be 200


st.set_page_config(layout="wide")
st.title("🌐 Flight Market Demand Dashboard")

# --- Upload Section ---
st.sidebar.header("Upload Flight Dataset")
file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

if file:
    df = pd.read_csv(file)

    # --- Data Cleaning ---
    df['class'].fillna(df['class'].mode()[0], inplace=True)
    df['duration'].fillna(df['duration'].mode()[0], inplace=True)
    df['days_left'].fillna(df['days_left'].median(), inplace=True)
    df = df[df['price'].notnull()]

    city_to_iata = {
        "DELHI": "DEL",
        "MUMBAI": "BOM",
        "BANGALORE": "BLR",
        "KOLKATA": "CCU",
        "CHENNAI": "MAA",
        "HYDERABAD": "HYD"
    }

    df['source_city'] = df['source_city'].str.upper()
    df['destination_city'] = df['destination_city'].str.upper()
    df['source_iata'] = df['source_city'].map(city_to_iata)
    df['destination_iata'] = df['destination_city'].map(city_to_iata)

    # --- Visualizations ---
    st.subheader("📈 Top Routes by Demand")
    route_counts = df.groupby(['source_city', 'destination_city']).size().reset_index(name='count')
    route_counts = route_counts.sort_values('count', ascending=False)
    fig1 = px.bar(route_counts.head(10), x='source_city', y='count', color='destination_city')
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("📉 Price vs Days Left")
    fig2 = px.scatter(df, x='days_left', y='price', color='class')
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("💰 Average Price by Class and City")
    avg_prices = df.groupby(['source_city', 'class'])['price'].mean().reset_index()
    fig3 = px.bar(avg_prices, x='source_city', y='price', color='class')
    st.plotly_chart(fig3, use_container_width=True)

# --- Aviationstack API ---
st.subheader("✈️ Live Airline Data (Aviationstack API)")
av_key = "4d82c5d897439d93cce8ae57c5a4e0d3"
av_url = f"http://api.aviationstack.com/v1/flights?access_key={av_key}&limit=100"

try:
    av_response = requests.get(av_url)
    av_data = av_response.json()
    df_api = pd.json_normalize(av_data['data'])
    top_departures = df_api['departure.iata'].value_counts().reset_index()
    top_departures.columns = ['Departure Airport', 'Flights']
    fig_api = px.bar(top_departures.head(10), x='Departure Airport', y='Flights')
    st.plotly_chart(fig_api, use_container_width=True)
except:
    st.warning("Aviationstack API failed to load.")

# --- OpenSky API ---
st.subheader("🌍 Live Aircraft Positions (OpenSky API)")
opensky_url = "https://opensky-network.org/api/states/all"

try:
    os_response = requests.get(opensky_url)
    os_data = os_response.json()
    columns = [
        "icao24", "callsign", "origin_country", "time_position", "last_contact",
        "longitude", "latitude", "baro_altitude", "on_ground", "velocity",
        "true_track", "vertical_rate", "sensors", "geo_altitude", "squawk",
        "spi", "position_source"
    ]
    df_os = pd.DataFrame(os_data['states'], columns=columns)
    df_os = df_os.dropna(subset=['latitude', 'longitude'])
    df_os = df_os[df_os['latitude'].between(-90, 90) & df_os['longitude'].between(-180, 180)]
    fig_map = px.scatter_geo(
        df_os.head(200),
        lat='latitude',
        lon='longitude',
        hover_name='callsign',
        color='origin_country',
        title='Live Aircraft Map',
        projection="natural earth"
    )
    st.plotly_chart(fig_map, use_container_width=True)
except:
    st.warning("OpenSky API failed to load.")
