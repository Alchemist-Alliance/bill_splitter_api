from user_info_in_event import UserInfoInEvent
from constant import EXPENSES, USER_BILLS

class Event:
    def __init__(self, key, name, users, users_info, bills, owner, is_active):
        """Initialization Function for the Event Class

        Args:
            key (String): The Unique Identification Key for an Event
            name (String): The name of the Event
            users (List[String]): The List of Users(Key) which are a part of Event
            user_info_in_event (List[Dynamic]): The List of User Info for all the users in Event
            bills (List[String]): The List of Bills(Key) which collectively create the Event
            owner (String): The User Key of the creator of the group
            is_active (Boolean): The Status of Event whether it is settled or not

        Raises:
            TypeError: If the [Key] Assigned to [Event] is Null
            TypeError: If the [Name] of [Event] is Null or different datatype than [String]
            TypeError: If The List of [Users] is Null or different datatype than [List]
            TypeError: If all the list items of [Users] are not of [String] datatype
            TypeError: If The List of [User_info] is Null or different datatype than [List]
            ValueError: If There occurs a mismatch of the length of [Users] and [Users_Info] [List]
            TypeError: If The List of [Bills] is Null or different datatype than [List]
            TypeError: If all the list items of [Bills] are not of [String] datatype
            TypeError: If the [Owner] of [Event] is Null or different datatype than [String]
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


        if users_info == None or not isinstance(users_info, list):
            raise TypeError("Users should be a list and not Null")
        else:
            users_info_in_event = []
            for user_info in users_info:
                user_info_in_event = UserInfoInEvent(
                    expenses=user_info[EXPENSES],user_bills=user_info[USER_BILLS])
                users_info_in_event.append(user_info_in_event)
            self.users_info_in_event = users_info_in_event


        if len(users) != len(users_info):
            raise ValueError("The Length of Users List and Users_Info List must be Same")


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


        if is_active == None or not isinstance(is_active, bool):
            raise TypeError("is_active should be boolean and not Null")
        else:
            self.is_active = is_active