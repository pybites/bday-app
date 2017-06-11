import os
import sys

from twilio.rest import Client

ACCOUNT_SID = os.environ.get('TWILIO_SID') or sys.exit('need account sid')
AUTH_TOKEN = os.environ.get('TWILIO_TOK') or sys.exit('need auth token')
CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)

FROM_PHONE = os.environ.get('TWILIO_FROM_PHONE')
if not FROM_PHONE:
    sys.exit('need Twilio phone number to send from')

ADMIN_PHONE = os.environ.get('TWILIO_ADMIN_PHONE')
if not ADMIN_PHONE:
    sys.exit('need admin phone to send notifications to')


def send_sms(message, media=None, to_phone=ADMIN_PHONE):
    message = CLIENT.messages.create(
        from_=FROM_PHONE,
        to=to_phone,
        body=message,
        media_url=media,
    )
    return message.sid


if __name__ == '__main__':
    msg = 'Keep cool and code in Python'
    media = 'https://sd.keepcalm-o-matic.co.uk/i/keep-calm-and-code-python-61.png'
    send_sms(msg, media)
