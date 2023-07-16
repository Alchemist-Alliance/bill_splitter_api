from constant import deta, KEY, NAME, USERS, BILLS, OWNER, EVENT_BASE, EXPENSES, STATUS, DEFAULT, CONTRIBUTIONS, SHARED_AMOUNT, AMOUNT, DRAWEES, PAYEES, EVENT
from schema.event import Event, UserStatus, EventStatus
from backend.redis_backend import *
events = deta.Base(EVENT_BASE)

EXPIRE_TIME = 1296000 # 15 Days


def validate_new_event(data) -> dict:
    """Validates Event Data according to the Event Schema

    Args:
        data (Dict): The Event Data to be validated

    Returns:
        Dict: A Dictionary of Event Data after proper validation
    """
    
    event_obj = Event(
            name=data[NAME],
            users=[],
            bills={},
            owner=DEFAULT,
            status=data[STATUS]
        )
    event_dict = event_obj.to_dict()
    return event_dict


def create_new_event(event) -> dict:
    """Creates a New Event in the Database and also caches it on Redis

    Args:
        event (Dict): The Event Data to be stored in Database

    Returns:
        Dict: The Event Data stored in Database (with a key as well if not provided)
    """
    
    if event[STATUS] == EventStatus.TEMPORARY.value:
        event_data = events.put(data=event,expire_in=EXPIRE_TIME)
    else:
        event_data = events.put(data=event)
    add_to_redis(Entity=EVENT, data=event_data)
    return event_data



def update_event(event) -> dict:
    """Updates Event Data in the Database and also cache it on Redis

    Args:
        event (Dict): The Event Data to be updated in Database
        
    Returns:
        Dict: The Event Data stored in Database after update
    """
    
    add_to_redis(Entity=EVENT, data=event)
    return events.put(event, event[KEY])



def fetch_event(event_key) -> dict:
    """Returns the user for the provided user key from database and also cache it on Redis

    Args:
        user_key ([String]): Unique Key for the User
        
    Raises:
        TypeError: If there is no Event in the database for the provided Event Key

    Returns:
        Dict: User Details for the specified user_key
    """
    
    event = fetch_from_redis(Entity=EVENT, key=event_key)
    if event is None:
        event = events.get(event_key)
        if event is None:
            raise TypeError("No Such Event Exists")
        add_to_redis(Entity=EVENT, data=event)
    
    return event


def update_owner_for_event(event, owner) -> None:
    """Update the owner of the Event

    Args:
        event (Dict): The Event to be updated
        owner (Dict): The Owner of the Event

    Raises:
        TypeError: If the Owner is not of datatype String
    """
    
    if not isinstance(owner, str):
        raise TypeError("Owner should be a string")
    
    event[OWNER] = owner


def check_event_before_adding_users(event, user_names) -> None:
    """Check whether the new users can be added to this Event

    Args:
        event (Dict): The Event, users are to be added to 
        user_names (List[String]): Names of the new users to be added to the Event

    Raises:
        TypeError: If the Status of the Event is marked as Inactive
        TypeError: If the Users Names is not of List datatype or Length of Users is 0
    """
    
    if event is None or event[STATUS] == EventStatus.INACTIVE.value:
        raise TypeError("Event is Inactive or does not exist")
    
    if not isinstance(user_names, list) or len(user_names) == 0:
        raise TypeError("user_names must be a list of User Names and not empty")


def add_new_users_to_event(event, user_names) -> None:
    """Adds new users to the Users List of Event

    Args:
        event (Dict): The Event, users are to be added to 
        user_names (List[String]): Names of the new users to be added to the Event

    Raises:
        TypeError: if all the names in User Names are of String Datatype
    """
    
    for user_name in user_names:    
        if not isinstance(user_name, str):
            raise TypeError("each name in user_names should be a string")
        
        event_user = {
            NAME : user_name,
            KEY : str(len(event[USERS])),
            EXPENSES : 0.0,
            BILLS : {},
            STATUS : UserStatus.TEMPORARY.value
        }
        event[USERS].append(event_user)



def check_event_before_inviting(event, user_index) -> None:
    """Check whether the User can be invited to the Event

    Args:
        event (_type_): The Event, User is invited to
        user_index (_type_): The Index at which the User is invited

    Raises:
        TypeError: If The Event does not exist
        TypeError: If the Status of the Event is marked as Inactive
        TypeError: If the Status of the Event is marked as Temporary
        TypeError: If the User Index does not lie in the range of 0 to length of Users List of Event
        TypeError: If the user at the User Index is a permanent user
        TypeError: If another user is already invited to that User Index
    """
    
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
    """Reserve the user index of the Users List of Event for the user

    Args:
        event (Dict): The Event, User is invited to
        user_key (String): The key of the invited User
        user_index (Integer): The index at which the User is invited
    """
    
    event[USERS][user_index][KEY] = user_key



