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
USER = "user"
BILLS = "bills"
EXPENSES = "expenses"
USER_BILLS = "user_bills"
FRIENDS = "friends"
REQUESTS = "requests"
IS_VERIFIED = "is_verified"
IS_ACTIVE = "is_active"
OWNER = "owner"
INVITES = "invites"
EVENT_KEY = "event_key"
AMOUNT = "amount"
DRAWEES = "drawees"
PAYEES = "payees"
CONTRIBUTIONS = "contributions"
USER_COUNT = "user_count"
NOTES = "notes"
