from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from backend.user_backend import *
from backend.event_backend import *
from constant import KEY, EVENT_KEY, OWNER, USER_KEY, IS_ACCEPTED, NAME, INDEX, OWNER_NAME

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
        user_data = get_user_from_database(data)

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
        create_event_in_database(data)
        add_new_user_to_event(event_key=data[KEY], user_name=data[OWNER_NAME])
        
        if is_event_active(event_key=data[KEY]):
            add_event_to_user(user_key=data[OWNER], event_key=data[KEY], user_index=0)
            make_user_permanent(event_key=data[KEY],user_key=data[OWNER], user_index=0)

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
        add_new_user_to_event(event_key=data[EVENT_KEY], user_name=data[NAME])
        
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
        check_event_before_inviting(event_key=data[EVENT_KEY], user_index=data[INDEX])
        check_user_before_inviting(user_key=data[USER_KEY], event_key=data[EVENT_KEY])
        mark_user_invited(user_key=data[USER_KEY], event_key=data[EVENT_KEY], user_index=data[INDEX])
        send_invite_to_user(user_key=data[USER_KEY], event_key=data[EVENT_KEY], user_index=data[INDEX])

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

        event = check_user_before_adding(user_key=data[USER_KEY], invite_index=data[INDEX])
        check_event_before_adding(event_key=event[KEY],user_key=data[USER_KEY],user_index=event[INDEX])

        if data[IS_ACCEPTED] == True:
            add_event_to_user(user_key=data[USER_KEY], event_key=event[KEY], user_index=event[INDEX])
            make_user_permanent(event_key=event[KEY],user_key=data[USER_KEY], user_index=event[INDEX])

        make_user_uninvited(event_key=event[KEY], user_index=event[INDEX])
        delete_invite(user_key=data[USER_KEY], invite_index=data[INDEX])

    except TypeError as err:
        return jsonify(error=str(err)), 400

    except KeyError as err:
        return jsonify(error=str(err)), 400
    
    return jsonify(success="User Added to Event"), 200 if data[IS_ACCEPTED] == True else jsonify(success="Invitaion Rejected"), 200


if __name__ == '__main__':
    app.run(debug=True)
