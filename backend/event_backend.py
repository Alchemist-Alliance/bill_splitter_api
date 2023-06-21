from constant import deta, KEY, NAME, USERS, BILLS, OWNER, IS_ACTIVE, EVENT_BASE, EXPENSES, USER_BILLS
from schema.event import Event

def create_event_in_database(data):
    event = Event(
            key = data[KEY],
            name=data[NAME],
            users=data[USERS],
            expenses=data[EXPENSES],
            user_bills=data[USER_BILLS],
            bills=data[BILLS],
            owner=data[OWNER],
            is_active=data[IS_ACTIVE]
        )
    event_dict = event.to_dict()
    events = deta.Base(EVENT_BASE)
    events.put(event_dict)