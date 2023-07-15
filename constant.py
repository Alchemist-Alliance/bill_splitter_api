from deta import Deta
from os import getenv
from dotenv import load_dotenv
from redis import Redis


try:
    load_dotenv(".env")
except:
    pass

#DETA Configs
DETA_PROJECT_KEY = getenv("DETA_PROJECT_KEY")
deta = Deta(DETA_PROJECT_KEY)

REDIS_PASSWORD = getenv("REDIS_PASSWORD")
REDIS_HOST = getenv("REDIS_HOST")
REDIS_PORT = getenv("REDIS_PORT")
redisClient = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True
)

#DETA BASE NAMES
EVENT_BASE = "event_base"
BILL_BASE = "bill_base"
USER_BASE = "user_base"

# IMPORTANT KEYWORDS converted into CONSTANTS
KEY = "key"
NAME = "name"
EVENTS = "events"
USERS = "users"
USER = "user"
BILLS = "bills"
EXPENSES = "expenses"
USER_BILLS = "user_bills"
FRIENDS = "friends"
REQUESTS = "requests"
IS_ACCEPTED = "is_accepted"
OWNER = "owner"
INVITES = "invites"
EVENT_KEY = "event_key"
AMOUNT = "amount"
DRAWEES = "drawees"
PAYEES = "payees"
CONTRIBUTIONS = "contributions"
USER_COUNT = "user_count"
NOTES = "notes"
INVITE_INDEX = "invite_index"
STATUS = "status"
INDEX = "index"
TEMP = "temp"
OWNER_NAME = "owner_name"
USER_KEY = "user_key"
USER_NAMES = "user_names"
DEFAULT="default"
SHARED_AMOUNT = "shared_amount"


DEFAULT_TIME = 3600


#TODO 1: split the functionality of fetch data from database, validating it and making changes to minimize DB calls
#TODO 2: properly comment the functions

