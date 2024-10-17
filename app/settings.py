from dotenv import load_dotenv
from os import getenv as env

""" File that contains project constants pulled from .env file"""

load_dotenv()

APP_NAME=env('APP_NAME','app')
APP_FONT=env('APP_FONT','doom')
APP_VERSION=env('APP_VERSION', '1.0.0-alpha.1')
MAX_UNCHANGED_CHECKS=int(env('MAX_UNCHANGED_CHECKS',10)) # maximum ammount of change checks. If reached, means that no more comments will be loaded
TIME_BETWEEN_ACTIONS=int(env('TIME_BETWEEN_ACTIONS',5)) # seconds
SELENIUM_CONTAINER_URL=env('SELENIUM_CONTAINER_URL')
SELENIUM_URL=env('SELENIUM_URL')
DOCCANO_URL=env('DOCCANO_URL')
COMMENTS_MARGIN=float(env('COMMENTS_MARGIN',0.5)) # margin of the number of comments to accept as done