from constant import KEY, NAME, FRIENDS, EVENTS, INVITES, INDEX

class User:
    def __init__(self, key, name, friends, invites, events) -> None:
        
        """Initialization Function for the User Class
        
        Args:
            key (String): The Unique Identification Key for an Event
            name (String): The name of the Event
            friends (List[String]): The List of Users(Key) which are a friends of the user
            invites (List[String]) : The List of Events(Key) which have sent invited to join
            events (List[Strings]): The List of Events(Key) which the user is a part of

        Raises:
            TypeError: If the [Key] Assigned to [User] is Null
            TypeError: If the [Name] of [Event] is different datatype than [String]
            TypeError: If The List of [Friends] is different datatype than [List]
            TypeError: If all the list items of [Friends] are not of [String] datatype
            TypeError: If The List of [invites] is different datatype than [List]
            TypeError: If all the list items of [Invites] are not validated properly
            TypeError: If The List of [Events] is different datatype than [List]
            TypeError: If all the list items of [Events] are not validated properly
        """
        
        if key == None:
            raise TypeError("Key should not be Null")
        else:
            self.key = key


        if not isinstance(name, str):
            raise TypeError("Name should be string")
        else:
            self.name = name


        if not isinstance(friends, list):
            raise TypeError("Friends should be a list")
        elif not all(isinstance(friend, str) for friend in friends):
            raise TypeError("Each userKey in friends list should be a string")
        else:
            self.friends = friends


        if not isinstance(invites, list):
            raise TypeError("invites should be a list and not Null")
        elif not all(validate_event(invite) == True for invite in invites):
            raise TypeError("Event Data not validated properly")
        else:
            self.invites = invites


        if not isinstance(events, list):
            raise TypeError("Events should be a list and not Null")
        elif not all(validate_event(event) == True for event in events):
            raise TypeError("Event Data not validated properly")
        else:
            self.events = events



    def to_dict(self) -> dict:
        """Converts Object of User Class to Dict

        Returns:
            Dict: The User data as a Dict
        """
        
        user_dict = {
            KEY : self.key,
            NAME : self.name,
            FRIENDS : self.friends,
            INVITES : self.invites,
            EVENTS : self.events,
        }
        return user_dict
    
    
def validate_event(event) -> bool:
    """Validates the data for each event stored in [Events] List in User

    Args:
        event (Dict): The Event Data of event stored in [Events] List in User

    Raises:
        TypeError: If the [Event] is different datatype than dict
        TypeError: If The Key of [User] is different datatype than [String]
        TypeError: If The Index of [User] is different datatype than [String]
        
    Returns:
        Bool: True if the Event data gets validated properly  
    """
    
    if not isinstance(event, dict):
        raise TypeError("Event Details must shared in a dict")
    if not isinstance(event.get(KEY), str):
        raise TypeError("Event key should be string")
    if not isinstance(event.get(INDEX), int):
        raise TypeError("User name should be integer")
    return True