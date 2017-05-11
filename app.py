import calendar
from datetime import datetime, date, timedelta

from flask import Flask, render_template, abort, redirect, request

from model import Birthday, app, db, THIS_YEAR

MONTHS = list(calendar.month_name)[1:]
UPCOMING_DAYS = 14


@app.route('/')
def upcoming():
    start = datetime.now()
    end = start + timedelta(days=UPCOMING_DAYS)

    bdays = Birthday.query.filter(Birthday.bday <= end).filter(Birthday.bday >= start)

    return render_template("index.html", 
                           data=bdays, 
                           upcoming=UPCOMING_DAYS,
                           months=MONTHS)


@app.route('/<int:month>')
def bdays_month(month):
    if month not in range(1, 13):
        print('{} is not a valid month'.format(month))
        abort(400)

    month_name = calendar.month_name[month]

    # how to get first last dt of month?
    # http://stackoverflow.com/questions/36155332/how-to-get-the-first-day-and-last-day-of-current-month-in-python
    _, num_days = calendar.monthrange(THIS_YEAR, month)
    start = date(THIS_YEAR, month, 1)
    end = date(THIS_YEAR, month, num_days)

    bdays = Birthday.query.filter(Birthday.bday <= end).filter(Birthday.bday >= start)
    return render_template("index.html", 
                           data=bdays, 
                           month=month_name,
                           months=MONTHS)


@app.route('/notify/<int:person>')
def notify(person):
    bday = Birthday.query.get(person)
    if not bday:
        return redirect(request.referrer)
    bday.notify = False if bday.notify else True
    db.session.commit()
    return redirect(request.referrer)


if __name__ == "__main__":
    app.run(debug=True)
