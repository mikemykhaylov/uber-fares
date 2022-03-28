import json
from datetime import datetime
from typing import TypedDict, Union, Dict, List
from zoneinfo import ZoneInfo

import functions_framework
import holidays
import pandas as pd
from flask import Flask
from geopy import distance
from google.api_core.client_options import ClientOptions
from google.cloud import aiplatform
from numpy import ndarray
from pandas import DataFrame, Series
from schema import Schema, SchemaError
from shapely.geometry import Point, shape


class Location(TypedDict):
    lat: int
    lng: int


class RequestData(TypedDict):
    pickup: Location
    dropoff: Location
    passenger_count: int
    year: int


location_schema = Schema({"lat": lambda val: -90 <= val <= 90, "lng": lambda val: -180 <= val <= 180})
request_schema = Schema({
    "pickup": location_schema,
    "dropoff": location_schema,
    "passenger_count": lambda val: 1 <= val <= 6,
    "year": lambda val: 2008 <= val <= 2015
})


def get_neighborhood(point, nyc_neighborhoods):
    """Calculates the neighborhood to which the point belongs

        Args:
          point(Point): Geographical point
          nyc_neighborhoods(dict): Dictionary of NYC Neighborhoods and their geolocation

        Returns:
          str: Neighborhood string or Outside NYC if out of bounds

        """
    for feature in nyc_neighborhoods["features"]:
        polygon = shape(feature["geometry"])
        if polygon.contains(point):
            return feature["properties"]["neighborhood"]
    return "Outside NYC"


def validate_request(request_json) -> Union[RequestData, list[str]]:
    try:
        data: RequestData = request_schema.validate(request_json)
        return data
    except SchemaError as e:
        return e.autos


def preprocess_data(data: RequestData) -> ndarray:
    df: DataFrame = pd.read_csv('./src/empty_features.csv')
    df = df.iloc[1:, :]
    curr_date = datetime.now(tz=ZoneInfo('America/New_York'))
    past_date = datetime(data['year'], curr_date.month, curr_date.day, curr_date.hour)

    new_entry = {
        'year':
            data['year'] - 2008,
        'is_holiday':
            past_date.date() in holidays.US(state="NY", years=past_date.year),
        'passenger_count':
            data['passenger_count'],
        'distance':
            distance.distance((data['pickup']['lat'], data['pickup']['lng']),
                              (data['dropoff']['lat'], data['dropoff']['lng'])).km,
        f'month_{past_date.month}':
            1,
        f'hour_{past_date.hour}':
            1,
        f'weekday_{past_date.weekday()}':
            1
    }

    geojson_path = "./src/nyc_neighborhoods.geo.json"
    with open(geojson_path) as f:
        nyc_neighborhoods = json.load(f)
        pickup_point = Point(data['pickup']['lng'], data['pickup']['lat'])
        pickup_neighborhood = get_neighborhood(pickup_point, nyc_neighborhoods)
        new_entry[f'pickup_neighborhood_{pickup_neighborhood}'] = 1

        dropoff_point = Point(data['dropoff']['lng'], data['dropoff']['lat'])
        dropoff_neighborhood = get_neighborhood(dropoff_point, nyc_neighborhoods)
        new_entry[f'dropoff_neighborhood_{dropoff_neighborhood}'] = 1
    df = pd.concat([df, pd.DataFrame([new_entry])]).fillna(0)
    out: Series = df.iloc[0]
    out: ndarray = out.to_numpy()
    return out


def predict_custom_trained_model_sample(
    project: str,
    endpoint_id: str,
    instances: Union[Dict, List[Dict]],
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
) -> float:
    """
    `instances` can be either single instance of type dict or a list
    of instances.
    """
    client_options = ClientOptions(api_endpoint=api_endpoint)
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    endpoint = client.endpoint_path(project=project, location=location, endpoint=endpoint_id)
    response = client.predict(endpoint=endpoint, instances=instances['instances'])
    predictions = response.predictions
    return predictions[0]


@functions_framework.http
def main(request: Flask.request_class):
    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows POST requests from any origin with the Content-Type
        # header and caches preflight response for 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return '', 204, headers

    # Disallow non-POSTs
    if request.method != 'POST':
        return 'Not found', 404

    # Set CORS headers for the main request
    headers = {'Access-Control-Allow-Origin': '*'}

    request_json = request.get_json()

    request_data = validate_request(request_json)
    if 'passenger_count' not in request_data:
        return {'errors': request_data}, 400

    features = preprocess_data(request_data)

    prediction = predict_custom_trained_model_sample(project="828440099324",
                                                     endpoint_id="1173407605255569408",
                                                     location="us-central1",
                                                     instances={"instances": [list(features)]})

    return {'prediction': prediction}, 200, headers
