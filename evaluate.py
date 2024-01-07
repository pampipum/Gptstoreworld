import requests

def get_building_id(lat, lng):
    api_endpoint = "https://api3.geo.admin.ch/rest/services/all/MapServer/identify"
    delta = 0.01  # Example value for creating a bounding box, adjust as needed

    params = {
        "geometry": f"{lng},{lat}",
        "geometryType": "esriGeometryPoint",
        "layers": "all:ch.bfe.solarenergie-eignung-daecher",
        "returnGeometry": "true",
        "geometryFormat": "geojson",
        "tolerance": 5,  # Adjusted tolerance value
        "sr": 4326,
        "lang": "en",
        "imageDisplay": "1487,1027,96",
        "mapExtent": f"{lng-delta},{lat-delta},{lng+delta},{lat+delta}",  # Corrected mapExtent
        "limit": 10
    }
    
    request_url = f"{api_endpoint}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"
    print(f"Full API request URL: {request_url}")

    try:
        response = requests.get(api_endpoint, params=params)
        if response.status_code == 200:
            data = response.json()
            building_id = data['results'][0]['properties']['building_id']
            print(f"Retrieved Building ID: {building_id}")  # Print the building ID
            return building_id
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def get_solar_potential_for_building(building_id):
    api_endpoint = "https://api3.geo.admin.ch/rest/services/api/MapServer/find"
    params = {
        "layer": "ch.bfe.solarenergie-eignung-daecher",
        "searchText": building_id,  # Use 'searchText' instead of 'layerDefs'
        "searchField": "building_id",  # Specify the search field
        "returnGeometry": "false",  # Set 'returnGeometry' to false
        "contains": "false",  # Set 'contains' to false
    }

    # Construct the full URL for debugging
    request_url = f"{api_endpoint}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"
    print(f"Full API request URL for building: {request_url}")

    try:
        response = requests.get(api_endpoint, params=params)
        if response.status_code == 200:
            return process_solar_data(response.json())
        else:
            return {"error": f"API request failed with status code {response.status_code}"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

def convert_orientation(orientation):
    if orientation >= -22.5 and orientation < 22.5:
        return "N"
    elif orientation >= 22.5 and orientation < 67.5:
        return "NE"
    elif orientation >= 67.5 and orientation < 112.5:
        return "E"
    elif orientation >= 112.5 and orientation < 157.5:
        return "SE"
    elif orientation >= 157.5 or orientation < -157.5:
        return "S"
    elif orientation >= -157.5 and orientation < -112.5:
        return "SW"
    elif orientation >= -112.5 and orientation < -67.5:
        return "W"
    elif orientation >= -67.5 and orientation < -22.5:
        return "NW"
    else:
        return "Unknown"

def process_solar_data(data):
    all_surfaces = []

    for feature in data.get('results', []):
        properties = feature.get('attributes', {})
        all_surfaces.append(properties)

    # Count the number of roof surfaces
    num_surfaces = len(all_surfaces)

    if num_surfaces == 0:
        return {"error": "No roof surfaces found"}

    # Find the surface with the highest 'stromertrag' (electricity yield) value
    best_surface = max(all_surfaces, key=lambda x: x.get('stromertrag', 0))

    # Convert orientation to cardinal direction
    orientation = convert_orientation(best_surface.get('ausrichtung', 0))

    # Get the 7 most important data points for the chosen surface
    top_6_data = {
        "area": best_surface.get('flaeche', ""),
        "orientation": orientation,
        "slope": best_surface.get('neigung', ""),
        "mean_radiation": best_surface.get('mstrahlung', ""),
        "electric_yield": best_surface.get('stromertrag', ""),
        "monthly_yield": best_surface.get('monats_ertrag', "")
    }

    return {
        "num_surfaces": num_surfaces,
        "best_surface_data": top_6_data
    }