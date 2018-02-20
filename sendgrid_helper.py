# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import sendgrid
import os
from sendgrid.helpers.mail import *

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

def send_email(name, send_from, subject, comment, send_to):
    """Uses the SendGrid api to send user an email."""

    sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
    from_email = Email(send_from)
    to_email = Email(send_to)
    subject = subject
    content = Content("text/plain", comment)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)