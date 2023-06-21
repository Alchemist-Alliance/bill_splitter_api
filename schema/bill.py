from constant import KEY, EVENT_KEY, NAME, AMOUNT, DRAWEES, PAYEES, CONTRIBUTIONS, USER_COUNT, NOTES

class Bill:
    def __init__(self, key, event_key, name, amount, drawees, payees, contributions, user_count, notes) -> None:
        
        """Initialization Function for the Bill Class
        
        Args:
            key (String): The Unique Identification Key for an Bill
            event_key (String): The Unique Identification Key for the event it is linked to
            name (String): The name of the Bill
            amount (Float): The total expense of the bill
            drawees (List[String]): The List of Users(Index) which are billed
            payees (List[String]): The List of Users(Index) which paid the bill
            contributions (Lis[String]): The List of Amount Paid by each payee
            user_count (Integer): The total no of users part of the event
            notes (String): Any Specific notes for the bill


        Raises:
            TypeError: If the [Key] Assigned to [Bill] is Null
            TypeError: If the [Event_Key] Assigned to [Bill] is Null
            TypeError: If the [Name] of [Bill] is Null or different datatype than [String]
            TypeError: If the [Amount] of [Bill] is Null or different datatype than [Float]
            TypeError: If The List of [Drawees] is Null or different datatype than [List]
            TypeError: If all the list items of [Drawees] are not of [Integer] datatype and within the range of 0 to [User_Count]
            TypeError: If The List of [Payees] is Null or different datatype than [List]
            TypeError: If all the list items of [Payees] are not of [Integer] datatype and within the range of 0 to [User_Count]
            TypeError: If The List of [Contributions] is Null or different datatype than [List]
            TypeError: If all the length of [Contributions] is not equal to the length of [Payees]
            TypeError: If all the list items of [Contributions] are not of [Float] datatype and greater than 0
            TypeError: If the sum of all the [Contributions] is not equal to the bill [Amount]
            TypeError: If the [User_Count] is Null or different datatype than [Integer] 
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
            raise TypeError("Each Drawee in Drawees list should be a int and in the range of 0 and user_count")
        else:
            self.drawees = drawees


        if payees == None or not isinstance(payees, list):
            raise TypeError("Payees should be a list and not Null")
        elif not all((isinstance(payee, int) or payee < 0 or payee >= user_count) for payee in payees):
            raise TypeError("Each Payee in Payees list should be a int and in the range of 0 and user_count")
        else:
            self.payees = payees
            
        if contributions == None or not isinstance(contributions, list):
            raise TypeError("contribution should be a list and not Null")
        elif len(contributions) != len(payees):
            raise TypeError("The Length of Payees and Contributions should be same")
        elif not all((isinstance(contribution, float) or contribution < 0 ) for contribution in contributions):
            raise TypeError("Each Contribution in Contributions list should be a Float and greater than 0")
        elif sum(contributions) != amount:
            raise TypeError("The sum of Contributions should be equal to the amount of the bill")
        else:
            self.contributions = contributions
        
        if user_count == None or not isinstance(user_count, int):
            raise TypeError("User_Count should be int and not Null")
        else:
            self.user_count = user_count
            
        if not isinstance(notes,str):
            notes = str(notes)
        self.notes = notes
        
    
    def to_dict(self) -> dict:
        bill_dict = {
            KEY : self.key,
            EVENT_KEY : self.event_key,
            NAME: self.name,
            AMOUNT : self.amount,
            DRAWEES : self.drawees,
            PAYEES : self.payees,
            CONTRIBUTIONS : self.contributions,
            USER_COUNT : self.user_count,
            NOTES : self.notes,
        }
        return bill_dict