import configparser

config = configparser.ConfigParser()
config.read("env.conf")

SECRET_KEY = config['flask']['secret']

TWILIO_ACCOUNT_SID = config['twilio_api']['sid']
TWILIO_AUTH_TOKEN = config['twilio_api']['token']

FROM_PHONE = config['phones']['twilio']
ADMIN_PHONE = config['phones']['admin']

LOGIN = config['login']['user']
PASSWORD = config['login']['password']

BASE_URL = config['server']['url'].rstrip('/')
