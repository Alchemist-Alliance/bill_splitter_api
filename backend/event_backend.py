from constant import deta, KEY, NAME, USERS, USERS_INFO, BILLS, OWNER, IS_ACTIVE, EVENT_BASE
from schema.event import Event

def create_event_in_database(data):
    event = Event(
            key = data[KEY],
            name=data[NAME],
            users=data[USERS],
            users_info=data[USERS_INFO],
            bills=data[BILLS],
            owner=data[OWNER],
            is_active=data[IS_ACTIVE]
        )
    event_dict = event.to_dict()
    events = deta.Base(EVENT_BASE)
    events.put(event_dict)