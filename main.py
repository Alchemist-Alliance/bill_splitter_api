from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from backend.user_backend import *
from backend.event_backend import *
from backend.bill_backend import *
from constant import *

app = Flask(__name__)

# swagger configs
SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Bill Splitter API"
    }
)
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)


@app.route("/")
def home():
    return "Bill Splitter API!"


@app.route("/create_user", methods=['GET', 'POST'])
def create_user():
    if (not request.data):
        return jsonify(error="Send Json Data"), 400

    try:
        data = request.get_json()
        create_user_in_database(data)

    except TypeError as err:
        return jsonify(error=str(err)), 400

    except KeyError as err:
        return jsonify(error=str(err)), 400

    return jsonify(success="User Created!"), 200


@app.route("/get_user", methods=['GET', 'POST'])
def get_user():
    if (not request.data):
        return jsonify(error="Send Json Data"), 400

    try:
        data = request.get_json()
        user_data = fetch_user(data[KEY])

    except TypeError as err:
        return jsonify(error=str(err)), 400

    except KeyError as err:
        return jsonify(error=str(err)), 400

    return jsonify(user_data=user_data), 200


@app.route("/create_event", methods=['GET', 'POST'])
def create_event():
    if (not request.data):
        return jsonify(error="Send Json Data"), 400

    try:
        data = request.get_json()
        
        
        if data[STATUS] == EventStatus.PERMANENT.value:
            user = fetch_user(user_key=data[OWNER])
        
        event = create_event_in_database(data)
        add_new_user_to_event(event=event, user_name=data[OWNER_NAME])
        
        if is_event_permanent(event):
            add_event_to_user(user=user, event_key=event[KEY], user_index=0)
            make_user_permanent(event=event,user_key=user[KEY], user_index=0)
            update_user(user)
        
        update_event(event)

    except TypeError as err:
        return jsonify(error=str(err)), 400

    except KeyError as err:
        return jsonify(error=str(err)), 400

    return jsonify(success="Event Created!"), 200


@app.route("/add_new_user", methods=['GET', 'POST'])
def add_new_user():
    if (not request.data):
        return jsonify(error="Send Json Data"), 400
    
    try:
        data = request.get_json()
        event = fetch_event(event_key=data[EVENT_KEY])
        add_new_user_to_event(event=event, user_name=data[NAME])
        update_event(event)
        
    except TypeError as err:
        return jsonify(error=str(err)), 400

    except KeyError as err:
        return jsonify(error=str(err)), 400

    return jsonify(success="User Added!"), 200


@app.route("/send_invite", methods=['GET', 'POST'])
def send_invite():
    if (not request.data):
        return jsonify(error="Send Json Data"), 400

    try:
        data = request.get_json()
        event = fetch_event(data[EVENT_KEY])
        user = fetch_user(data[USER_KEY])
        
        check_event_before_inviting(event=event, user_index=data[INDEX])
        check_user_before_inviting(user=user, event_key=event[KEY])
        mark_user_invited(user_key=user[KEY], event=event, user_index=data[INDEX])
        send_invite_to_user(user=user, event_key=event[KEY], user_index=data[INDEX])
        
        update_user(user=user)
        update_event(event=event)

    except TypeError as err:
        return jsonify(error=str(err)), 400

    except KeyError as err:
        return jsonify(error=str(err)), 400

    return jsonify(success="Invitation Sent!"), 200


@app.route("/resolve_invite", methods=['GET', 'POST'])
def accept_invite():
    if (not request.data):
        return jsonify(error="Send Json Data"), 400

    try:
        data = request.get_json()
        
        user = fetch_user(user_key=data[USER_KEY])
        invite = check_user_before_adding(user=user, invite_index=data[INDEX])
        event = fetch_event(event_key=invite[KEY])
        check_event_before_adding(event=event,user_key=user[KEY],user_index=invite[INDEX])

        if data[IS_ACCEPTED] == True:
            add_event_to_user(user=user, event_key=event[KEY], user_index=invite[INDEX])
            make_user_permanent(event=event,user_key=user[KEY], user_index=invite[INDEX])

        make_user_uninvited(event=event, user_index=invite[INDEX])
        delete_invite(user=user, invite_index=data[INDEX])
        
        update_event(event=event)
        update_user(user=user)

    except TypeError as err:
        return jsonify(error=str(err)), 400

    except KeyError as err:
        return jsonify(error=str(err)), 400
    
    if data[IS_ACCEPTED] == True:
        return jsonify(success="User Added to Event"), 200
    else:
        return jsonify(success="Invitation Rejected"), 200



@app.route("/create_bill", methods=['GET', 'POST'])
def create_bill():
    if (not request.data):
        return jsonify(error="Send Json Data"), 400
    
    try:
        data = request.get_json()
        event = fetch_event(event_key=data[EVENT_KEY])
        bill = create_bill_in_database(data)
        update_drawee_expenses(drawees=bill[DRAWEES],event=event,contribution=bill[AMOUNT]/len(bill[DRAWEES]),  bill_key=bill[KEY])
        update_payee_expenses(payees=bill[PAYEES],event=event, bill_key=bill[KEY])
        add_bill_to_event(event=event, bill_key=bill[KEY])
        update_event(event=event)

    except TypeError as err:
        return jsonify(error=str(err)), 400

    except KeyError as err:
        return jsonify(error=str(err)), 400

    return jsonify(success="Bill Created!"), 200


if __name__ == '__main__':
    app.run(debug=True)
