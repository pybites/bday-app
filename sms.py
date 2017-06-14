from twilio.rest import Client
from env import ACCOUNT_SID, AUTH_TOKEN
from env import FROM_PHONE, ADMIN_PHONE

CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)


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
    media = 'https://sd.keepcalm-o-matic.co.uk/i/keep-calm-and-code-python-61.png'  # noqa E501
    send_sms(msg, media)
