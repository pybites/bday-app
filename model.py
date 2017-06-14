import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from faker import Factory

from bdays import get_birthdays
from env import SECRET_KEY

LOCALHOST = 'http://127.0.0.1:5000'
THIS_YEAR = 2017

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///birthdays.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # mute warnings
app.secret_key = SECRET_KEY

db = SQLAlchemy(app)


class Birthday(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    bday = db.Column(db.DateTime)
    phone = db.Column(db.String(20))

    def __init__(self, name, bday, phone=None):
        self.name = name
        self.bday = bday
        self.phone = phone

    def __repr__(self):
        return '<Birthday %r %r %r>' % (self.name,
                                        self.bday,
                                        self.phone)


if __name__ == '__main__':
    # if ran as script create the birthday table and load in all birthdays
    test_mode = True  # no real names
    if len(sys.argv) > 1:
        test_mode = False

    fake = Factory.create()

    db.drop_all()
    db.create_all()

    for bd in sorted(get_birthdays('cal.ics'),
                     key=lambda x: (x.bday.month, x.bday.day)):

        # no real names
        if test_mode:
            name = fake.name()
        else:
            name = bd.name

        # import all bdays with THIS_YEAR to make it easier to query later
        bday = bd.bday.replace(year=THIS_YEAR)
        bd_obj = Birthday(name, bday)
        db.session.add(bd_obj)

    db.session.commit()
