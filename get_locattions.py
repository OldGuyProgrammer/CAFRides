#
# CAF Email Generator
#
# Get SquareUp Locations
#
# Indiana Wing CAF
# Jim Olivi 2024

import json
import os

from app import App
from square.http.auth.o_auth_2 import BearerAuthCredentials
from square.client import Client


def get_locations():

    print('Get locations from SquareUp')

    client = Client(
        bearer_auth_credentials=BearerAuthCredentials(
            access_token=os.environ['ACCESS_TOKEN']
        ),
        environment='production')

    result = client.locations.list_locations()

    if result.is_success():
        with open("locations.json", 'w') as locations_file:
            json.dump(result.body, locations_file)
        locations = result.body['locations']
    elif result.is_error():
        raise ConnectionError(result.errors)

    App.locations_list = [(loc['name'], loc['id']) for loc in locations]
    App.locations_names = [loc['name'] for loc in locations]

    return
