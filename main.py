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

if __name__ == '__main__':
    print('Start email generator')

    parser = argparse.ArgumentParser(description='Send confirmation emails to Rides customers based on .csv file listing names.')
    parser.add_argument('-id', '--userid',
                        help='UserID - for production use the sender"s email address, for testing use the mailtrap account number.')
    parser.add_argument('-pw','--password',
                        help='Password.')
    parser.add_argument('-p', '--production', action='store_true',
                        help='Run program in production mode. Test mode will send emails to mailtrap.')

    args = parser.parse_args()
    App.production = args.production
    App.UserId = args.userid
    App.password = args.password

    if App.production:
        print('Production mode selected.')
    else:
        print('Test mode selected.')

    rides = rides('Rides_Customers.csv')

    print('email generator ended.')
