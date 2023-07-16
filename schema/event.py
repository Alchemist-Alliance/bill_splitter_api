from constant import EXPENSES, KEY, NAME, USERS, BILLS, OWNER, STATUS, SHARED_AMOUNT, AMOUNT
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
            TypeError: If The Dict of [Bills] is different datatype than [Dict]
            TypeError: If all the list items of [Bills] are not validated properly
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


        if not isinstance(bills, dict):
            raise TypeError("Bills should be a Dict")
        elif not all(validate_bill(bill) == True for bill in bills.values()):
            raise TypeError("Each billKey in bills list should be a string")
        else:
            self.bills = bills


        if not isinstance(owner, str):
            raise TypeError("Owner should be string")
        else:
            self.owner = owner


        if not isinstance(status, int) or status < 0 or status >= len(EventStatus):
            raise TypeError(f"status should be integer in the range of 0 to {len(EventStatus) - 1}")
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
        user (Dict): The User Data of user stored in [Users] List in Event

    Raises:
        TypeError: If the [User] is different datatype than dict
        TypeError: If The Key of [User] is different datatype than [String]
        TypeError: If The Name of [User] is different datatype than [String]
        TypeError: If The Expense of [User] is different datatype than [Float]
        TypeError: If The Status of [User] is different datatype than [Integer]
        TypeError: If The Status of [User] should be in the range of 0 to length of [UserStatus] Enum
        TypeError: If The Length of Bills of [User] is not equal to the Length of Contributions of [User]
        TypeError: If The Bills of [User] is different datatype than [List]
        TypeError: If each bill in Bills is different datatype than [String]
        TypeError: If The Contributions of [User] is different datatype than [List]
        TypeError: If each Contribution in Contributions is different datatype than [Float]
        
    Returns:
        Bool : True if the User Data of User stored in [Users] List in Event gets validated properly
        
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
    if not isinstance(user.get(BILLS), dict):
        raise TypeError("User Bills should be a dict")
    if not all(isinstance(bill_keys, str) for bill_keys in user.get(BILLS).keys()):
        raise TypeError("All keys in bills dict must be string")
    if not all(isinstance(bill_values, float) for bill_values in user.get(BILLS).values()):
        raise TypeError("All values in bills dict must be float")
    return True


def validate_bill(bill) -> bool:
    """Validates the data for each bill stored in [Bills] List in Event

    Args:
        bill (Dict): The Bill Data of bill stored in [Bills] List in Event

    Raises:
        TypeError: If the [Bill] is different datatype than dict
        TypeError: If The Name of [Bill] is different datatype than [String]
        TypeError: If The Amount of [Bill] is different datatype than [Float]
        TypeError: If The Shared_Amount of [Bill] is different datatype than [Float]
        
    Returns:
        Bool : True if the Bill Data of Bill stored in [Bills] List in Event gets validated properly
    """
    
    if not isinstance(bill, dict):
        raise TypeError("Bill details must shared in a dict")
    if not isinstance(bill.get(NAME), str):
        raise TypeError("Bill name should be string")
    if not isinstance(bill.get(AMOUNT), float):
        raise TypeError("Amount should be float")
    if not isinstance(bill.get(SHARED_AMOUNT), float):
        raise TypeError("Shared Amount should be float")
    return True