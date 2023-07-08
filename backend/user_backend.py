from schema.user import User
from constant import USER_BASE, deta, KEY, NAME, FRIENDS, EVENTS, INVITES, INDEX
users = deta.Base(USER_BASE)


def create_user_in_database(data) -> None:
    user_obj = User(
        key=data[KEY],
        name=data[NAME],
        friends=data[FRIENDS],
        invites=data[INVITES],
        events=data[EVENTS]
    )
    user_dict = user_obj.to_dict()
    users = deta.Base(USER_BASE)
    users.put(user_dict)
    
    
def fetch_user(user_key) -> dict:
    """Returns the user for the provided user key from database 

    Args:
        user_key ([String]): Unique Key for the User

    Returns:
        dict: User Details for the specified user_key
    """
    users = deta.Base(USER_BASE)
    user = users.get(user_key)
    return user


def check_user_before_creating_event(user) -> None:
    if user is None:
        raise TypeError("No Such User Exists")


def check_user_before_inviting(user, event_key) -> None:
    if user is None:
        raise TypeError("No Such User Exists")
    
    for event in user[INVITES]:
        if event[KEY] == event_key:
            raise TypeError("User Already Invited to Event")
    
    for event in user[EVENTS]:
        if event[KEY] == event_key:
            raise TypeError("User Already a part of Event")

    

def send_invite_to_user(user, event_key, user_index) -> None:
    event = {
        KEY : event_key,
        INDEX : user_index
    }
    
    user[INVITES].append(event)


def check_user_before_adding(user, invite_index) -> dict:
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
    del user[INVITES][invite_index]


def add_event_to_user(user, event_key, user_index) -> None:
    event = {
        KEY: event_key,
        INDEX: user_index
    }
    user[EVENTS].append(event)

    
def update_user(user):
    users.put(user,user[KEY])