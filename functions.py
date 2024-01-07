import requests
import os
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
from geopy.distance import geodesic
import evaluate
import financial

# Global cache for storing solar data calculations
solar_data_cache = {}

load_dotenv()  # This loads the variables from .env

GOOGLE_CLOUD_API_KEY = os.environ['GOOGLE_CLOUD_API_KEY']
AIRTABLE_API_KEY = os.environ['AIRTABLE_API_KEY']

# Add lead to Airtable
def create_lead(name, phone, address):
  url = "https://api.airtable.com/v0/appMsEE4H40MM10gI/Leads"  # Change this to your Airtable API URL
  headers = {
      "Authorization": f"Bearer {AIRTABLE_API_KEY}",
      "Content-Type": "application/json"
  }
  data = {
      "records": [{
          "fields": {
              "Name": name,
              "Phone": phone,
              "Address": address
          }
      }]
  }
  response = requests.post(url, headers=headers, json=data)
  if response.status_code == 200:
    print("Lead created successfully.")
    return response.json()
  else:
    print(f"Failed to create lead: {response.text}")


# Get coordidinates from address via Geocoding API
def get_coordinates(address):
  geocoding_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GOOGLE_CLOUD_API_KEY}"
  response = requests.get(geocoding_url)
  if response.status_code == 200:
    location = response.json().get('results')[0].get('geometry').get(
        'location')
    print(f"Coordinates for {address}: {location}")
    return location['lat'], location['lng']
  else:
    print(f"Error getting coordinates: {response.text}")


def get_solar_data(lat, lng):
    cache_key = f"{lat},{lng}"
    if cache_key in solar_data_cache:
        print(f"Using cached data for coordinates: {lat}, {lng}")
        return solar_data_cache[cache_key]

    building_id = evaluate.get_building_id(lat, lng)
    print(f"Retrieved Building ID: {building_id}")
    if building_id:
        solar_data = evaluate.get_solar_potential_for_building(building_id)
        print(f"API Response Solar Data: {solar_data}")
        solar_data_cache[cache_key] = solar_data
        return solar_data
    else:
        print("Error: Could not retrieve building ID")
        return None



def solar_panel_calculations(address):
    print(f"Calculating solar panel potential for {address}.")
    lat, lng = get_coordinates(address)
    if not lat or not lng:
        return {"error": "Could not get coordinates for the address provided."}

    cache_key = f"{lat},{lng}"
    if cache_key in solar_data_cache:
        print(f"Using cached data for address: {address}")
        return solar_data_cache[cache_key]

    return get_solar_data(lat, lng)



def process_solar_data(address):
    lat, lng = get_coordinates(address)
    cache_key = f"{lat},{lng}"

    if cache_key in solar_data_cache:
        print(f"Using cached data for coordinates: {lat}, {lng}")
        solar_data = solar_data_cache[cache_key]
    else:
        solar_data = get_solar_data(lat, lng)
        if solar_data is not None:
            solar_data_cache[cache_key] = solar_data

    if solar_data is None or solar_data.get("error"):
        return {"error": "Could not retrieve solar data"} 

    # Extract 'best_surface_data' for the solar system report
    best_surface_data = solar_data.get('best_surface_data', {})
    print(f"Processed Solar Data: {best_surface_data}")

    return financial.generate_solar_system_report(
        best_surface_data.get('area', 0),
        best_surface_data.get('orientation', ''),
        best_surface_data.get('slope', 0),
        best_surface_data.get('mean_radiation', 0),
        best_surface_data.get('electric_yield', 0),
        best_surface_data.get('monthly_yield', [])
    )

# Load the installers data
installers_df = pd.read_csv('solar_installers.csv')

def find_best_solar_installers(address):
    lat, lng = get_coordinates(address)
    if not lat or not lng:
        return {"error": "Could not get coordinates for the address provided."}

    # Add a column to the DataFrame for the distance from the user's address
    installers_df['distance'] = installers_df.apply(lambda row: geodesic((lat, lng), (row['Latitude'], row['Longitude'])).kilometers, axis=1)

    # Sort by distance, rating, and number of reviews (assuming 'Review Summary' contains the number of reviews)
    installers_df['review_count'] = installers_df['Review Summary'].str.extract(r'(\d+)').astype(float)
    sorted_installers = installers_df.sort_values(by=['distance', 'Average Rating', 'review_count'], ascending=[True, False, False])

    # Select the top three installers
    top_three_installers = sorted_installers.head(3)

    return top_three_installers[['Company Name', 'Address', 'Phone Number', 'Average Rating', 'Business Website']].to_dict(orient='records')


