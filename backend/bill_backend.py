from constant import KEY, EVENT_KEY, NAME, AMOUNT, DRAWEES, PAYEES, NOTES, BILL_BASE,deta, USER_COUNT
from schema.bill import Bill
bills = deta.Base(BILL_BASE)

def create_bill_in_database(data,user_count) -> dict:
    bill_obj = Bill(
            event_key = data[EVENT_KEY],
            name = data[NAME],
            amount = data[AMOUNT],
            drawees = data[DRAWEES],
            payees = data[PAYEES],
            user_count=user_count,
            notes = data[NOTES]
        )
    bill_dict = bill_obj.to_dict()
    bill = bills.put(bill_dict)
    return bill
        
        
def fetch_bill(bill_key) -> dict:
    """Returns the bill for the provided bill key from database 

    Args:
        bill_key ([String]): Unique Key for the Bill

    Returns:
        dict: Bill Details for the specified bill_key
    """
    bill = bills.get(bill_key)
    return bill


def check_bill_before_deleting(bill) -> None:
    if bill is None:
        raise TypeError("No Such Bill Exists")
    


def remove_bill(bill) -> None:
    bills.delete(bill[KEY])