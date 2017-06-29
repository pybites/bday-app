#!/usr/bin/env python
from datetime import datetime, timedelta
import logging
import time

from model import Birthday
from sqlalchemy import extract, and_
import schedule

from env import BASE_URL
from sms import send_sms

DAYS_IN_ADVANCE = 0
TODAY = datetime.now() + timedelta(days=DAYS_IN_ADVANCE)
LOCALHOST = 'http://127.0.0.1:5000'
CARD_LINK = BASE_URL + '/birthday/{friendid}'
MSG = '''Birthday{plural} today:

{birthdays}'''

logging.basicConfig(filename='notify.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)  # only log for this module, not 3rd party


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
            Birthday.phone != None)).all()  # noqa E711

    if not bdays:
        logger.debug('no birthdays')
        return

    logger.debug('upcoming birthday: {}'.format(bdays))
    msg = _create_msg(bdays)
    logger.debug('sending SMS msg: {}'.format(msg))
    try:
        send_sms(msg)
        logger.debug('message sent ok')
    except Exception as exc:
        logger.error('message not sent, error: {}'.format(exc))


if __name__ == '__main__':
    schedule.every().day.at('00:05').do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
