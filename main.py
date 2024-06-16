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
from app import App
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
                    help='Start date for orders query.')
parser.add_argument('-ed', '--end_date',
                    help='End date for orders query.')


args = parser.parse_args()
App.production = args.production
App.UserId = args.userid
App.password = args.password

if App.production:
    print('Production mode selected.')
else:
    print('Test mode selected.')

if args.letters:
    rides = rides('Rides_Customers.csv')
else:
    get_customers()

print('email generator ended.')

if __name__ == '__main__':
    pass