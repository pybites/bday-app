# Birthday App (bday-app)
> Never Forget A Friend's Birthday with Python, Flask and Twilio

[![GitHub issues][git-issues-image]][git-issues-url]
[![GitHub forks][git-forks-image]][git-forks-url]
[![GitHub stars][git-stars-image]][git-stars-url]
[![Twitter][twitter-image]][twitter-url]

This app lets you:

- import your Facebook birthday calendar,
- send SMS notification messages of upcoming birthdays,
- send text messages and simple ecards via SMS.

![app-printscreen](app-printscreen.png)

## Setup instructions

1. Clone this repo:

		$ git clone https://github.com/pybites/bday-app

2. Make a virtual env and install dependencies:

		$ cd bday-app
		$ python3 -m venv venv
		$ source venv/bin/activate
		$ pip install -r requirements.txt

3. Create a Twilio account, get a phone number and API key (sid) and token.

4. Copy the [settings template](https://github.com/pybites/bday-app/blob/master/env-example.conf) in place:

		$ cp env-example.conf env.conf

5. Update it with the correct settings:

	* flask - secret = set this to a random, hard to guess string (see [Flask docs](http://flask.pocoo.org/docs/0.12/quickstart/))
	* twilio_api - sid + token = obtained in step 3
	* phones - twilio = obtained in step 3
	* phones - admin = your (verified) mobile phone number, where you want to receive notification messages
	* login - user + password = define your login credentials for the Flask app
	* server - url = unchanged if running locally, update to base URL if deployed elsewhere (so far I only tested it on my localhost)

> NOTE: make sure you use E.164 number formatting for phone numbers (e.g. +34666555444, +442071838750). See Twilio's support article: [Formatting International Phone Numbers](https://support.twilio.com/hc/en-us/articles/223183008-Formatting-International-Phone-Numbers).

6. Import your FB calendar into local SQLite database with birthdays

	- Export your birthday calendar from Facebook and save it as `cal.ics` in the app's toplevel directory.

		![export FB cal](http://projects.bobbelderbos.com/twilio/import_birthdays.gif)

	- Run `model.py` to import the birthdays into the DB. Use it with `-t` if you want to strip out real names.

			$ python model.py

## How to run it

This app has two parts:

1. The [notifier](https://github.com/pybites/bday-app/blob/master/notify.py) which checks once a day for birthdays. If there are one or more birthdays that day it sends out an SMS to your configured admin phone. You need to run this as a background job so use `nohup`:

		$ nohup ./notify.py &

2. The front-end is a Flask app which you can invoke with:

		$ python app.py

Note that for both scripts you need to have your virtualenv enabled.


[git-issues-image]: https://img.shields.io/github/issues/pybites/bday-app.svg
[git-issues-url]: https://github.com/pybites/bday-app/issues
[git-forks-image]: https://img.shields.io/github/forks/pybites/bday-app.svg
[git-forks-url]: https://github.com/pybites/bday-app/network
[git-stars-image]: https://img.shields.io/github/stars/pybites/bday-app.svg
[git-stars-url]: https://github.com/pybites/bday-app/stargazers
[twitter-image]: https://img.shields.io/twitter/url/https/github.com/pybites/bday-app.svg?style=social
[twitter-url]: https://twitter.com/intent/tweet?text=Wow:&url=%5Bobject%20Object%5D
