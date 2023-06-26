from schema.user import User
from constant import USER_BASE, deta, KEY, NAME, FRIENDS, EVENTS, INVITES


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


def add_event_to_user(user_key,event_key) -> bool:
    users = deta.Base(USER_BASE)
    user = users.get(user_key)
    
    for event in user[EVENTS]:
        if event == event_key:
            return False
    
    user[EVENTS].append(event_key)
    users.update({EVENTS : user[EVENTS]}, user_key)
    return True 


def send_invite_to_user(user_key,event_key) -> bool:
    users = deta.Base(USER_BASE)
    user = users.get(user_key)
    
    for event in user[INVITES]:
        if event == event_key:
            return False
    
    for event in user[EVENTS]:
        if event == event_key:
            return False
    
    user[INVITES].append(event_key)
    users.update({INVITES : user[INVITES]}, user_key)
    return True


def check_invite(user_key, invite_index) -> str:
    users = deta.Base(USER_BASE)
    user = users.get(user_key)
    event_key = user[INVITES][invite_index]
    return event_key


def delete_invite(user_key, event_key) -> str:
    users = deta.Base(USER_BASE)
    user = users.get(user_key)
    user[INVITES].remove(event_key)
    users.update({INVITES : user[INVITES]}, user_key)
    return event_key