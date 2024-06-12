#
# Send Rides confirmation
#
# Indiana Wing CAF
# Jim Olivi 2024

import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from time import sleep

from jinja2 import Environment, FileSystemLoader
import os

import pandas as pd
import smtplib
from smtplib import SMTPException

from app import App


def rides(database):

    app = App()
    aircraft_df = app.aircraft_df

    print('Enter Rides Class Initializer')

    print('Data contained in: ' + database)

    # --** Begin SMTP - Jinja2 Mail Merge
    env = Environment(loader=FileSystemLoader('%s/templates' % os.path.dirname(__file__)))
    # --***************************************************

    rides_id = App.UserId
    rides_password = App.password

    if rides_id is None or rides_password is None:
        raise ValueError('From email address or password not specified.')

    try:
        customer_df = pd.read_csv(database)
        customer_df = customer_df.drop(customer_df[customer_df.Send_Email == 'n'].index)
    except FileNotFoundError:
        print('Pandas file not found: ' + database)
    except:
        print('Pandas file error: ' + database)
    else:
        # --** Start mailtrap code
        if not App.production:
            print('Send to Mailtrap')
            server = smtplib.SMTP('sandbox.smtp.mailtrap.io', 2525)
            server.starttls()
            try:
                server.login(rides_id, rides_password)
            except:
                print('Mailtrap login failed')
        # --****************************
        # --** Start Zoho Code
        else:
            try:
                print('Send from Zoho.')
                smtp_server = 'smtp.zoho.com'
                smtp_port = 465
                server = smtplib.SMTP_SSL(smtp_server, smtp_port)
                server.login(str(rides_id), str(rides_password))
            except SMTPException as error:
                raise ReferenceError('SMTP error: ' + str(error))
        # --***************************************
        template = env.get_template('Confirm_Without_Hold_Harmless.html')
        now = datetime.datetime.now()
        letter_date = str(now.month) + '/' + str(now.day) + '/' + str(now.year)
        for customer in customer_df.itertuples():
            message = MIMEMultipart()
            subject = 'Your upcoming Warbird Ride.'
            message['Subject'] = subject
            message['From'] = rides_id
            to_email = customer[3]
            message['To'] = to_email
            purchaser = customer[1] + ' ' + customer[2]
            amount = str(customer[6])
            HH_text = ''
            if customer[7] == 'y':
                HH = True
                amount = ''
            else:
                HH_text = 'Please click this link '
                HH_text += '<a href=https://cafhq.formstack.com/forms/hh_master?'
                HH_text += '&caf_hold_harmless=&signee_information=Adult+Rider+(ages+18+and+up)'
                HH_text += '&which_unit=Indiana+Wing'
                HH_text += '&Dollar+Amount+of+Total+Purchase='
                HH_text += amount
                HH_text += '&which+aircraft='
                hh_aircraft = app.get_aircraft(customer[4]).replace(' ', '+')
                HH_text += hh_aircraft + '>'
                HH_text += 'CAF Hold Harmless</a> '
                HH_text += 'to complete necessary CAF paperwork. This will save time at the airport.'
                HH = False

            message_html = template.render(date=letter_date, purchaser=purchaser, airplane=customer[4],
                                           airport=customer[8],
                                           hold_harmless=HH, date_of_flight=customer[5])
            message.attach((MIMEText(message_html, 'html')))
            try:
                if not App.production:
                    # --** Start mailtrap code
                    message = MIMEText(message_html, "html")
                    message["Subject"] = subject
                    message["From"] = rides_id
                    message['To'] = to_email
                    server.sendmail(
                        rides_id,
                        to_email,
                        message.as_string()
                    )
                    # --*************************************************8
                else:
                    # --** Zoho server send
                    server.sendmail(rides_id, to_email, message.as_string())
            except Exception as error:
                print(f'Sendmail failed: {error}')

            print(f'Confirmation sent to {purchaser}')
            sleep(1)
        server.quit()
