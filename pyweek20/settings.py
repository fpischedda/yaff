# settings.py
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


BROKER_URL = os.environ.get("BROKER_URL")
TWEET_START_SPEED = 500
TWEET_ELASTICITY = 0.9
GRAVITY = 300
