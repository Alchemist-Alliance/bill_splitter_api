from schema.user import User
from constant import USER_BASE, deta, KEY, NAME, FRIENDS, EVENTS, INVITES, INDEX


def create_user_in_database(data) -> None:
    user = User(
        key=data[KEY],
        name=data[NAME],
        friends=data[FRIENDS],
        invites=data[INVITES],
        events=data[EVENTS]
    )
    user_dict = user.to_dict()
    users = deta.Base(USER_BASE)
    users.put(user_dict)
    
    
def get_user_from_database(data) -> dict:
    users = deta.Base(USER_BASE)
    return users.get(data[KEY])


def check_user_before_inviting(user_key, event_key) -> None:
    users = deta.Base(USER_BASE)
    user = users.get(user_key)
    
    if user is None:
        raise TypeError("No Such User Exists")
    
    for event in user[INVITES]:
        if event[KEY] == event_key:
            raise TypeError("User Already Invited to Event")
    
    for event in user[EVENTS]:
        if event[KEY] == event_key:
            raise TypeError("User Already a part of Event")

    

def send_invite_to_user(user_key, event_key, user_index) -> None:
    users = deta.Base(USER_BASE)
    user = users.get(user_key)
    
    event = {
        KEY : event_key,
        INDEX : user_index
    }
    
    user[INVITES].append(event)
    users.update({INVITES : user[INVITES]}, user_key)


def check_user_before_adding(user_key, invite_index) -> dict:
    users = deta.Base(USER_BASE)
    user = users.get(user_key)
    
    if user is None:
        raise TypeError("No Such User Exists")
    
    if invite_index < 0 or invite_index >= len(user[INVITES]):
        raise TypeError("Invalid Invite Index")
    
    event_key = user[INVITES][invite_index][KEY]
    
    for event in user[EVENTS]:
        if event[KEY] == event_key:
            return TypeError("User already added to event")
    
    return user[INVITES][invite_index]


def delete_invite(user_key, invite_index) -> None:
    users = deta.Base(USER_BASE)
    user = users.get(user_key)
    del user[INVITES][invite_index]
    users.update({INVITES : user[INVITES]}, user_key)


def add_event_to_user(user_key, event_key, user_index) -> None:
    users = deta.Base(USER_BASE)
    user = users.get(user_key)
    
    event = {
        KEY: event_key,
        INDEX: user_index
    }
    
    user[EVENTS].append(event)
    users.update({EVENTS : user[EVENTS]}, user_key) 