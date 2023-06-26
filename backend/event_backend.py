from constant import deta, KEY, NAME, USERS, BILLS, OWNER, USER_STATUSES, EVENT_BASE, EXPENSES, USER_BILLS, EVENT_STATUS
from schema.event import Event, UserStatus, EventStatus

def create_event_in_database(data):
    event = Event(
            key = data[KEY],
            name=data[NAME],
            users=data[USERS],
            expenses=data[EXPENSES],
            user_bills=data[USER_BILLS],
            user_statuses=data[USER_STATUSES],
            bills=data[BILLS],
            owner=data[OWNER],
            event_status=data[EVENT_STATUS]
        )
    event_dict = event.to_dict()
    events = deta.Base(EVENT_BASE)
    events.put(event_dict)
    

def is_event_active(event_key) -> bool:
    events = deta.Base(EVENT_BASE)
    event = events.get(event_key)
    if(event is None):
        return False
    return event[EVENT_STATUS] == EventStatus.ACTIVE.value


def add_user_to_event(event_key) -> None:
    events = deta.Base(EVENT_BASE)
    event = events.get(event_key)

    event[USERS].append("temp")
    event[EXPENSES].append(0.0)
    event[USER_BILLS].append([])
    event[USER_STATUSES].append(UserStatus.TEMPORARY.value)
    
    events.update({
            USERS:event[USERS], 
            EXPENSES: event[EXPENSES], 
            USER_BILLS: event[USER_BILLS], 
            USER_STATUSES: event[USER_STATUSES]
        },event_key)


def update_invited_user(event_key, user_key, user_index) -> None:
    events = deta.Base(EVENT_BASE)
    event = events.get(event_key)
    event[USERS][user_index] = user_key
    events.update({
            USERS:event[USERS]
        },event_key)


def make_user_permanent(event_key, user_key) -> None:
    events = deta.Base(EVENT_BASE)
    event = events.get(event_key)
    
    user_count = len(event[USERS])
    for index in range(0, user_count):
        if event[USERS][index] == user_key and event[USER_STATUSES][index] == UserStatus.TEMPORARY.value:
            event[USER_STATUSES][index] = UserStatus.PERMANENT.value
    events.update({
            USER_STATUSES: event[USER_STATUSES]
        },event_key)        
    

            
def users_in_event(event_key) -> int:
    events = deta.Base(EVENT_BASE)
    event = events.get(event_key)
    
    return len(event[USERS])