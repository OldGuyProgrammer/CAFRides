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
    parser.add_argument('-p', '--production', default=False, action='store_false',
                        help='Run program in production mode. Test mode will send emails to mailtrap.')
    parser.add_argument('id',
                        help='UserID - Not needed if added to environment variables. Overrides environment variable if entered.')
    parser.add_argument('password',
                        help='Password - Not needed if added to environment variables. Overrides environment variable if entered.')

    args = parser.parse_args()
    App.production = args.production
    App.UserId = args.id
    print(App.UserId)
    App.password = args.password
    print(App.password)

    if App.production:
        print('Production mode selected.')
    else:
        print('Test mode selected.')

    rides = rides('Rides_Customers.csv')

    print('email generator ended.')
