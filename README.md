# vector-features

A REST API built using the Django REST Framework  serving vector features in a GeoJSON compatible format.
The following endpoints are provided

```
  - GET /features/ — List features (public)
  - POST /features/ — Create a feature (requires auth)
  - GET /features/{id}/ — Feature detail (public)
  - PUT /features/{id}/ — Update feature (requires auth)
  - DELETE /features/{id}/ — Delete feature (requires auth)
  - POST /api/token/ — Obtain JWT token
  - POST /api/token/refresh/ — Refresh JWT token

```

  ## Table of Contents                                                                                                                                       
  - [Deployment - Docker with Docker Compose](#oDeployment---docker-with-docker-compose)
  - [Deployment- Local Development](#deployment---local-development)                                                                                                                  
  - [Usage](#usage) 



## Deployment - Docker with Docker Compose.


### Requirements

- Docker & Docker Compose

### Setup & Run

1. Clone the repository
2. Create a `.env` file with the following variables:
```bash
    POSTGIS_USER=
    POSTGIS_PASSWORD=
    POSTGIS_DB_NAME=
    DJANGO_SUPERUSER_USERNAME=
    DJANGO_SUPERUSER_PASSWORD=
    DJANGO_SUPERUSER_EMAIL=
```
You may copy the .env.example by running 
```bash
cp .env.example .env
```
and filling out appropriate fields.

3. Start the application:
```bash
docker compose up --build
```
A superuser account will be created with the username and password set in the .env file.

The API will be available at http://localhost:8000/features/ 

## Deployment - Local Development                                                                                                            
                                                                                                                                                             
### Requirements
- Python 3.14
- GDAL
- PostgreSQL with PostGIS extension

### Setup & Run

1. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create a `.env` file with the following variables:
```bash
POSTGIS_USER=
POSTGIS_PASSWORD=
POSTGIS_DB_NAME=
DJANGO_SUPERUSER_USERNAME=
DJANGO_SUPERUSER_PASSWORD=
DJANGO_SUPERUSER_EMAIL=
```
You may copy the .env.example by running 
```bash
cp .env.example .env
```
and filling out appropriate fields.

4. Create a PostGIS database
```bash
psql -U postgres                                                                                                                                     
CREATE DATABASE vector_features_db;                                                                                                                     
\c vector_features_db
CREATE EXTENSION postgis;
```
Alternatively, you can use the PostGIS database from the included docker compose by running 
```bash
docker compose up db 
```
and keeping `DB_HOST=127.0.0.1` in your `.env`.

5. Run migrations:
```bash
python manage.py migrate
```
6. Create a superuser:
```bash
python manage.py createsuperuser
```
**IMPORTANT:** *This command will prompt you for a username and password, ensure the username and password are set in the .env file as these are used by the `upload_features.py` script.*

7. Start the server:

```bash
python manage.py runserver
```

8. Running tests

```bash
python manage.py test
```

 
 ## Usage 
When the server is running:

To upload the municipalities_nl.geojson
run: 
```bash
docker compose exec web python scripts/upload_features.py
```
or for local development
```bash
python scripts/upload_features.py
```

---

while you are not authenticated, you have READONLY access, i.e. you may view all features available and feature details of a specific feature. 


Navigate to `localhost:8000/features` for a list of all available features, features are paginated with 100 features per page.

Navigate to `localhost:8000/features/{id}` to view a specific feature with more details (i.e. the geometry).


### Filtering

Bounding box filter:
```
GET /features/?in_bbox=min_lon,min_lat,max_lon,max_lat
```

Example: Bounding box surrounding the Groningen Province:
```bash
curl "http://localhost:8000/features/?in_bbox=6.0,53.0,7.3,53.6" 
```
**Note: Ensure that you've run the upload_features script first and the results may include features from neighboring areas**

---
To gain access to update or delete features, authenticate yourself by navigating to `localhost:8000/admin` and login with the username and password you created. 

Once logged in, naviging to `localhost:8000/features` or `localhost:8000/features/{id}` will have more available options. 

You are able to create a feature with the following parameters *NOTE: Name is Mandatory*

name: `Municipality-name`

geometry: `{"type": "MultiPolygon", "coordinates": [[[[5.0, 52.0], [5.1, 52.0], [5.1, 52.1], [5.0, 52.1], [5.0, 52.0]]]]}`

OR

As a raw data field

content:  
```json
{                                                                                                                                                          
      "type": "Feature",                                                                                                                                   
      "geometry": {                                                                                                                                          
          "type": "MultiPolygon",                                                                                                                            
          "coordinates": [[[[5.0, 52.0], [5.1, 52.0], [5.1, 52.1], [5.0, 52.1], [5.0, 52.0]]]]                                                               
      },                                                                                                                                                   
      "properties": {
          "name": "Test Municipality"
      }
  }
```

### API Usage                                                             
Get a JWT token:                                                                                                                                           
```bash                                                                                                                                                    
curl -X POST http://localhost:8000/api/token/ \
-H "Content-Type: application/json" \
-d '{"username": "your_username", "password": "your_password"}'

```

List features (public):
```bash
curl http://localhost:8000/features/
```

Get a single feature (public):
```bash
curl http://localhost:8000/features/1/
```
Create a feature (requires auth):

```bash
curl -X POST http://localhost:8000/features/ \
-H "Authorization: Bearer <your_access_token>" \
-H "Content-Type: application/json" \
-d '{
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [5.0, 52.0]},
    "properties": {"name": "Example Feature"}
}'

```
Delete a feature (requires auth):

```bash
curl -X DELETE http://localhost:8000/features/1/ \
-H "Authorization: Bearer <your_access_token>"
```