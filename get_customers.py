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
from customer_df import CustomerData


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
            fulfillment_dict = {
                'item_name': [],
                'variation_name': [],
                'email_address': [],
                'phone_number': [],
                'customer_name': []
            }
            for order in orders_dict:
                if 'fulfillments' in order and 'line_items' in order:
                    for fulfillment in order['fulfillments']:
                        shipment = fulfillment['shipment_details']
                        recipient = shipment['recipient']
                        if 'email_address' in recipient:
                            fulfillment_dict['email_address'].append(recipient['email_address'])
                        else:
                            fulfillment_dict['email_address'].append('')

                        if 'phone_number' in recipient:
                            fulfillment_dict['phone_number'].append(recipient['phone_number'])
                        else:
                            fulfillment_dict['phone_number'].append('')
                        if 'address' in recipient:
                            address = recipient['address']
                            fulfillment_dict['customer_name'].append(address['first_name'] + ' ' + address['last_name'])
                        else:
                            fulfillment_dict['customer_name'].append('')
#        Assume that the first line item has flight information
                    line_item = order['line_items'][0]
                    fulfillment_dict['item_name'].append(line_item['name'])
                    fulfillment_dict['variation_name'].append(line_item['variation_name'])

        df = CustomerData(fulfillment_dict)

    print('Exit get_customers')