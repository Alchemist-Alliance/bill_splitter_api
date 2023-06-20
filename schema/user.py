from constant import KEY, NAME, FRIENDS, EVENTS, INVITES

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
            TypeError: If the [Name] of [Event] is Null or different datatype than [String]
            TypeError: If The List of [Friends] is Null or different datatype than [List]
            TypeError: If all the list items of [Friends] are not of [String] datatype
            TypeError: If The List of [invites] is Null or different datatype than [List]
            TypeError: If all the list items of [invites] are not of [String] datatype
            TypeError: If The List of [Events] is Null or different datatype than [List]
            TypeError: If all the list items of [Events] are not of [String] datatype
        """
        
        if key == None:
            raise TypeError("Key should not be Null")
        else:
            self.key = key


        if name == None or not isinstance(name, str):
            raise TypeError("Name should be string and not Null")
        else:
            self.name = name


        if friends == None or not isinstance(friends, list):
            raise TypeError("Friends should be a list and not Null")
        elif not all(isinstance(friend, str) for friend in friends):
            raise TypeError("Each userKey in friends list should be a string")
        else:
            self.friends = friends


        if invites == None or not isinstance(invites, list):
            raise TypeError("invites should be a list and not Null")
        elif not all(isinstance(request, str) for request in invites):
            raise TypeError("Each eventKey in invites list should be a string")
        else:
            self.invites = invites


        if events == None or not isinstance(events, list):
            raise TypeError("Events should be a list and not Null")
        elif not all(isinstance(event, str) for event in events):
            raise TypeError("Each eventKey in events list should be a string")
        else:
            self.events = events



    def to_dict(self) -> dict:
        user_dict = {
            KEY : self.key,
            NAME : self.name,
            FRIENDS : self.friends,
            INVITES : self.invites,
            EVENTS : self.events,
        }
        
        return user_dict