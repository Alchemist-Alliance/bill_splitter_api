class Bill:
    def __init__(self, key, event_key, name, amount, drawees, payees, user_count) -> None:
        
        """Initialization Function for the Bill Class
        
        Args:
            key (String): The Unique Identification Key for an Bill
            event_key (String): The Unique Identification Key for the event it is linked to
            name (String): The name of the Bill
            amount (Float): The total expense of the bill
            drawees (List[String]): The List of Users(Index) which are billed
            payees (List[String]): The List of Users(Index) which paid the bill
            user_count (Integer): The total no of users part of the event


        Raises:
            TypeError: If the [Key] Assigned to [Bill] is Null
            TypeError: If the [Event_Key] Assigned to [Bill] is Null
            TypeError: If the [Name] of [Bill] is Null or different datatype than [String]
            TypeError: If the [Amount] of [Bill] is Null or different datatype than [Float]
            TypeError: If The List of [Drawees] is Null or different datatype than [List]
            TypeError: If all the list items of [Drawees] are not of [Integer] datatype and within the range of 0 to [User_Count]
            TypeError: If The List of [Payees] is Null or different datatype than [List]
            TypeError: If all the list items of [Payees] are not of [Integer] datatype and within the range of 0 to [User_Count]
        """
        
        if key == None:
            raise TypeError("Key should not be Null")
        else:
            self.key = key


        if event_key == None:
            raise TypeError("Event Key should not be Null")
        else:
            self.event_key = event_key


        if name == None or not isinstance(name, str):
            raise TypeError("Name should be string and not Null")
        else:
            self.name = name


        if amount == None or not isinstance(amount, float):
            raise TypeError("Amount should be float and not Null")
        else:
            self.amount = amount


        if drawees == None or not isinstance(drawees, list):
            raise TypeError("Drawees should be a list and not Null")
        elif not all((isinstance(drawee, int) or drawee < 0 or drawee >= user_count) for drawee in drawees):
            raise TypeError("Each Drawee in Drawees list should be a int and in the range of user_count")
        else:
            self.drawees = drawees


        if payees == None or not isinstance(payees, list):
            raise TypeError("Payees should be a list and not Null")
        elif not all((isinstance(payee, int) or payee < 0 or payee >= user_count) for payee in payees):
            raise TypeError("Each Payee in Payees list should be a int and in the range of user_count")
        else:
            self.payees = payees