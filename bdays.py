from collections import namedtuple
import sys

from icalendar import Calendar

DEFAULT_CAL = 'cal.ics'

Bday = namedtuple('Bday', 'name bday')


def get_birthdays(cal):
    with open(cal, 'rb') as g:
        gcal = Calendar.from_ical(g.read())
        for component in gcal.walk():
            if component.name == "VEVENT":
                name = component.get('SUMMARY')
                if not name:
                    continue
                name = name.replace("'s birthday", "")
                bday = component.get('DTSTART').dt
                yield Bday(name=name, bday=bday)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        cal = DEFAULT_CAL
    else:
        cal = sys.argv[1]

    for bday in get_birthdays(cal):
        print(bday)
