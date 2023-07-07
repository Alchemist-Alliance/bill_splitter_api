from constant import deta, KEY, NAME, USERS, BILLS, OWNER, EVENT_BASE, EXPENSES, STATUS
from schema.event import Event, UserStatus, EventStatus
events = deta.Base(EVENT_BASE)

def create_event_in_database(data) -> dict:
    """Creates the event for the provided details in the database

    Args:
        data (Dictionary): Contains all the required data for creating event according to the Event schema

    Returns:
        dict: Event Details that were stored in the database
    """
    event_obj = Event(
            name=data[NAME],
            users=data[USERS],
            bills=data[BILLS],
            owner=data[OWNER],
            status=data[STATUS]
        )
    event_dict = event_obj.to_dict()
    events = deta.Base(EVENT_BASE)
    event = events.put(event_dict)
    return event



def fetch_event(event_key) -> dict:
    """Returns the event for the provided event key from database 

    Args:
        event_key ([String]): Unique Key for the Event

    Returns:
        dict: Event Details for the specified event_key
    """
    events = deta.Base(EVENT_BASE)
    event = events.get(event_key)
    return event


def is_event_permanent(event) -> bool:
    if event is None:
        return False
    return event[STATUS] == EventStatus.PERMANENT.value


def add_new_user_to_event(event, user_name) -> None:
    if event is None or event[STATUS] == EventStatus.REMOVED.value:
        raise TypeError("Event is Inactive or does not exist")
    
    user = {
        NAME : user_name,
        KEY : str(len(event[USERS])),
        EXPENSES : 0.0,
        BILLS : [],
        STATUS : UserStatus.TEMPORARY.value
    }
    
    event[USERS].append(user)



def check_event_before_inviting(event, user_index) -> None:
    if event is None:
        raise TypeError("No Such Event Exists")
    
    if event[STATUS] == EventStatus.REMOVED.value:
        raise TypeError("The Event is Inactive")
    elif event[STATUS] == EventStatus.TEMPORARY.value:
        raise TypeError("Temporary Events can't invite users")
    
    if user_index < 0 or user_index >= len(event[USERS]):
        raise TypeError(f"Invalid Invite, index must be in the range of 0 to {len(event[USERS]) - 1}")
    if event[USERS][user_index][STATUS] != UserStatus.TEMPORARY.value:
        raise TypeError("The index provided is not of a temporary user")
    if event[USERS][user_index][KEY] != str(user_index):
        raise TypeError("This index is not free for user invite")


def mark_user_invited(event, user_key, user_index) -> None:
    event[USERS][user_index][KEY] = user_key



def check_event_before_adding(event, user_key, user_index) -> None:
    if event[STATUS] == EventStatus.REMOVED.value:
        raise TypeError("The Event is Inactive")
    elif event[STATUS] == EventStatus.TEMPORARY.value:
        raise TypeError("Temporary Events can't add users")
    
    if user_index < 0 or user_index >= len(event[USERS]):
        raise TypeError(f"Invalid Invite, index must be in the range of 0 to {len(event[USERS]) - 1}")
    if event[USERS][user_index][STATUS] != UserStatus.TEMPORARY.value:
        raise TypeError("The index provided is not of a temporary user")
    if event[USERS][user_index][KEY] != user_key:
        raise TypeError("The user is not invited at this index")


def make_user_permanent(event, user_index, user_key) -> None:
    event[USERS][user_index][KEY] = user_key
    event[USERS][user_index][STATUS] = UserStatus.PERMANENT.value
    


def make_user_uninvited(event, user_index) -> None:
    event[USERS][user_index][KEY] = str(user_index)
    

            
def users_in_event(event_key) -> int:
    events = deta.Base(EVENT_BASE)
    event = events.get(event_key)
    return len(event[USERS])


# def validate_drawees(drawees, event) -> None:
#     for drawee in drawees:
#         if drawee < 0 or drawee >= len(event[USERS]):
#             raise TypeError(f"Drawee Index should be in the range of 0 to {len(event[USERS]) - 1}")


# def validate_payees(payees, event) -> None:
#     for payee in payees:
#         if int(payee) < 0 or int(payee) >= len(event[USERS]):
#             raise TypeError(f"Payee Index should be in the range of 0 to {len(event[USERS]) - 1}")


def update_drawee_expenses(drawees, event, contribution, bill_key) -> None:
    for drawee in drawees:
        event[USERS][drawee][EXPENSES] -= contribution
        if event[USERS][drawee][BILLS] is None:
            event[USERS][drawee][BILLS] = [bill_key]
        else:
            event[USERS][drawee][BILLS].append(bill_key)


def update_payee_expenses(payees, event, bill_key) -> None:
    for payee in payees:
        event[USERS][int(payee)][EXPENSES] += payees[payee]
        if event[USERS][int(payee)][BILLS] is None:
            event[USERS][int(payee)][BILLS] = [bill_key]
        elif event[USERS][int(payee)][BILLS][-1] != bill_key:
            event[USERS][int(payee)][BILLS].append(bill_key)


def add_bill_to_event(event, bill_key) -> None:
    event[BILLS].append(bill_key)



def update_event(event):
    events.put(event, event[KEY])