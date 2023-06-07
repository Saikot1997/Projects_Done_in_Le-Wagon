import streamlit as st
import requests
from datetime import datetime
from geopy.geocoders import GoogleV3
import streamlit_folium as stf
from streamlit_folium import folium_static
import folium


def main():
    st.title("Taxi Fare")
    geolocator = GoogleV3(api_key='AIzaSyBzRO8KVtdOU3jtc-W0yVW_vNym1kD1gnM')

    # Set initial map location to New York City
    initial_latitude = 40.7128
    initial_longitude = -74.0060
    initial_zoom = 12
    map_figure = folium.Map(location=[initial_latitude, initial_longitude], zoom_start=initial_zoom)

    st.write("Please provide the following details:")

    with st.form("Parameter Input"):
        pickup_date = st.date_input("Date", value=datetime.now().date())
        pickup_time = st.time_input("Time", value=datetime.now().time())
        pickup_location = st.text_input("Pickup Location", key="pickup")
        dropoff_location = st.text_input("Dropoff Location", key="dropoff")
        passenger_count = st.number_input("Passenger Count", min_value=1, max_value=8, value=1, step=1)

        submitted = st.form_submit_button("Get Fare")

        if submitted:
            pickup_coordinates = geolocator.geocode(pickup_location)
            if pickup_coordinates is None:
                st.error("Failed to retrieve pickup coordinates. Please enter a valid pickup location.")
                return
            pickup_latitude, pickup_longitude = pickup_coordinates.latitude, pickup_coordinates.longitude

            dropoff_coordinates = geolocator.geocode(dropoff_location)
            if dropoff_coordinates is None:
                st.error("Failed to retrieve dropoff coordinates. Please enter a valid dropoff location.")
                return
            dropoff_latitude, dropoff_longitude = dropoff_coordinates.latitude, dropoff_coordinates.longitude

            pickup_datetime = datetime.combine(pickup_date, pickup_time)

            url = 'https://taxifare.lewagon.ai/predict'
            api_params = {
                "pickup_datetime": pickup_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "pickup_longitude": pickup_longitude,
                "pickup_latitude": pickup_latitude,
                "dropoff_longitude": dropoff_longitude,
                "dropoff_latitude": dropoff_latitude,
                "passenger_count": passenger_count
            }

            response = requests.get(url, params=api_params)
            fare_prediction = response.json()["fare"]

            st.success(f"Predicted Fare: ${fare_prediction:.2f}")
            map_data = {
                "Pickup": [pickup_latitude, pickup_longitude],
                "Dropoff": [dropoff_latitude, dropoff_longitude]
            }

            for label, coord in map_data.items():
                folium.Marker(location=coord, popup=label).add_to(map_figure)

            route = folium.PolyLine(
                locations=[[pickup_latitude, pickup_longitude], [dropoff_latitude, dropoff_longitude]],
                color='blue',
                weight=5,
                opacity=0.7
            )
            route.add_to(map_figure)

    st.write(f"Pickup: {pickup_location}")
    st.write(f"Dropoff: {dropoff_location}")
    folium_static(map_figure)


if __name__ == "__main__":
    main()
