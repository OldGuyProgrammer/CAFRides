#
# Send Rides confirmation
#
# Indiana Wing CAF
# Jim Olivi 2024

import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
import os

import pandas as pd
import smtplib

from app import App


class Rides:
    def __init__(self, database):

        app = App()

        aircraft_df = app.aircraft_df

        print('Enter Rides Class Initializer')

        print('Data contained in: ' + database)

        # --** Begin SMTP - Jinja2 Mail Merge
        env = Environment(loader=FileSystemLoader('%s/templates' % os.path.dirname(__file__)))
        # --***************************************************

        rides_email = os.environ.get('INDYCAF_EMAIL_ADDRESS')
        rides_password = os.environ.get('RIDES_PASSWORD')
        if rides_email is None or rides_password is None:
            raise ValueError('From email address or password not specified.')

        try:
            customer_df = pd.read_csv(database)
        except FileNotFoundError:
            print('Pandas file not found: ' + database)
        except:
            print('Pandas file error: ' + database)
        else:
            # --** Start mailtrap code
            print('Send to Mailtrap')
            server = smtplib.SMTP('sandbox.smtp.mailtrap.io', 2525)
            server.starttls()
            id = os.environ.get('MAILTRAP_ID')
            password = os.environ.get('MAILTRAP_PASSWORD')
            try:
                server.login(id, password)
            except:
                print('Mailtrap login failed')
            # --****************************
            # --** Start Zoho Code
            # smtp_server = 'smtp.zoho.com'
            # smtp_port = 465
            # server = smtplib.SMTP_SSL(smtp_server, smtp_port)
            # server.login(rides_email, rides_password)
            # --***************************************
            template = env.get_template('Confirm_Without_Hold_Harmless.html')
            now = datetime.datetime.now()
            letter_date = str(now.month) + '/' + str(now.day) + '/' + str(now.year)
            for customer in customer_df.itertuples():
                message = MIMEMultipart()
                subject = 'Your upcoming Warbird Ride.'
                message['Subject'] = subject
                to_email = customer[3]
                purchaser = customer[1] + ' ' + customer[2]
                amount = str(customer[6])
                HH_text = ''
                if customer[7] == 'y':
                    print('HH Done')
                    HH = True
                    amount = ''
                else:
                    HH_text = 'Please click this link '
                    HH_text += '<a href=https://cafhq.formstack.com/forms/hh_master?'
                    HH_text += '&caf_hold_harmless=&signee_information=Adult+Rider+(ages+18+and+up)'
                    HH_text += '&which_unit=Indiana+Wing'
                    HH_text += '&Dollar+Amount+of+Total+Purchase='
                    HH_text += amount
                    HH_text += '&Which+Aircraft=AT6+/+SNJ+/+Harvard>'
                    HH_text += 'CAF Hold Harmless</a> '
                    HH_text += 'to complete necessary CAF paperwork. This will save time at the airport.'
                    HH = False

                message_html = template.render(date=letter_date, purchaser=purchaser, airplane=customer[4], airport=customer[8],
                                               hold_harmless=HH, date_of_flight=customer[5], HH_text=HH_text)
                message.attach((MIMEText(message_html, 'html')))
                try:
                    # --** Start mailtrap code
                    message = MIMEText(message_html, "html")
                    message["Subject"] = subject
                    message["From"] = rides_email
                    message['To'] = to_email
                    server.sendmail(
                        rides_email,
                        to_email,
                        message.as_string()
                    )
                    # --*************************************************8
                    # --** Zoho server send
                    # server.sendmail(rides_email, to_email, message.as_string())
                except Exception as error:
                    print(f'Sendmail failed: {error}')

                print(f'Confirmation sent to {purchaser}')
            server.quit()
