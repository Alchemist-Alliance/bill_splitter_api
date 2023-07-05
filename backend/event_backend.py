from constant import deta, KEY, NAME, USERS, BILLS, OWNER, EVENT_BASE, EXPENSES, STATUS
from schema.event import Event, UserStatus, EventStatus

def create_event_in_database(data) -> None:
    event = Event(
            key = data[KEY],
            name=data[NAME],
            users=data[USERS],
            bills=data[BILLS],
            owner=data[OWNER],
            status=data[STATUS]
        )
    event_dict = event.to_dict()
    events = deta.Base(EVENT_BASE)
    events.put(event_dict)
    

def is_event_active(event_key) -> bool:
    events = deta.Base(EVENT_BASE)
    event = events.get(event_key)
    if event is None:
        return False
    return event[STATUS] == EventStatus.ACTIVE.value


def add_new_user_to_event(event_key, user_name) -> None:
    events = deta.Base(EVENT_BASE)
    event = events.get(event_key)
    
    if event is None or event[STATUS] == EventStatus.INACTIVE.value:
        raise TypeError("Event is Inactive or does not exist")
    
    user = {
        NAME : user_name,
        KEY : str(len(event[USERS])),
        EXPENSES : 0.0,
        BILLS : [],
        STATUS : UserStatus.TEMPORARY.value
    }

    event[USERS].append(user)
    
    events.update({
            USERS:event[USERS]
        },event_key)


def check_event_before_inviting(event_key, user_index) -> None:
    events = deta.Base(EVENT_BASE)
    event = events.get(event_key)
    
    if event is None:
        raise TypeError("No Such Event Exists")
    
    if event[STATUS] == EventStatus.INACTIVE.value:
        raise TypeError("The Event is Inactive")
    elif event[STATUS] == EventStatus.TEMPORARY.value:
        raise TypeError("Temporary Events can't invite users")
    
    if user_index < 0 or user_index >= len(event[USERS]):
        raise TypeError(f"Invalid Invite, index must be in the range of 0 to {len(event[USERS]) - 1}")
    if event[USERS][user_index][STATUS] != UserStatus.TEMPORARY.value:
        raise TypeError("The index provided is not of a temporary user")
    if event[USERS][user_index][KEY] != str(user_index):
        raise TypeError("This index is not free for user invite")


def mark_user_invited(event_key, user_key, user_index) -> None:
    events = deta.Base(EVENT_BASE)
    event = events.get(event_key)
    
    event[USERS][user_index][KEY] = user_key
    events.update({
            USERS:event[USERS]
        },event_key)


def check_event_before_adding(event_key, user_key, user_index) -> None:
    events = deta.Base(EVENT_BASE)
    event = events.get(event_key)
    
    if event[STATUS] == EventStatus.INACTIVE.value:
        raise TypeError("The Event is Inactive")
    elif event[STATUS] == EventStatus.TEMPORARY.value:
        raise TypeError("Temporary Events can't add users")
    
    if user_index < 0 or user_index >= len(event[USERS]):
        raise TypeError(f"Invalid Invite, index must be in the range of 0 to {len(event[USERS]) - 1}")
    if event[USERS][user_index][STATUS] != UserStatus.TEMPORARY.value:
        raise TypeError("The index provided is not of a temporary user")
    if event[USERS][user_index][KEY] != user_key:
        raise TypeError("The user is not invited at this index")


def make_user_permanent(event_key, user_index, user_key) -> None:
    events = deta.Base(EVENT_BASE)
    event = events.get(event_key)
    
    event[USERS][user_index][KEY] = user_key
    event[USERS][user_index][STATUS] = UserStatus.PERMANENT.value
    events.update({
            USERS: event[USERS]
        },event_key) 


def make_user_uninvited(event_key, user_index) -> None:
    events = deta.Base(EVENT_BASE)
    event = events.get(event_key)
    
    event[USERS][user_index][KEY] = str(user_index)
    events.update({
            USERS: event[USERS]
        },event_key)       
    

            
def users_in_event(event_key) -> int:
    events = deta.Base(EVENT_BASE)
    event = events.get(event_key)
    
    return len(event[USERS])