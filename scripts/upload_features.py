import os

import geopandas as gpd
import requests
from dotenv import load_dotenv
from shapely.geometry import mapping


def post_features_to_api(geojson_file_path, base_url, jwt_token):
    """Posts features from a GeoJSON file to the API.
    Parameters:
    - geojson_file_path: Path to the GeoJSON file containing the features.
    - base_url: Base URL of the API (e.g., http://localhost:8000).
    - jwt_token: JWT token for authentication.
    Returns:
    - True if all features were posted successfully, False otherwise.
    """

    api_url = f"{base_url}/features/"

    if(not valid_jwt_token(base_url, jwt_token)):
        print("Invalid JWT token. Please check your credentials and try again.")
        return False

    # Load GeoJSON data into a GeoDataFrame
    gdf = gpd.read_file(geojson_file_path)

    # track if all features were loaded successfully
    result = True

    print(f"Loaded GeoDataFrame with {len(gdf)} features")
    for index, row in gdf.iterrows():

        # build a feature dictionary.
        feature = {
            "type": "Feature",
            "geometry": mapping(row['geometry']), # Convert Shapely geometry to GeoJSON format
            "properties": {
                "name": row['name']
            }
        }
        headers = {'Content-Type': 'application/json' , 'Authorization': f'Bearer {jwt_token}'}
        response = requests.post(api_url, json=feature, headers=headers)

        # Log a message if the request was not successful
        if response.status_code != 201:
            print(f"Error {response.status_code} for {row['name']}: {response.text}")
            result = False
    return result

def get_jwt_token(base_url, username, password):
    """Obtains a JWT token from the API using the provided username and password.
    Parameters:
    - base_url: Base URL of the API (e.g., http://localhost:800
    - username: Username for authentication.
    - password: Password for authentication.
    Returns:
    - JWT token as a string if successful, None otherwise.
    """

    url = f"{base_url}/api/token/"
    data = {'username': username, 'password': password}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json().get('access')
    else:
        print(f"Failed to obtain JWT token: {response.status_code} - {response.text}")
        return None

def valid_jwt_token(base_url, token):
    """
    Validates the JWT token by making a request to the token verification endpoint.
    parameters:
    - base_url: Base URL of the API (e.g., http://localhost:8000)
    - token: JWT token to validate
    Returns True if the token is valid, False otherwise.

    """
    url = f"{base_url}/api/token/verify/"
    data = {'token': token}
    response = requests.post(url, data=data)
    return response.status_code == 200

if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file

    # Set configurable parameters from environment variables with defaults
    user_name = os.environ.get('API_USER_NAME')
    user_password = os.environ.get('API_USER_PASSWORD')
    api_base_url = os.environ.get('API_BASE_URL', 'http://localhost:8000')
    file_path = os.environ.get('GEOJSON_FILE_PATH', 'data/features.geojson')

    # Obtain JWT token for authentication
    token = get_jwt_token(api_base_url, user_name, user_password)
    if not token:
        print("Exiting due to failure in obtaining JWT token.")
        exit(1)

    # Post features from the GeoJSON file to the API
    result = post_features_to_api(file_path, api_base_url, token)

    if result:
        print("All features loaded successfully.")
    else:
        print("Some features failed to load.")
