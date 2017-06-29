# Never Forget A Friend's Birthday with Python, Flask and Twilio 

This app lets you:

- import your Facebook birthday calendar,
- send SMS notification messages of upcoming birthdays,
- send text messages and simple ecards via SMS.

Setup - how to run this on your box

1. Clone this repo:

		$ git clone https://github.com/pybites/bday-app

2. Import your birthday calendar from Facebook and save it as `cal.ics` in the app's folder

3. Populate SQLite database with birthdays in `cal.ics`:

		$ python model.py

	Use `-t` if you want to strip out real names.

4. Copy the [settings template](https://github.com/pybites/bday-app/blob/master/env-example.conf):

		$ cp env-example.conf env.conf

5. Add details:
	
	* twilio_api = from step 1
	* twilio phone = from step 1
	* admin phone = your number, where you want to receive notification messages
	* login / password = for the Flask app
	* server = unchanged if running locally, update to URL if deployed elsewhere 

6. Make a virtual env and install dependencies:

		$ python3 -m venv venv 
		$ source venv/bin/activate
		$ pip install -r requirements.txt

7. Kick off [the notifier cronjob](https://github.com/pybites/bday-app/blob/master/notify.py):

		$ nohup ./notify.py &
	
8. Start the Flask app: 

		$ python app.py
