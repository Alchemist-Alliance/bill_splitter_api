from constant import EVENT_KEY, NAME, AMOUNT, DRAWEES, PAYEES, NOTES, BILL_BASE,deta, USER_COUNT
from schema.bill import Bill

def create_bill_in_database(data) -> dict:
    bill_obj = Bill(
            event_key = data[EVENT_KEY],
            name = data[NAME],
            amount = data[AMOUNT],
            drawees = data[DRAWEES],
            payees = data[PAYEES],
            user_count=data[USER_COUNT],
            notes = data[NOTES]
        )
    bill_dict = bill_obj.to_dict()
    events = deta.Base(BILL_BASE)
    bill = events.put(bill_dict)
    return bill
        