#
# CAF Email Generator
#
# Read database containing names and other info and generate emails to the customers
#
# -> Send rides confirmation emails
#
# Indiana Wing CAF
# Jim Olivi 2024

import argparse
from app import App, check_params
from rides import rides
from get_customers import get_customers


print('Start email generator')

parser = argparse.ArgumentParser(description='Send confirmation emails to Rides customers based on .csv file listing names.')
parser.add_argument('-id', '--userid',
                    help='UserID - for production use the sender"s email address, for testing use the mailtrap account number.')
parser.add_argument('-pw','--password',
                    help='Password.')
parser.add_argument('-p', '--production', action='store_true',
                    help='Run program in production mode. Test mode will send emails to mailtrap.')
parser.add_argument('-l', '--letters', action='store_true',
                    help='Send the emails. If false, query SquareUp for customers.')
parser.add_argument('-sd', '--start_date',
                    help='Start date for orders query. Use format mm/dd/yyyy.')
parser.add_argument('-ed', '--end_date',
                    help='End date for orders query. Use format mm/dd/yyyy. If end date is not specified, only one day will be requested.')
parser.add_argument('-f', '--orders_csv',
                    help='Manditory: File name containing orders. This file is where the orders are written to and are read from.')

app = App()

args = parser.parse_args()
App.production = args.production
App.UserId = args.userid
App.password = args.password
App.orders_file = args.orders_csv
App.start_date = args.start_date
if args.end_date is not None:
    App.end_date = args.end_date
else:
    App.end_date = App.start_date

App.abort = False
print(check_params())
print(App.production)
print(App.start_date)
print(App.end_date)

print(App.abort)
if App.abort:
    quit()

if App.production:
    print('Production mode selected.')
else:
    print('Test mode selected.')

if args.letters:
    rides = rides(App.orders_file)
else:
    get_customers()

print('email generator ended.')

if __name__ == '__main__':
    pass