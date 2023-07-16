from schema.user import User
from constant import USER_BASE, deta, KEY, NAME, FRIENDS, EVENTS, INVITES, INDEX, USER
users = deta.Base(USER_BASE)
from backend.redis_backend import *


def validate_new_user(data) -> dict:
    """Validates User Data according to the User Schema

    Args:
        data (Dict): The User Data to be validated

    Returns:
        Dict: A Dictionary of User Data after proper validation
    """
    
    user_obj = User(
        key=data[KEY],
        name=data[NAME],
        friends=data[FRIENDS],
        invites=data[INVITES],
        events=data[EVENTS]
    )
    user_dict = user_obj.to_dict()
    return user_dict


def create_new_user(user) -> dict:
    """Creates a New User in the Database and also caches it on Redis

    Args:
        user (Dict): The User Data to be stored in Database

    Returns:
        Dict: The User Data stored in Database (with a key as well if not provided)
    """
    
    user_data = users.put(user)
    add_to_redis(Entity=USER, data=user_data)
    return user_data


def update_user(user) -> dict:
    """Updates User Data in the Database and also cache it on Redis

    Args:
        user (Dict): The User Data to be updated in Database
        
    Returns:
        Dict: The User Data stored in Database after update
    """
    
    add_to_redis(Entity=USER, data=user)
    return users.put(user,user[KEY])
    
    
def fetch_user(user_key) -> dict:
    """Returns the user for the provided user key from database and also cache it on Redis

    Args:
        user_key ([String]): Unique Key for the User
        
    Raises:
        TypeError: If there is no User in the database for the provided User Key

    Returns:
        Dict: User Details for the specified user_key
    """
    
    user = fetch_from_redis(Entity=USER, key=user_key)
    if user is None:
        user = users.get(user_key)
        if user is None:
            raise TypeError("No Such User Exists")
        add_to_redis(Entity=USER, data=user)
        
    return user


def check_user_before_creating_event(user) -> None:
    """Check whether the User can create a permanent Event and become it's Owner

    Args:
        user (Dict): The User Data of the Owner of the Event

    Raises:
        TypeError: If there is no User in the database for the provided User Key
    """
    
    if user is None:
        raise TypeError("No Such User Exists")


def check_user_before_inviting(user, event_key) -> None:
    """Checks whether the User can be Invited to the Event as a Permanent member

    Args:
        user (Dict): The Data of the User invited to Event
        event_key (String): The key of the Event user is invited to

    Raises:
        TypeError: If there is no User in the database for the provided User Key
        TypeError: If the User is already invited to the Event
        TypeError: If the User is already a permanent member in the Event
    """
    
    if user is None:
        raise TypeError("No Such User Exists")
    
    for event in user[INVITES]:
        if event[KEY] == event_key:
            raise TypeError("User Already Invited to Event")
    
    for event in user[EVENTS]:
        if event[KEY] == event_key:
            raise TypeError("User Already a part of Event")

    

def send_invite_to_user(user, event_key, user_index) -> None:
    """Add the Event Key and User Index assigned to the User for the Event in the Invites List of User

    Args:
        user (Dict): The Data of the User invited to Event
        event_key (String): The key of the Event user is invited to
        user_index (Integer): The index assigned to the User for the Event
    """
    
    event = {
        KEY : event_key,
        INDEX : user_index
    }
    
    user[INVITES].append(event)


def check_user_before_adding(user, invite_index) -> dict:
    """Checks whether the User can be Added to the Event as a Permanent member

    Args:
        user (Dict): The Data of the User invited to Event
        invite_index (Integer): The index of the Invite from the Invite List to be Resolved 

    Raises:
        TypeError: If there is no User in the database for the provided User Key
        TypeError: If the Invite Index does not lie in the range of 0 to length of User Invites List
        TypeError: If the User is already a permanent member in the Event

    Returns:
        dict: The Event Data stored in the Invite List of User
    """
    
    if user is None:
        raise TypeError("No Such User Exists")
    
    if invite_index < 0 or invite_index >= len(user[INVITES]):
        raise TypeError("Invalid Invite Index")
    
    event_key = user[INVITES][invite_index][KEY]
    
    for event in user[EVENTS]:
        if event[KEY] == event_key:
            return TypeError("User already added to event")
    
    return user[INVITES][invite_index]


def delete_invite(user, invite_index) -> None:
    """Remove the Invite at the provided index from Invite List of User

    Args:
        user (Dict): The Data of the User invited to Event
        invite_index (Integer): The index of the Invite from the Invite List to be Resolved 
    """
    
    del user[INVITES][invite_index]


def add_event_to_user(user, event_key, user_index) -> None:
    """Add the Event Key and User Index assigned to the User for the Event in the Event List of User

    Args:
        user (Dict): The Data of the User invited to Event
        event_key (String): The key of the Event user is invited to
        user_index (Integer): The index assigned to the User for the Event
    """
    
    event = {
        KEY: event_key,
        INDEX: user_index
    }
    user[EVENTS].append(event)
