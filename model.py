from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# for printscreens for blog post I want real dates, but names stripped out
from helpers import get_random_name

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///birthdays.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # mute warnings
db = SQLAlchemy(app)

TEST_MODE = True  # no real names
THIS_YEAR = 2017


class Birthday(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    bday = db.Column(db.DateTime)
    notify = db.Column(db.Boolean)

    def __init__(self, name, bday, notify=False):
        self.name = name
        self.bday = bday
        self.notify = False

    def __repr__(self):
        return '<Birthday %r %r %r>' % (self.name, self.bday, self.notify)


if __name__ == '__main__':
    # if ran as script create the birthday table and load in all birthdays

    from bdays import get_birthdays

    db.drop_all()
    db.create_all()

    for bd in sorted(get_birthdays('cal.ics'), key=lambda x: (x.bday.month, x.bday.day)):

        # no real names
        if TEST_MODE:
            name = get_random_name()
        else:
            name = bd.name
    
        # import all bdays with THIS_YEAR to make it easier to query later
        bday = bd.bday.replace(year=THIS_YEAR)
        bd_obj = Birthday(name, bday)
        db.session.add(bd_obj)

    db.session.commit()
