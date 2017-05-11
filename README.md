# Simple Flask / Flask-SQLAlchemy Birthday App

Steps to get you up2speed

* Download your [FB birthday calendar](https://www.facebook.com/events/upcoming) 

	* Click the "Birthday" link under "You can add your events to Microsoft Outlook, Google Calendar or Apple Calendar..."

	* You should get a popup, something like: "Do you want to allow this page to open 'Calendar'?"

	* Click Allow. In your calendar app you should see the download link, something like webcal://www.facebook.com/ical/b.php?uid=YOUR_UID&key=SESSION_KEY

	* Strip off the 'webcal://www.' part and put the link in your browser. It should not download the ics file.

* Save the file as "cal.ics"

* Run model.py to import the birthdays into birthdays.db (SQLite). **Note** that for the article I used anonymous names so TEST_MODE is True. You probably want to use it with real names so set TEST_MODE to False

* Run the app and browse to http://127.0.0.1:5000/ - you should see the birthdays that are coming up the coming 14 days.

* Browse to any month int and you should see the birthdays for that month, e.g. http://127.0.0.1:5000/4

* TODO: as you see the notify column is set to False, I want you to be able to set this to True for certain friends so you get an email notification the day before. 
