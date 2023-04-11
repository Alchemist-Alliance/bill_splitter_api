class Bill:
    def __init__(self, key, event_key, name, amount, drawees, payees, user_count) -> None:
        
        if key == None:
            raise TypeError("Key should not be Null")
        else:
            self.key = key


        if name == None or not isinstance(name, str):
            raise TypeError("Name should be string and not Null")
        else:
            self.name = name


        if event_key == None or not isinstance(event_key, str):
            raise TypeError("Event Key should be string and not Null")
        else:
            self.event_key = event_key


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