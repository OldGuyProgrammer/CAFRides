#
# Send Rides confirmation
#
# Indiana Wing CAF
# Jim Olivi 2024

import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
import os

import pandas as pd
import smtplib


class Rides:
    def __init__(self, database):

        print('Enter Rides Class Initializer')

        print('Data contained in: ' + database)

# --** Begin SMTP - Jinja2 Mail Merge
        env = Environment(loader=FileSystemLoader('%s/templates' % os.path.dirname(__file__)))
# --***************************************************

        rides_email = os.environ.get('INDYCAF_EMAIL_ADDRESS')
        print(rides_email)
        rides_password = os.environ.get('RIDES_PASSWORD')
        print(rides_password)
        if rides_email is None or rides_password is None:
            raise ValueError('From email address or password not specified.')

        try:
            customer_df = pd.read_csv(database)
        except FileNotFoundError:
            print('Pandas file not found: ' + database)
        except:
            print('Pandas file error: ' + database)
        else:
            print('Database Read Successful')

# --** Start mailtrap code
#             with smtplib.SMTP('sandbox.smtp.mailtrap.io', 2525) as server:
#                 server.starttls()
#                 server.login('', '')
# --****************************
            smtp_server = 'smtp.zoho.com'
            smtp_port = 465
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
            server.login(rides_email, rides_password)
            template = env.get_template('Confirm_Without_Hold_Harmless.html')
            for customer in customer_df.itertuples():
                message = MIMEMultipart()
                message['Subject'] = 'Your upcoming Warbird Ride.'
                purchaser = customer[1] + ' ' + customer[2]
                if customer[6] == 'y':
                    HH = True
                else:
                    HH = False
                message_html = template.render(purchaser=purchaser, airplane=customer[4], airport=customer[7], hold_harmless=HH, date_of_flight=customer[5])
                message.attach((MIMEText(message_html, 'html')))
                try:
                    server.sendmail(rides_email, customer[3], message.as_string())
                except Exception as error:
                    print(f'Sendmail failed: {error}')
# --** Start mailtrap code
#                 server.sendmail(
#                     'test-center@example.com',
#                     customer[3],
#                     message
#                 )
# --*************************************************8
                print(f'Confirmation sent to {purchaser}')
            server.quit()
