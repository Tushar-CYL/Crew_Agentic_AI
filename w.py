import streamlit as st
from crewai import LLM  # Assuming you have the LLM class from your environment
import folium
from folium import plugins
from streamlit_folium import st_folium
from dotenv import load_dotenv

load_dotenv()

# Initialize the Gemini LLM model
llm = LLM(model="gemini/gemini-1.5-pro-latest", temperature=0.7)

# Function to generate weather data using LLM
def get_weather_data_using_llm(location):
    prompt = f"Provide the current weather forecast and disaster warnings for {location}."
    
    # Use the correct method (e.g., 'ask') instead of 'predict'
    weather_data = llm.ask(prompt)  # Replace 'ask' with the correct method name
    return weather_data

# Function to generate resource management data using LLM
def get_resource_data_using_llm():
    prompt = "Suggest optimal resource allocation for disaster management, including shelters, rescue teams, and ambulances."
    resource_data = llm.ask(prompt)  # Use the correct method to get resource allocation
    return resource_data

# Function to create an interactive map
def create_map(lat, lon, disaster_area_data, resource_data):
    disaster_map = folium.Map(location=[lat, lon], zoom_start=12)
    
    # Add disaster area markers
    for area in disaster_area_data:
        folium.Marker([area["latitude"], area["longitude"]], 
                      popup=area["name"], 
                      icon=folium.Icon(color='red')).add_to(disaster_map)
    
    # Add resource markers (shelters, rescue teams, etc.)
    for resource in resource_data:
        folium.Marker([resource["latitude"], resource["longitude"]], 
                      popup=f"Resource: {resource['type']}", 
                      icon=folium.Icon(color='green')).add_to(disaster_map)
    
    # Add cluster plugin for better UI when there are many markers
    marker_cluster = plugins.MarkerCluster().add_to(disaster_map)
    for area in disaster_area_data + resource_data:
        folium.Marker([area["latitude"], area["longitude"]], 
                      popup=area.get("name", area.get("type", "Unknown"))).add_to(marker_cluster)

    return disaster_map

# Main function for the Streamlit app
def main():
    # Title and introduction
    st.title("Disaster Management and Evacuation Planner")
    st.write("This application helps to visualize and manage resources during disasters. It integrates weather data, real-time resource management, and dynamic evacuation planning.")

    # Section for selecting a location and viewing weather data
    st.header("Weather and Disaster Data")
    location = st.text_input("Enter a Location (city name or coordinates):", "Bhopal")
    
    # Fetch and display weather data using LLM
    if location:
        weather_data = get_weather_data_using_llm(location)
        if weather_data:
            st.write(f"Weather Forecast and Disaster Warnings for {location}:")
            st.write(weather_data)
    
    # Section for displaying resource data using LLM
    st.header("Resource Management")
    resource_data = get_resource_data_using_llm()
    if resource_data:
        st.write("Suggested Resources for Disaster Management (Shelters, Rescue Teams, etc.):")
        st.write(resource_data)
    
    # Section for creating an interactive map
    st.header("Interactive Map")
    disaster_area_data = [
        {"name": "Flood Zone", "latitude": 23.2599, "longitude": 77.4126},  # Example disaster area
        {"name": "Fire Zone", "latitude": 23.2699, "longitude": 77.4426}
    ]  # Example data, you can replace with dynamic data based on the disaster type
    
    # Example resource data
    resource_data = [
        {"type": "Ambulance", "latitude": 23.2600, "longitude": 77.4200},
        {"type": "Shelter", "latitude": 23.2700, "longitude": 77.4500}
    ]
    
    # Create and display the map with disaster and resource markers
    disaster_map = create_map(23.2599, 77.4126, disaster_area_data, resource_data)
    st_folium(disaster_map, width=800, height=600)
    
    # Section for resource optimization and dynamic decision-making
    st.header("Resource Optimization and Evacuation Planning")
    st.write("This section will dynamically allocate resources to disaster areas based on the current scenario.")
    
    # Example decision-making process (simulated)
    st.write("Based on the current disaster scenario, the system recommends dispatching:")
    recommended_resources = ["2 Rescue Teams", "3 Emergency Shelters", "5 Ambulances"]
    st.write(f"Recommendation: {', '.join(recommended_resources)}")
    
    # Simulate resource allocation
    if st.button("Allocate Resources"):
        st.write("Resources allocated successfully!")
        st.write("Rescue Teams are en route to the affected areas.")
    
    # Footer and additional information
    st.sidebar.header("More Information")
    st.sidebar.write("This system is designed to assist with disaster response by providing real-time data visualization, resource management, and evacuation planning.")

if __name__ == "__main__":
    main()
