#
# CAF Email Generator
#
# Read database containing names and other info and generate emails to the customers
#
# -> Get customer list from Square
#
# Indiana Wing CAF
# Jim Olivi 2024
import json
import os

from square.http.auth.o_auth_2 import BearerAuthCredentials
from square.client import Client

from app import App


def get_customers():
    print('Get customers requested.')

    if App.production:
        print('get_customers production mode.')
        client = Client(
        bearer_auth_credentials = BearerAuthCredentials(
            access_token= os.environ['ACCESS_TOKEN']
            ),
            environment='production')

        result = client.orders.search_orders(
            body={
                "location_ids": [
                    "L4Z5WSQDM9WSE"
                ],
                "query": {
                    "filter": {
                        "date_time_filter": {
                            "created_at": {
                                "start_at": "2024-06-02T00:00:00+00:00",
                                "end_at": "2024-06-13T00:00:00+00:00"
                            }
                        }
                    }
                }
            }
        )

        if result.is_error():
            print(result.errors)
        elif result.is_success():
            with open('orders.json', 'w') as orders_JSON:
                orders_JSON.write(json.dumps(result.body))
            orders_dict = result.body['orders']
    else:
        print('get_customers test mode.')
        with open('orders.json', 'r') as orders_json:
            orders_dict = json.load(orders_json)["orders"]
            for order in orders_dict:
                if 'line_items' in order:
                    for item in order['line_items']:
                        print(item['name'])
                        print(item['variation_name'])
                if 'fulfillments' in order:
                    for fulfillment in order['fulfillments']:
                        shipment = fulfillment['shipment_details']
                        recipient = shipment['recipient']
                        if 'email_address' in recipient:
                            print(recipient['email_address'])
                        if 'phone_number' in recipient:
                            print(recipient['phone_number'])
                        if 'address' in recipient:
                            address = recipient['address']
                            print(address['first_name'] + ' ' + address['last_name'])