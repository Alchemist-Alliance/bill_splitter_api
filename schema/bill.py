from constant import EVENT_KEY, NAME, AMOUNT, DRAWEES, PAYEES, NOTES

class Bill:
    def __init__(self, event_key, name, amount, drawees, payees, user_count, notes) -> None:
        
        """Initialization Function for the Bill Class
        
        Args:
            event_key (String): The Unique Identification Key for the event it is linked to
            name (String): The name of the Bill
            amount (Float): The total expense of the bill
            drawees (List[String]): The List of Users(Index) which are billed
            payees (Dictionary): The Dictionary of Users(Index) which paid the bill and their contribution
            notes (String): Any Specific notes for the bill


        Raises:
            TypeError: If the [Key] Assigned to [Bill] is Null
            TypeError: If the [Event_Key] Assigned to [Bill] is Null
            TypeError: If the [Name] of [Bill] is Null or different datatype than [String]
            TypeError: If the [Amount] of [Bill] is Null or different datatype than [Float]
            TypeError: If The List of [Drawees] is Null or different datatype than [List]
            TypeError: If all the list items of [Drawees] are not of [Integer] datatype and within the range of 0 to [User_Count]
            TypeError: If The List of [Payees] is Null or different datatype than [Dictionary]
            TypeError: If all the keys of [Payees] are not of [Integer] datatype and within the range of 0 to [User_Count]
            TypeError: If the sum of all the [Payees] Values is not equal to the bill [Amount]
            TypeError: If the [User_Count] is Null or different datatype than [Integer] 
        """


        if event_key == None:
            raise TypeError("Event Key should not be Null")
        else:
            self.event_key = event_key


        if not isinstance(name, str):
            raise TypeError("Name should be string and not Null")
        else:
            self.name = name


        if not isinstance(amount, str):
            raise TypeError("Amount should be string and not Null")
        else:
            self.amount = float(amount)
        
        if not isinstance(user_count, int):
            raise TypeError("User_Count should be int and not Null")


        if drawees == None or not isinstance(drawees, list):
            raise TypeError("Drawees should be a list and not Null")
        elif not all((isinstance(drawee, int) and drawee >= 0 and drawee < user_count) for drawee in drawees):
            raise TypeError(f"Each Drawee in Drawees list should be a int and in the range of 0 and {user_count - 1}")
        else:
            self.drawees = drawees


        if payees == None or not isinstance(payees, dict):
            raise TypeError("Payees should be a list and not Null")
        
        total_contribution = 0.0
        for payee, contribution in payees.items():
            if not isinstance(payee, str):
                raise TypeError("Each Payee in Payees list should be a str")
            
            if not isinstance(contribution, str):
                raise TypeError("Each Contribution of Payees should be str")
            
            contribution = float(contribution)
            payee = int(payee)
            
            if payee < 0 and payee >= user_count:
                print(payee)
                raise TypeError(f"Each Payee in Payees list should be in the range of 0 to {user_count - 1}")
            
            total_contribution += contribution
            
        if total_contribution != self.amount:
            raise TypeError(f"The sum of Contributions({total_contribution}) of all Payees should be equal to the Amount({amount}) of the bill")
        else:
            self.payees = {payee:float(contribution) for payee,contribution in payees.items()}
        
            
        if not isinstance(notes,str):
            notes = str(notes)
        self.notes = notes
        
    
    def to_dict(self) -> dict:
        """Converts Object of Bill Class to Dict

        Returns:
            Dict: The Bill data as a Dict
        """
        
        bill_dict = {
            EVENT_KEY : self.event_key,
            NAME: self.name,
            AMOUNT : self.amount,
            DRAWEES : self.drawees,
            PAYEES : self.payees,
            NOTES : self.notes,
        }
        return bill_dict