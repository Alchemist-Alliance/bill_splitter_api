from schema.user import User
from constant import USER_BASE, deta, KEY, IS_VERIFIED, NAME, FRIENDS, EVENTS, REQUESTS, USERS


def create_user_in_database(data):
    user = User(
        key=data[KEY],
        is_verified=data[IS_VERIFIED],
        name=data[NAME],
        friends=data[FRIENDS],
        requests=data[REQUESTS],
        events=data[EVENTS]
    )
    user_dict = user.to_dict()
    users = deta.Base(USER_BASE)
    users.put(user_dict)
    
    
def get_user_from_database(data) -> dict:
    users = deta.Base(USER_BASE)
    return users.get(data[KEY])


def add_event_to_user(data) -> None:
    users = deta.Base(USER_BASE)
    for userKey in data[USERS]:
        user = users.get(userKey)
        user[EVENTS].add(data[KEY])
    
    