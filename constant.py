from deta import Deta
from os import getenv
from dotenv import load_dotenv


try:
    load_dotenv(".env")
except:
    pass

#DETA Configs
DETA_PROJECT_KEY = getenv("DETA_PROJECT_KEY")
deta = Deta(DETA_PROJECT_KEY)

#DETA BASE NAMES
EVENT_BASE = "event_base"
BILL_BASE = "bill_base"
USER_BASE = "user_base"

# IMPORTANT KEYWORDS converted into CONSTANTS
KEY = "key"
NAME = "name"
EVENTS = "events"
USERS = "users"
BILLS = "bills"
EXPENSES = "expenses"
USER_BILLS = "user_bills"
# USERS_INFO_IN_EVENT = "users_info_in_event"
# USERS_INFO = "users_info"
FRIENDS = "friends"
REQUESTS = "requests"
IS_VERIFIED = "is_verified"
IS_ACTIVE = "is_active"
OWNER = "owner"
INVITES = "invites"