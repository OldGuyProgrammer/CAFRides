#
# CAF Email Generator
#
# Create new customer Dataframe
#
# Indiana Wing CAF
# Jim Olivi 2024

import pandas as pd


class CustomerData:
    def __init__(self, customer_dict):
        print("Create new customer dictionary.")

        for key, value in customer_dict.items():
            print(key + ": " + str(value))
        self.customers_df = pd.DataFrame(customer_dict)


    def __del__(self):
        print('Saving data.')
        self.customers_df.to_csv('orders.csv', index=False)