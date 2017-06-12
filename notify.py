from datetime import datetime, timedelta
import time

from model import Birthday, app
from sqlalchemy import extract, and_
import schedule

from sms import send_sms

DAYS_IN_ADVANCE = 0
TODAY = datetime.now() + timedelta(days=DAYS_IN_ADVANCE)
BASE_URL = app.config.get('SERVER_NAME') or 'http://127.0.0.1:5000'
CARD_LINK = BASE_URL + '/birthday/{friendid}'
MSG = '''Birthday{plural} today:

{birthdays}'''


def _create_msg(entries):
    bdays = []
    for entry in entries:
        name = entry.name
        link = CARD_LINK.format(friendid=entry.id)
        entry = '{}\n{}\n'.format(name, link)
        bdays.append(entry)
    plural = 's' if len(bdays) > 1 else ''
    return MSG.format(plural=plural,
                      birthdays='\n'.join(bdays))


def job():
    bdays = Birthday.query.filter(and_(
            extract('day', Birthday.bday) == TODAY.day,
            extract('month', Birthday.bday) == TODAY.month,
            Birthday.phone != None)).all()

    if bdays:
        msg = _create_msg(bdays)
        send_sms(msg)


if __name__ == '__main__':
    schedule.every().day.at('00:01').do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
