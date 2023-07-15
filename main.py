from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from backend.user_backend import *
from backend.event_backend import *
from backend.bill_backend import *
from constant import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
     r"/*": {"origins": ["http://localhost:3000", "https://bill-splitter-frontend-alpha.vercel.app"]}})

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
    return jsonify(error="Go to bill splitter app"), 400


@app.route("/create_user", methods=['GET', 'POST'])
def create_user():
    if (not request.data):
        return jsonify(error="Send Json Data"), 400

    try:
        data = request.get_json()
        user = create_user_in_database(data)
        # redisClient.json().set(f"USER-{user[KEY]}", '$', user)
        # redisClient.expire(name=f"USER-{user[KEY]}", time=DEFAULT_TIME)

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
        # print(data[KEY])
        # user = redisClient.json().get(name=f"USER-{data[KEY]}")
        # print(user)
        # if user is None:
        user = fetch_user(data[KEY])

    except TypeError as err:
        return jsonify(error=str(err)), 400

    except KeyError as err:
        return jsonify(error=str(err)), 400

    return jsonify(user_data=user), 200


@app.route("/create_event", methods=['GET', 'POST'])
def create_event():
    if (not request.data):
        return jsonify(error="Send Json Data"), 400

    try:
        data = request.get_json()

        event = validate_new_event(data)
        check_event_before_adding_users(
            event=event, user_names=data[USER_NAMES])
        add_new_users_to_event(event=event, user_names=data[USER_NAMES])
        update_owner_for_event(event=event, owner=data[USER_NAMES][0])

        if data[STATUS] == EventStatus.PERMANENT.value:
            user = fetch_user(user_key=data[OWNER])
            check_user_before_creating_event(user)
            update_owner_for_event(event=event, owner=data[OWNER])
            make_user_permanent(event=event,user_key=user[KEY], user_index=0)
        
        event = create_new_event(event)
        
        if data[STATUS] == EventStatus.PERMANENT.value:
            add_event_to_user(user=user, event_key=event[KEY], user_index=0)
            update_user(user)

    except TypeError as err:
        return jsonify(error=str(err)), 400

    except KeyError as err:
        return jsonify(error=str(err)), 400

    return jsonify(success="Event Created!" ,event=event), 200


@app.route("/get_event", methods=['GET', 'POST'])
def get_event():
    if (not request.data):
        return jsonify(error="Send Json Data"), 400

    try:
        data = request.get_json()
        event = fetch_event(data[KEY])

    except TypeError as err:
        return jsonify(error=str(err)), 400

    except KeyError as err:
        return jsonify(error=str(err)), 400

    return jsonify(event=event), 200


@app.route("/add_new_user", methods=['GET', 'POST'])
def add_new_user():
    if (not request.data):
        return jsonify(error="Send Json Data"), 400

    try:
        data = request.get_json()
        event = fetch_event(event_key=data[EVENT_KEY])
        check_event_before_adding_users(
            event=event, user_names=data[USER_NAMES])
        add_new_users_to_event(event=event, user_names=data[USER_NAMES])
        update_event(event)

    except TypeError as err:
        return jsonify(error=str(err)), 400

    except KeyError as err:
        return jsonify(error=str(err)), 400

    return jsonify(success="User Added!",event=event), 200


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
        mark_user_invited(user_key=user[KEY],event=event, user_index=data[INDEX])
        send_invite_to_user(user=user, event_key=event[KEY], user_index=data[INDEX])

        update_user(user=user)
        update_event(event=event)

    except TypeError as err:
        return jsonify(error=str(err)), 400

    except KeyError as err:
        return jsonify(error=str(err)), 400

    return jsonify(success="Invitation Sent!"), 200


@app.route("/resolve_invite", methods=['GET', 'POST'])
def resolve_invite():
    if (not request.data):
        return jsonify(error="Send Json Data"), 400

    try:
        data = request.get_json()

        user = fetch_user(user_key=data[USER_KEY])
        invite = check_user_before_adding(user=user, invite_index=data[INDEX])
        event = fetch_event(event_key=invite[KEY])
        check_event_before_adding(
            event=event, user_key=user[KEY], user_index=invite[INDEX])

        if data[IS_ACCEPTED] == True:
            add_event_to_user(
                user=user, event_key=event[KEY], user_index=invite[INDEX])
            make_user_permanent(
                event=event, user_key=user[KEY], user_index=invite[INDEX])

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
        bill = validate_new_bill(data=data,user_count=len(event[USERS]))
        check_event_before_creating_bill(event=event, drawees=data[DRAWEES], payees=data[PAYEES])
        bill = create_new_bill(bill)
        add_bill_in_event(event=event, bill=bill)
        update_event(event=event)

    except TypeError as err:
        return jsonify(error=str(err)), 400

    except KeyError as err:
        return jsonify(error=str(err)), 400

    return jsonify(success="Bill Created!", bill=bill), 200



@app.route("/get_bill", methods=['GET', 'POST'])
def get_bill():
    if (not request.data):
        return jsonify(error="Send Json Data"), 400

    try:
        data = request.get_json()
        bill = fetch_bill(data[KEY])

    except TypeError as err:
        return jsonify(error=str(err)), 400

    except KeyError as err:
        return jsonify(error=str(err)), 400

    return jsonify(bill=bill), 200



@app.route("/delete_bill", methods=['GET', 'POST'])
def delete_bill():
    if (not request.data):
        return jsonify(error="Send Json Data"), 400

    try:
        data = request.get_json()
        bill = fetch_bill(bill_key=data[KEY])
        check_bill_before_deleting(bill=bill)
        event = fetch_event(event_key=bill[EVENT_KEY])
        check_event_before_removing_bill(event=event, bill_key=bill[KEY])
        remove_bill_from_event(event=event, bill=bill)
        update_event(event=event)
        remove_bill(bill=bill)

    except TypeError as err:
        return jsonify(error=str(err)), 400

    except KeyError as err:
        return jsonify(error=str(err)), 400

    return jsonify(success="Bill Deleted!"), 200


if __name__ == '__main__':
    app.run(debug=True)
