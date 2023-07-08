from constant import EXPENSES, KEY, NAME, USERS, BILLS, OWNER, STATUS
from enum import Enum

class UserStatus(Enum):
    INACTIVE = 0
    TEMPORARY = 1
    PERMANENT = 2

class EventStatus(Enum):
    INACTIVE = 0
    TEMPORARY = 1
    PERMANENT = 2

class Event:
    def __init__(self, name, users, bills, owner, status) -> None:
        """Initialization Function for the Event Class

        Args:
            name (String): The name of the Event
            users (List[Dict]): The List of Users(Data) which are a part of Event
            bills (List[String]): The List of Bills(Key) which collectively create the Event
            owner (String): The User Key of the creator of the group
            status (Boolean): The Status of Event whether it is temporary, active or inactive

        Raises:
            TypeError: If the [Name] of [Event] is different datatype than [String]
            TypeError: If The List of [Users] is different datatype than [List]
            TypeError: If all the list items of [Users] are not validated properly
            TypeError: If The List of [Bills] is different datatype than [List]
            TypeError: If all the list items of [Bills] are not of [String] datatype
            TypeError: If the [Owner] of [Event] is different datatype than [String]
            TypeError: If the [status] is different datatype than [Integer] and within the range of 0 to 2
        """


        if not isinstance(name, str):
            raise TypeError("Name should be string")
        else:
            self.name = name


        if not isinstance(users, list):
            raise TypeError("Users should be a list")
        elif not all(validate_user(user) == True for user in users):
            raise TypeError("User Data not Validated Properly")
        else:
            self.users = users


        if not isinstance(bills, list):
            raise TypeError("Bills should be a list")
        elif not all(isinstance(bill, str) for bill in bills):
            raise TypeError("Each billKey in bills list should be a string")
        else:
            self.bills = bills


        if not isinstance(owner, str):
            raise TypeError("Owner should be string")
        else:
            self.owner = owner


        if not isinstance(status, int) or status < 0 or status > len(EventStatus):
            raise TypeError("status should be integer in the range of 0 to 2")
        else:
            self.status = status
            
        
    
    def to_dict(self) -> dict:
        event_dict = {
            NAME: self.name,
            USERS: self.users,
            BILLS: self.bills,
            OWNER: self.owner,
            STATUS : self.status,
        }
        return event_dict
    
    
def validate_user(user) -> bool:
    """Validates the data for each user stored in [Users] List in Event

    Args:
        user (Dictionary): The User Data of user stored in [Users] List in Event

    Raises:
        TypeError: If the [User] is different datatype than dict
        TypeError: If The Key of [User] is different datatype than [String]
        TypeError: If The Name of [User] is different datatype than [String]
        TypeError: If The Expense of [User] is different datatype than [Float]
        TypeError: If The Status of [User] is different datatype than [Integer]
        TypeError: If The Status of [User] should be in the range of 0 to length of [UserStatus] Enum
        TypeError: If The Bills of [User] is different datatype than [List]
        TypeError: If each bill in Bills is different datatype than [String]
        
    Returns:
        bool : True if the User Data of user stored in [Users] List in Event gets validated properly
        
    """
    
    if not isinstance(user, dict):
        raise TypeError("User details must shared in a dict")
    if not isinstance(user.get(KEY), str):
        raise TypeError("User key should be string")
    if not isinstance(user.get(NAME), str):
        raise TypeError("User name should be string")
    if not isinstance(user.get(EXPENSES), float):
        raise TypeError("User expenses should be float")
    if not isinstance(user.get(STATUS), int):
        raise TypeError("User Status should be integer")
    if user.get(STATUS) < 0 or user.get(STATUS) >= len(UserStatus):
        raise TypeError(f"User Status should be in the range of 0 to {len(UserStatus) - 1}")
    if not isinstance(user.get(BILLS), list):
        raise TypeError("User Bills should be a list")
    if not all(isinstance(bill, str) for bill in user.get(BILLS)):
        raise TypeError("Each User Bill in User Bills should be string")
    return True