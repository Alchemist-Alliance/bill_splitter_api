class UserInfoInEvent:
    def __init__(self, expenses, user_bills) -> None:
        
        """Initialization Function for the User Info Class
        
        Args:
            expenses (Float): The total expense of the user in the event
            user_bills (List[String]): The bill Key of all the bills of user in the event

        Raises:
            TypeError: If the [Expenses] of user is Null or different datatype than [Float]
            TypeError: If The List of [User_Bills] is Null or different datatype than [List]
            TypeError: If all the list items of [User_Bills] are not of [String] datatype
        """


        # if expenses == None or not isinstance(expenses, float):
        #     raise TypeError("expenses should be Float and not Null")
        # else:
        #     self.expenses = expenses


        # if user_bills == None or not isinstance(user_bills, list):
        #     raise TypeError("bills should be a list and not Null")
        # elif not all(isinstance(bill, str) for bill in user_bills):
        #     raise TypeError("Each billKey in user_bills list should be a string")
        # else:
        #     self.user_bills = user_bills