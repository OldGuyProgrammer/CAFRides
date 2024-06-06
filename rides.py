#
# Send Rides confirmation
#
# Indiana Wing CAF
# Jim Olivi 2024

import pandas as pd
import smtplib


class Rides:
    def __init__(self, database):

        smtp_server = 'sandbox.smtp.mailtrap.io'
        port = 2525
        login = '6f5e80fce2ea00'
        password = 'c26f1d3a41d801'

        print('Enter Rides Class Initializer')

        print('Data contained in: ' + database)

        message_HH_done = '''
Indiana Wing 
Commemorative Air Force



Dear {purchaser},

Thank you for purchasing a ride in the {airplane}  on {date_of_flight}. It will be an exciting ride on a genuine World War 2 warbird. Please arrive at {airport} at least one hour before your flight to get prepared and to complete any leftover paperwork. 

Dress comfortably. There are canopies on the airplane, but it will be breezy. Long pants are recommended. Closed toe shoes are required (no sandals). We will provide a headset so that you can hear the pilot communicate with other air traffic and for you to talk to the pilot. You can bring your own aviation headset, if you want.

If you have any questions, do not hesitate to call me at 317-584-7852.

Col. Jim Olivi
Indiana Wing, Commemorative Air Force
Rides Coordinator
317-584-7852
rides@indianawingcaf.org
        '''

        message_needs_HH = '''
Indiana Wing 
Commemorative Air Force



Dear {purchaser},

Thank you for purchasing a ride in the {airplane}  on {date_of_flight}. It will be an exciting ride on a genuine World War 2 warbird. Please arrive at {airport} at least one hour before your flight to get prepared and to complete any leftover paperwork. 

Dress comfortably. There are canopies on the airplane, but it will be breezy. Long pants are recommended. Closed toe shoes are required (no sandals). We will provide a headset so that you can hear the pilot communicate with other air traffic and for you to talk to the pilot. You can bring your own aviation headset, if you want.

Please click this link https://cafhq.formstack.com/forms/hh_master to fill out the required Commemorative Air Force form. This will save time at the airport.

If you have any questions, do not hesitate to call me at 317-584-7852.

Col. Jim Olivi
Indiana Wing, Commemorative Air Force
Rides Coordinator
317-584-7852
rides@indianawingcaf.org
                '''

        try:
            customer_df = pd.read_csv(database)
        except FileNotFoundError:
            print('Pandas file not found: ' + database)
        except:
            print('Pandas file error.')
        else:
            print('Database Read Successful')
            with smtplib.SMTP(smtp_server, port) as server:
                server.login(login, password)
                for r in customer_df.itertuples():
                    purchaser = r[1] + ' ' + r[2]
                    email = r[3]
                    airplane = r[4]
                    date_of_flight = r[5]
                    HH_Needed = r[6]
                    if HH_Needed == 'y':
                        message = message_needs_HH
                    else:
                        message = message_HH_done

                    server.sendmail(
                        'test-center@example.com',
                        email,
                        message.format(purchaser=purchaser, recipient=email, airplane=airplane, date_of_flight=date_of_flight, airport='Zionsville')
                    )
                    print(f'Confirmation sent to {purchaser}')



