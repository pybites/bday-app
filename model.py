from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///birthdays.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # mute warnings
db = SQLAlchemy(app)


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
    # sorted by month->day

    from bdays import get_birthdays

    db.create_all()

    for bd in sorted(get_birthdays('cal.ics'), key=lambda x: (x.month, x.day)):
    	db.session.add(Birthday(bd.name, bd.month, bd.day))

    db.session.commit()
