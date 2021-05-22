#!/usr/local/opt/python-3.9.0/bin/python3.9

import time
import sys
from datetime import datetime, timedelta

from cowin_api import CoWinAPI

import smtplib

# Slot Query
WEEKS = 2
DISTRICTS = ['294', '265']
AGE_LIMIT = 18
POLL_INTERVAL = 10

# Email Variables
SMTP_SERVER = 'smtp.gmail.com'  # Email Server (don't change!)
SMTP_PORT = 587  # Server Port (don't change!)
GMAIL_USERNAME = ''  # change this to match your gmail account
GMAIL_PASSWORD = ''  # change this to match your gmail password
sendTo = ''
emailSubject = "VACCINE SLOT at {}!!!"
emailContent = "Slot: {}, Date: {}, Pincode: {}"

class Emailer:
    def sendmail(self, recipient, subject, content):
        # Create Headers
        headers = ["From: " + GMAIL_USERNAME, "Subject: " + subject, "To: " + recipient,
                   "MIME-Version: 1.0", "Content-Type: text/html"]
        headers = "\r\n".join(headers)

        # Connect to Gmail Server
        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()

        # Login to Gmail
        session.login(GMAIL_USERNAME, GMAIL_PASSWORD)

        # Send Email & Exit
        session.sendmail(GMAIL_USERNAME, recipient, headers + "\r\n\r\n" + content)
        session.quit()


sender = Emailer()

cowin = CoWinAPI()

while True:
    try:
        start_dates = [datetime.now() + timedelta(days=i*7) for i in range(WEEKS)]
        dates = [start_date.strftime('%d-%m-%Y') for start_date in start_dates]

        for district in DISTRICTS:
            for date in dates:
                print("Fetching for date:", date, "district:", district)
                available_centers = cowin.get_availability_by_district(district, date, AGE_LIMIT)

                for center in available_centers['centers']:
                    for session in center['sessions']:
                        if session['available_capacity'] > 0:
                            content = emailContent.format(center["name"], session["date"], center["pincode"])
                            sender.sendmail(sendTo, emailSubject.format(center["name"]), content)
                            print(center["name"], available_centers)
    except(e):
        print(repr(e))
        sender.sendmail(sendTo, 'Error in vaccine script', e)
    sys.stdout.flush()
    time.sleep(POLL_INTERVAL)

