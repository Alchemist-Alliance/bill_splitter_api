from schema.user import User
from constant import USER_BASE, deta, KEY, NAME, FRIENDS, EVENTS, INVITES, USER, EVENT_KEY


def create_user_in_database(data):
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


def add_event_to_user(data) -> bool:
    user_key = data[USER]
    event_key = data[EVENT_KEY]
    users = deta.Base(USER_BASE)
    user = users.get(user_key)
    for event in user[EVENTS]:
        if event == event_key:
            return False
    user[EVENTS].append(event_key)
    users.update({EVENTS : user[EVENTS]}, user_key)
    return True 


def send_invite_to_user(data) -> None:
    user_key = data[USER]
    event_key = data[EVENT_KEY]
    users = deta.Base(USER_BASE)
    user = users.get(user_key)
    for event in user[INVITES]:
        if event == event_key:
            return False
    user[INVITES].append(event_key)
    users.update({INVITES : user[INVITES]}, user_key)
    return True