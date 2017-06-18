import calendar
from datetime import datetime, date, timedelta
from functools import wraps
import re
import time

from flask import abort, flash, redirect, render_template
from flask import request, url_for, send_file, session
from sqlalchemy import asc
import requests

from env import LOGIN, PASSWORD, BASE_URL
from model import Birthday, app, db, THIS_YEAR
from sms import send_sms
from text_on_image import download_url, create_img_with_text, CARDS

DEFAULT_FIRST_TAB = 'Upcoming'
TABS = [DEFAULT_FIRST_TAB] + [m[:3] for m in
                              list(calendar.month_name)[1:]]
UPCOMING_DAYS = 14
TWILIO_SMS_CHAR_LIMIT = 160


def login_required(test):
    '''From RealPython Flask course'''
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to log in first')
            return redirect(url_for('login'))
    return wrap


# other helpers

def _get_current_date():
    return date.today().replace(year=THIS_YEAR)


def _get_friend_or_abort(friendid):
    friend = Birthday.query.filter(Birthday.id == friendid).first()
    if not friend:
        abort(400, 'Not a valid friend id')
    return friend


def _is_valid_url(url):
    try:
        r = requests.get(url)
        return r.status_code == 200
    except:
        return False


@app.route('/login', methods=['GET', 'POST'])
def login():
    user = None
    status_code = 200
    if request.method == 'POST':
        user = request.form.get('username')
        password = request.form.get('password')
        if user != LOGIN or password != PASSWORD:
            flash('Invalid credentials')
            status_code = 401
        else:
            session['logged_in'] = user
            return redirect(url_for('index'))
    return render_template('login.html', user=user), status_code


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))


@app.route('/')
@login_required
def index():
    start = datetime.now() - timedelta(days=1)
    end = start + timedelta(days=UPCOMING_DAYS)
    now = _get_current_date()

    bdays = (Birthday.query.filter(Birthday.bday <= end)
             .filter(Birthday.bday >= start))

    return render_template("index.html",
                           data=bdays,
                           now=now,
                           active_tab=DEFAULT_FIRST_TAB,
                           tabs=TABS)


@app.route('/<int:month>')
@login_required
def bdays_month(month):
    if month not in range(1, 13):
        abort(400, 'Not a valid month')

    # SO questions/36155332
    _, num_days = calendar.monthrange(THIS_YEAR, month)
    start = date(THIS_YEAR, month, 1)
    end = date(THIS_YEAR, month, num_days)
    now = _get_current_date()

    # TODO: some duplication here with index()
    bdays = (Birthday.query.filter(Birthday.bday <= end)
             .filter(Birthday.bday >= start))

    month_name = calendar.month_name[month][:3]

    return render_template("index.html",
                           data=bdays,
                           now=now,
                           active_tab=month_name,
                           tabs=TABS)


@app.route('/search', methods=['GET'])
@login_required
def search():
    name = request.args.get('name')
    if not name.isalpha():
        print('Not isalpha string')
        return redirect(request.referrer)

    bdays = (Birthday.query
             .filter(Birthday.name.like("%{}%".format(name)))
             .order_by(asc(Birthday.bday)).all())

    now = _get_current_date()
    title = 'Search'
    tabs = [title] + TABS[1:]

    return render_template("index.html",
                           data=bdays,
                           now=now,
                           active_tab=title,
                           tabs=tabs)


@app.route('/friends/<int:friendid>', methods=['GET', 'POST'])
@login_required
def update(friendid):
    friend = _get_friend_or_abort(friendid)

    error = None

    if request.method == 'POST':
        phone = request.form.get('phone')
        if not phone:
            error = 'Please fill in phone number'
        elif not re.match('^\+\d+$', phone):
            error = 'Please fill in phone as +digits (e.g. +34666555444)'

        equal_phones_in_db = Birthday.query.filter(
                             Birthday.phone == phone).first()
        if equal_phones_in_db:
            error = '{} already in database'.format(phone)

        if not error:
            if friend.phone != phone:
                friend.phone = phone
                db.session.commit()

            return redirect(url_for('index'))

    return render_template('update.html', friend=friend, error=error)


@app.route('/birthday/<int:friendid>', methods=['GET'])
@login_required
def send_card(friendid):
    friend = _get_friend_or_abort(friendid)
    today = datetime.now()

    if today.day != friend.bday.day or today.month != friend.bday.month:
        abort(400, 'It is not his/her birthday')

    if not friend.phone:
        print('Need a phone number')
        return redirect(url_for('update', friendid=friendid))

    return render_template('card.html', friend=friend)


@app.route('/birthday/<int:friendid>/confirm', methods=['POST'])
@login_required
def confirm_card(friendid):
    if request.method != 'POST':
        abort(400, 'Post submit route only')

    msg = request.form.get('msg')
    url = request.form.get('url')
    action = request.form.get('action')

    if action not in ('verify', 'send'):
        abort(400, 'Invalid action')

    friend = _get_friend_or_abort(friendid)

    if action == 'verify':
        error = None
        utstamp = str(int(time.time()))

        if not msg:
            error = 'Please provide a message'
        elif len(msg) > TWILIO_SMS_CHAR_LIMIT:
            error = 'Max message size: {} chars'.format(TWILIO_SMS_CHAR_LIMIT)
        elif url and not _is_valid_url(url):
            error = 'URL not valid or reachable'

        if error:
            return render_template('card.html',
                                   friend=friend,
                                   msg=msg,
                                   url=url,
                                   error=error)

        if url:
            base_img = download_url(url)
            name = friend.name.replace(' ', '_').lower()
            img_dest = CARDS + '/' + name + '.png'
            create_img_with_text(base_img, msg, out_file=img_dest)
            url = url_for('get_card', name=name)
            print(url)

        return render_template('send.html',
                               friend=friend,
                               msg=msg,
                               url=url,
                               utstamp=utstamp)

    else:
        # good to send!

        if url:
            media = BASE_URL + url
        else:
            media = None

        try:
            send_sms(msg, media=media, to_phone=friend.phone)
        except Exception as exc:
            print('Cannot send SMS:')
            print(exc)
            print('Called send_sms with:')
            print(msg, media, friend.phone)

        confirmation = 'Birthday Message sent to {}'.format(friend.name)
        back_url = url_for('index')

        return render_template("send.html",
                               confirmation=confirmation,
                               back_url=back_url)


@app.route("/cards/<name>.png")
def get_card(name):
    img = 'cards/' + name + '.png'
    return send_file(img, mimetype='image/png')  # caching! add ?str in img tag


if __name__ == "__main__":
    app.run(debug=True)
