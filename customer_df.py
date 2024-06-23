#
# CAF Email Generator
#
# Create new customer Dataframe
#
# Indiana Wing CAF
# Jim Olivi 2024

import pandas as pd
from app import App


class CustomerData:
    def __init__(self, customer_dict):
        print("Create new customer orders file.")

        self.customers_df = pd.DataFrame(customer_dict)


    def __del__(self):
        print('Saving data.')
        if not App.orders_file:
            raise FileNotFoundError('csv file not specified.')
        self.customers_df.to_csv(App.orders_file, index=False)
        print('Orders written to: ' + App.orders_file)