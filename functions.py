import requests
import os
from dotenv import load_dotenv
import pandas as pd
import financial
import json

# Global cache for storing solar data calculations
solar_data_cache = {}

load_dotenv()  # This loads the variables from .env

GOOGLE_CLOUD_API_KEY = os.environ['GOOGLE_CLOUD_API_KEY']

def get_coordinates(address):
    geocoding_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GOOGLE_CLOUD_API_KEY}"
    response = requests.get(geocoding_url)
    if response.status_code == 200:
        location = response.json().get('results')[0].get('geometry').get('location')
        print(f"Coordinates for {address}: {location}")
        return location['lat'], location['lng']
    else:
        print(f"Error getting coordinates: {response.text}")

def get_solar_data(lat, lng):
    cache_key = f"{lat},{lng}"
    if cache_key in solar_data_cache:
        print(f"Using cached data for coordinates: {lat}, {lng}")
        return solar_data_cache[cache_key]['best_surface_details']

    solar_api_url = f"https://solar.googleapis.com/v1/buildingInsights:findClosest?location.latitude={lat}&location.longitude={lng}&requiredQuality=MEDIUM&key={GOOGLE_CLOUD_API_KEY}"
    response = requests.get(solar_api_url)
    
    if response.status_code == 200:
        data = response.json()
        print("Solar data retrieved successfully:")
        solar_potential = data.get('solarPotential', {})
        roof_segment_stats = solar_potential.get('roofSegmentStats', [])
        
        if roof_segment_stats:
            best_surface_details = process_solar_data_world(roof_segment_stats)
            if best_surface_details:
                print("Best surface details:")
                print(json.dumps(best_surface_details, indent=4))
                # Cache the best surface details with coordinates
                solar_data_cache[cache_key] = {'best_surface_details': best_surface_details}
                return best_surface_details
            else:
                print("Could not determine the best surface for solar panels.")
        else:
            print("No 'roofSegmentStats' found in 'solarPotential' or it is empty.")
    else:
        print(f"Error getting solar data: {response.text}")
    return None

def solar_panel_calculations(address):
    print(f"Calculating solar panel potential for {address}.")
    lat, lng = get_coordinates(address)
    if not lat or not lng:
        return {"error": "Could not get coordinates for the address provided."}

    return get_solar_data(lat, lng)

def process_solar_data_world(roof_segment_stats):
    print("Starting to process solar panel data...")
    
    best_surface = None
    max_electric_yield = 0

    for segment in roof_segment_stats:
        area_m2 = segment.get('stats', {}).get('areaMeters2', 0)
        azimuth_degrees = segment.get('azimuthDegrees', 0)
        pitch_degrees = segment.get('pitchDegrees', 0)
        sunshine_quantiles = segment.get('stats', {}).get('sunshineQuantiles', [])
        max_sunshine_hours_per_year = max(sunshine_quantiles) if sunshine_quantiles else 0

        electric_yield = calculate_electric_yield(area_m2, max_sunshine_hours_per_year)
        
        if electric_yield > max_electric_yield:
            max_electric_yield = electric_yield
            best_surface = {
                'area_m2': area_m2,
                'orientation': azimuth_degrees,
                'slope': pitch_degrees,
                'electric_yield': electric_yield
            }

    return best_surface

def calculate_electric_yield(area_m2, max_sunshine_hours_per_year):
    panel_capacity_watts = 300
    efficiency = 0.18
    electric_yield = area_m2 * max_sunshine_hours_per_year * panel_capacity_watts * efficiency / 1000
    return electric_yield

def process_solar_data(address, monthly_electrical_bill):
    lat, lng = get_coordinates(address)
    cache_key = f"{lat},{lng}"

    if cache_key in solar_data_cache:
        print(f"Using cached data for coordinates: {lat}, {lng}")
        best_surface_data = solar_data_cache[cache_key]['best_surface_details']
    else:
        best_surface_data = get_solar_data(lat, lng)
        if best_surface_data is not None:
            solar_data_cache[cache_key] = {'best_surface_details': best_surface_data}

    if best_surface_data is None:
        return {"error": "Best surface data could not be determined"}

    print(f"Processed Solar Data: {best_surface_data}")

    return financial.generate_solar_system_report(
        best_surface_data.get('area_m2', 0),
        best_surface_data.get('orientation', 0),
        best_surface_data.get('slope', 0),
        best_surface_data.get('electric_yield', 0),
        monthly_electrical_bill
    )