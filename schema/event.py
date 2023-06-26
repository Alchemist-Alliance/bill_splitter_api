from constant import EXPENSES, USER_BILLS, KEY, NAME, USERS, BILLS, OWNER, USER_STATUSES, EVENT_STATUS
from enum import Enum

class UserStatus(Enum):
    REMOVED = 0
    TEMPORARY = 1
    PERMANENT = 2

class EventStatus(Enum):
    TEMPORARY = 0
    ACTIVE = 1
    INACTIVE = 2

class Event:
    def __init__(self, key, name, users, expenses, user_bills, user_statuses, bills, owner, event_status) -> None:
        """Initialization Function for the Event Class

        Args:
            key (String): The Unique Identification Key for an Event
            name (String): The name of the Event
            users (List[String]): The List of Users(Key) which are a part of Event
            expenses (Float): The total expense of the user in the event
            user_bills (List[String]): The bill Key of all the bills of user in the event
            user_statuses (List[Integer]): The Status of users which are part of event 
            bills (List[String]): The List of Bills(Key) which collectively create the Event
            owner (String): The User Key of the creator of the group
            status (Boolean): The Status of Event whether it is temporary, active or inactive

        Raises:
            TypeError: If the [Key] Assigned to [Event] is Null
            TypeError: If the [Name] of [Event] is Null or different datatype than [String]
            TypeError: If The List of [Users] is Null or different datatype than [List]
            TypeError: If all the list items of [Users] are not of [String] datatype
            TypeError: If The List of [Expenses] is Null or different datatype than [List]
            TypeError: If all the list items of [Expenses] are not of [Float] datatype
            TypeError: If The List of [User_Bills] is Null or different datatype than [List]
            TypeError: If all the list items of [User_Bills] are not of [String] datatype
            TypeError: If The List of [User_Statuses] is Null or different datatype than [List]
            TypeError: If all the list items of [User_Statuses] are not of [Integer] datatype and within the range of 0 to 2
            TypeError: If all the length of [Expenses], [User_Statuses] and [User_Bills] is not equal to length of [Users]
            TypeError: If The List of [Bills] is Null or different datatype than [List]
            TypeError: If all the list items of [Bills] are not of [String] datatype
            TypeError: If the [Owner] of [Event] is Null or different datatype than [String]
            TypeError: If the [event_status] is Null or different datatype than [Integer] and within the range of 0 to 2
        """


        if key == None:
            raise TypeError("Key should not be Null")
        else:
            self.key = key


        if name == None or not isinstance(name, str):
            raise TypeError("Name should be string and not Null")
        else:
            self.name = name


        if users == None or not isinstance(users, list):
            raise TypeError("Users should be a list and not Null")
        elif not all(isinstance(user, str) for user in users):
            raise TypeError("Each userKey in users list should be a string")
        else:
            self.users = users


        if expenses == None or not isinstance(expenses, list):
            raise TypeError("expenses should be list and not Null")
        elif not all(isinstance(expense, float) for expense in expenses):
            raise TypeError("Each Expense in Expenses list should be a float")
        else:
            self.expenses = expenses


        if user_bills == None or not isinstance(user_bills, list):
            raise TypeError("bills should be a list and not Null")
        elif not all(isinstance(user_bill, list) or not all(isinstance(bill, str) for bill in user_bill) for user_bill in user_bills):
            raise TypeError("Each user_bill in user_bills list should be a list of bills which are string")
        else:
            self.user_bills = user_bills
            
            
        if user_statuses == None or not isinstance(user_statuses, list):
            raise TypeError("User_Statuses should be list and not Null")
        elif not all(isinstance(status, float) or status < 0 or status > 2 for status in user_statuses):
            raise TypeError("Each Status in User_Statuses list should be a integer and in the range of 0 to 2")
        else:
            self.user_statuses = user_statuses


        if len(users) != len(expenses) or len(users) != len(user_bills) or len(users) != len(user_statuses):
            raise TypeError("The Length of Users List, Expenses, User_Info and Users_Statuses List must be Same")


        if bills == None or not isinstance(bills, list):
            raise TypeError("Bills should be a list and not Null")
        elif not all(isinstance(bill, str) for bill in bills):
            raise TypeError("Each billKey in bills list should be a string")
        else:
            self.bills = bills


        if owner == None or not isinstance(owner, str):
            raise TypeError("Owner should be string and not Null")
        else:
            self.owner = owner


        if event_status == None or not isinstance(event_status, bool) or event_status < 0 or event_status > 2:
            raise TypeError("is_active should be integer in the range of 0 to 2 and not Null")
        else:
            self.event_status = event_status
            
    
    def to_dict(self) -> dict:
        event_dict = {
            KEY : self.key,
            NAME: self.name,
            USERS: self.users,
            EXPENSES: self.expenses,
            USER_BILLS: self.user_bills,
            USER_STATUSES : self.user_statuses,
            BILLS: self.bills,
            OWNER: self.owner,
            EVENT_STATUS : self.event_status,
        }
        return event_dict