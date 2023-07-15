from constant import deta, KEY, EVENT_KEY, NAME, AMOUNT, DRAWEES, PAYEES, NOTES, BILL_BASE, BILL, STATUS, __EXPIRES
from schema.bill import Bill
from schema.event import EventStatus
from backend.redis_backend import *
bills = deta.Base(BILL_BASE)

def validate_new_bill(data,user_count) -> dict:
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
    return bill_dict
        
        
def fetch_bill(bill_key) -> dict:
    """Returns the bill for the provided bill key from database 

    Args:
        bill_key ([String]): Unique Key for the Bill

    Returns:
        dict: Bill Details for the specified bill_key
    """
    
    bill = fetch_from_redis(Entity=BILL, key=bill_key)
    if bill is None:
        bill = bills.get(bill_key)
        add_to_redis(Entity=BILL, data=bill)
    return bill


def check_bill_before_deleting(bill) -> None:
    if bill is None:
        raise TypeError("No Such Bill Exists")
    

def create_new_bill(bill,event) -> dict:
    if event[STATUS] == EventStatus.TEMPORARY.value:
        bill_data = bills.put(bill, expire_at=event[__EXPIRES])
    else:
        bill_data = bills.put(bill)
    add_to_redis(Entity=BILL, data=bill_data)
    return bill_data


def remove_bill(bill) -> None:
    remove_from_redis(Entity=BILL, key=bill[KEY])
    bills.delete(bill[KEY])