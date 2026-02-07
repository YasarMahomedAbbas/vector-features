import geopandas as gpd
import requests
from shapely.geometry import mapping

FILE_PATH = 'data/municipalities_nl.geojson'
API_URL = 'http://localhost:8000/features/'

def load_data(geojson_file_path, api_url):

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
        response = requests.post(api_url, json=feature)

        # Log a message if the request was not successful
        if response.status_code != 201:
            print(f"Error {response.status_code} for {row['name']}: {response.text}")
            result = False
    return result

if __name__ == "__main__":

    result = load_data(FILE_PATH, API_URL)
    if result:
        print("All features loaded successfully.")
    else:
        print("Some features failed to load.")