def check_event_before_making_user_permanent(event, user_key, user_index) -> None:
    """Check whether the user can be made permanent in the Event

    Args:
        event (Dict): The Event, User is invited to
        user_key (String): The key of the invited User
        user_index (Integer): The index at which the User is invited

    Raises:
        TypeError: If The Event does not exist
        TypeError: If the Status of the Event is marked as Inactive
        TypeError: If the Status of the Event is marked as Temporary
        TypeError: If the User Index does not lie in the range of 0 to length of Users List of Event
        TypeError: If the User at the User Index is a Permanent User
        TypeError: If the User is not invited at that Index
    """
    
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
    """Mark the User as Permanent at the index in the Users List of Event

    Args:
        event (Dict): The Event, User is invited to
        user_key (String): The key of the invited User
        user_index (Integer): The index at which the User is invited
    """
    
    event[USERS][user_index][KEY] = user_key
    event[USERS][user_index][STATUS] = UserStatus.PERMANENT.value
    


def make_user_uninvited(event, user_index) -> None:
    """Remove the user key from reserved index of Users List of Event

    Args:
        event (Dict): The Event, User is invited to
        user_index (Integer): The index at which the User is invited
    """
    event[USERS][user_index][KEY] = str(user_index)



def check_event_before_creating_bill(event) -> None:
    """Check whether the bill can be created for this Event

    Args:
        event (Dict): The Event, bill is going to be created for

    Raises:
        TypeError: If The Event does not exist
        TypeError: If the Status of the Event is marked as Inactive
    """
    if event is None:
        raise TypeError("No Such Event Exists")
    
    if event[STATUS] == EventStatus.INACTIVE.value:
        raise TypeError("The Event is Inactive")


def add_bill_in_event(event, bill) -> None:
    """Add the Bill to the Event 

    Args:
        event (Dict): The Event, bill is going to be created for
        bill (Dict): The Bill to be added

    Raises:
        TypeError: If all the payee in the Payees List of Bill are not Active Users 
        TypeError: If all the drawee in the Drawees List of Bill are not Active Users 
    """
    
    #! the amount to be shared in between all the drawees
    shared_amount = bill[AMOUNT] / len(bill[DRAWEES])
    
    #! Add the bill to the event with the name, amount and shared_amount of bill to the Bills Dict of the Event
    event[BILLS][bill[KEY]] = {
        NAME : bill[NAME],
        AMOUNT : bill[AMOUNT],
        SHARED_AMOUNT : shared_amount
    }
    
    #! For all the payees:
    #!  1. check whether all the users are active
    #!  2. add the amount they paid to the expenses of users
    #!  3. add the bill key and paid amount to bills dict of users
    for payee in bill[PAYEES]:
        if event[USERS][int(payee)][STATUS] == UserStatus.INACTIVE.value:
            raise TypeError(f"{event[USERS][int(payee)][NAME]} is Inactive and can't be added to a bill")
        
        event[USERS][int(payee)][EXPENSES] += bill[PAYEES][payee]
        event[USERS][int(payee)][BILLS][bill[KEY]] = bill[PAYEES][payee]
    
    #! For all the drawees:
    #!  1. check whether all the users are active
    #!  2. subtract the shared_amount from the expenses of users
    #!  3. add the bill key and 0 to bills dict of users if it is not already added.(Could have been a payee also)
    for drawee in bill[DRAWEES]:
        if event[USERS][drawee][STATUS] == UserStatus.INACTIVE.value:
            raise TypeError(f"{event[USERS][drawee][NAME]} is Inactive and can't be added to a bill")
        
        event[USERS][drawee][EXPENSES] -= shared_amount

        if event[USERS][drawee][BILLS].get(bill[KEY]) == None:
            event[USERS][drawee][BILLS][bill[KEY]] = 0



def check_event_before_removing_bill(event, bill_key) -> None:
    """Check whether the bill can be removed from the Event

    Args:
        event (Dict): The Event, Bill is going to be removed from
        bill (Dict): The key of the Bill going to be removed

    Raises:
        TypeError: If The Event does not exist
        TypeError: If the Status of the Event is marked as Inactive
        TypeError: If the bill is not a part of the Event
    """
    
    
    if event is None:
        raise TypeError("No Such Event Exists")
    
    if event[STATUS] == EventStatus.INACTIVE.value:
        raise TypeError("The Event is Inactive")
    
    for event_bill in event[BILLS].keys():
        if event_bill == bill_key:
            return
        
    raise TypeError("No Such Bill Exists in the Event")



def remove_bill_from_event(event, bill) -> None:
    """Removes the Bill from the Event

    Args:
        event (Dict): The Event, Bill is going to be removed from
        bill (Dict): The Bill to be removed
    """
    
    #! the amount to be shared in between all the drawees
    shared_amount = bill[AMOUNT] / len(bill[DRAWEES])
    
    #! remove the bill from the Bills Dict of the Event
    del event[BILLS][bill[KEY]]
    
    #! For all the payees:
    #!  1. subtract the amount they paid to the expenses of users
    #!  2. remove the bill key from bills dict of users
    for payee in bill[PAYEES]:
        event[USERS][int(payee)][EXPENSES] -= bill[PAYEES][payee]
        del event[USERS][int(payee)][BILLS][bill[KEY]]

    #! For all the drawees:
    #!  1. add the shared_amount from the expenses of users
    #!  2. subtract the bill key from bills dict of users if it has not been removed.(Could have been a payee also)
    for drawee in bill[DRAWEES]:
        event[USERS][drawee][EXPENSES] += shared_amount
        
        if event[USERS][drawee][BILLS].get(bill[KEY]) != None:
            del event[USERS][drawee][BILLS][bill[KEY]]
