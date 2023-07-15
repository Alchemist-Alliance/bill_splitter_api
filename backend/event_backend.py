from constant import deta, KEY, NAME, USERS, BILLS, OWNER, EVENT_BASE, EXPENSES, STATUS, DEFAULT, CONTRIBUTIONS, SHARED_AMOUNT, AMOUNT, DRAWEES, PAYEES
from schema.event import Event, UserStatus, EventStatus
events = deta.Base(EVENT_BASE)

def validate_new_event(data) -> dict:
    """Creates the event for the provided details in the database

    Args:
        data (Dictionary): Contains all the required data for creating event according to the Event schema

    Returns:
        dict: Event Details that were stored in the database
    """
    
    event_obj = Event(
            name=data[NAME],
            users=[],
            bills=[],
            owner=DEFAULT,
            status=data[STATUS]
        )
    event_dict = event_obj.to_dict()
    return event_dict



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


def update_owner_for_event(event, owner) -> None:
    
    if not isinstance(owner, str):
        raise TypeError("Owner should be a string")
    
    event[OWNER] = owner


def check_event_before_adding_users(event, user_names) -> None:
    if event is None or event[STATUS] == EventStatus.INACTIVE.value:
        raise TypeError("Event is Inactive or does not exist")
    
    if not isinstance(user_names, list) or len(user_names) == 0:
        raise TypeError("user_names must be a list of User Names and not empty")


def add_new_users_to_event(event, user_names) -> None:
    
    for user_name in user_names:    
        if not isinstance(user_name, str):
            raise TypeError("each name in user_names should be a string")
        
        event_user = {
            NAME : user_name,
            KEY : str(len(event[USERS])),
            EXPENSES : 0.0,
            BILLS : [],
            CONTRIBUTIONS : [],
            STATUS : UserStatus.TEMPORARY.value
        }
        event[USERS].append(event_user)



def check_event_before_inviting(event, user_index) -> None:
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


def mark_user_invited(event, user_key, user_index) -> None:
    event[USERS][user_index][KEY] = user_key



def check_event_before_adding(event, user_key, user_index) -> None:
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


def make_user_permanent(event, user_index, user_key) -> None:
    event[USERS][user_index][KEY] = user_key
    event[USERS][user_index][STATUS] = UserStatus.PERMANENT.value
    


def make_user_uninvited(event, user_index) -> None:
    event[USERS][user_index][KEY] = str(user_index)



def check_event_before_creating_bill(event, drawees, payees) -> None:
    if event is None:
        raise TypeError("No Such Event Exists")
    
    if event[STATUS] == EventStatus.INACTIVE.value:
        raise TypeError("The Event is Inactive")
    
    for drawee in drawees:
        if event[USERS][drawee][STATUS] == UserStatus.INACTIVE.value:
            raise TypeError(f"{event[USERS][drawee][NAME]} is Inactive and can't be added to a bill")
        
    for payee in payees:
        if event[USERS][int(payee)][STATUS] == UserStatus.INACTIVE.value:
            raise TypeError(f"{event[USERS][int(payee)][NAME]} is Inactive and can't be added to a bill")



def add_bill_in_event(event, bill) -> None:
    shared_amount = bill[AMOUNT] / len(bill[DRAWEES])
    bill_idx = len(event[BILLS])
    
    event_bill = {
        KEY : bill[KEY],
        NAME : bill[NAME],
        SHARED_AMOUNT : shared_amount
    }
    
    event[BILLS].append(event_bill)
    
    for payee in bill[PAYEES]:
        event[USERS][int(payee)][EXPENSES] += bill[PAYEES][payee]
        
        if event[USERS][int(payee)][BILLS] is None or len(event[USERS][int(payee)][BILLS]) == 0:
            event[USERS][int(payee)][BILLS] = [bill_idx]
            event[USERS][int(payee)][CONTRIBUTIONS] = [bill[PAYEES][payee]]
        
        else:
            event[USERS][int(payee)][BILLS].append(bill_idx)
            event[USERS][int(payee)][CONTRIBUTIONS].append(bill[PAYEES][payee])
    
    
    for drawee in bill[DRAWEES]:
        event[USERS][drawee][EXPENSES] -= shared_amount
        
        if event[USERS][drawee][BILLS] is None or len(event[USERS][drawee][BILLS]) == 0:
            event[USERS][drawee][BILLS] = [bill_idx]
            
        elif event[USERS][int(payee)][BILLS][-1] != bill_idx:
            event[USERS][drawee][BILLS].append(bill_idx)
            

    



def check_event_before_removing_bill(event, bill_key) -> int:
    if event is None:
        raise TypeError("No Such Event Exists")
    
    if event[STATUS] == EventStatus.INACTIVE.value:
        raise TypeError("The Event is Inactive")
    
    for bill_idx, event_bill in enumerate(event[BILLS]):
        if event_bill[KEY] == bill_key:
            return bill_idx
        
    raise TypeError("No Such Bill Exists in the Event")



def remove_bill_from_event(event, bill, bill_idx) -> None:
    shared_amount = bill[AMOUNT] / len(bill[DRAWEES])
    
    del event[BILLS][bill_idx]
    
    for payee in bill[PAYEES]:
        event[USERS][int(payee)][EXPENSES] -= bill[PAYEES][payee]
        
        for user_bill, idx in enumerate(event[USERS][int(payee)][BILLS]):
            if user_bill == bill_idx:
                del event[USERS][int(payee)][BILLS][idx]
                del event[USERS][int(payee)][CONTRIBUTIONS][idx]
                break

    for drawee in bill[DRAWEES]:
        event[USERS][drawee][EXPENSES] += shared_amount

        try:
            event[USERS][drawee].remove(bill_idx)
        except ValueError:
            pass
    


def create_new_event(event) -> dict:
    return events.put(event)

def update_event(event) -> dict:
    return events.put(event, event[KEY])