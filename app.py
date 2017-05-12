import calendar
from datetime import datetime, date, timedelta

from flask import Flask, render_template, abort, redirect, request
from sqlalchemy import asc

from model import Birthday, app, db, THIS_YEAR

DEFAULT_FIRST_TAB = 'Upcoming'
TABS = [DEFAULT_FIRST_TAB] + [m[:3] for m in 
                              list(calendar.month_name)[1:]]
UPCOMING_DAYS = 14


@app.route('/')
def upcoming():
    start = datetime.now()
    end = start + timedelta(days=UPCOMING_DAYS)

    bdays = Birthday.query.filter(Birthday.bday <= end).filter(Birthday.bday >= start)

    return render_template("index.html", 
                           data=bdays, 
                           active_tab=DEFAULT_FIRST_TAB,
                           tabs=TABS)


@app.route('/<int:month>')
def bdays_month(month):
    if month not in range(1, 13):
        print('{} is not a valid month'.format(month))
        abort(400)

    # how to get first last dt of month?
    # http://stackoverflow.com/questions/36155332/how-to-get-the-first-day-and-last-day-of-current-month-in-python
    _, num_days = calendar.monthrange(THIS_YEAR, month)
    start = date(THIS_YEAR, month, 1)
    end = date(THIS_YEAR, month, num_days)

    bdays = Birthday.query.filter(Birthday.bday <= end).filter(Birthday.bday >= start)

    month_name = calendar.month_name[month][:3]

    return render_template("index.html", 
                           data=bdays, 
                           active_tab=month_name,
                           tabs=TABS)


@app.route('/search', methods=['GET'])
def search():
    name = request.args.get('name')
    if not name.isalpha():
        print('Not isalpha string')
        return redirect(request.referrer)
    bdays = Birthday.query.filter(Birthday.name.like("%{}%".format(name))).order_by(asc(Birthday.bday)).all()

    title = 'Search'
    tabs = [title] + TABS[1:]

    return render_template("index.html", 
                           data=bdays,
                           active_tab=title,
                           tabs=tabs)
    


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
