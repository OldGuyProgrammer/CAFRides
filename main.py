#
# CAF Email Generator
#
# Read database containing names and other info and generate emails to the customers
#
# -> Send rides confirmation emails
#
# Indiana Wing CAF
# Jim Olivi 2024

from rides import Rides

# num-sent-emails = 0

if __name__ == '__main__':
    print('Start email generator')

    rides = Rides('Rides_Customers.csv')

    print('email generator ended.')
