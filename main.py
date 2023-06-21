from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from backend.user_backend import *
from backend.event_backend import *
from constant import KEY, EVENT_KEY, OWNER, USER

app = Flask(__name__)

# swagger configs
SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name' : "Bill Splitter API"
    }
)
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)

@app.route("/")
def home():
    return "Bill Splitter API!"

@app.route("/create_user", methods=['GET', 'POST'])
def create_user():
    if(not request.data):
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
    if(not request.data):
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
    if(not request.data):
        return jsonify(error="Send Json Data"), 400
    
    try:
        data = request.get_json()
        create_event_in_database(data)
        event_data = {
            EVENT_KEY : data[KEY],
            USER : data[OWNER]
        }
        print(add_event_to_user(event_data))
    
    except TypeError as err:
        return jsonify(error=str(err)), 400
    
    except KeyError as err:
        return jsonify(error=str(err)), 400
    
    return jsonify(success="Event Created!"), 200


@app.route("/send_invite", methods=['GET', 'POST'])
def send_invite():
    if(not request.data):
        return jsonify(error="Send Json Data"), 400
    
    try:
        data = request.get_json()
        flag = send_invite_to_user(data)
    
    except TypeError as err:
        return jsonify(error=str(err)), 400
    
    except KeyError as err:
        return jsonify(error=str(err)), 400
    
    return jsonify(success="User Already has Invitation") if flag == False else jsonify(success="Invitation Sent!"), 200   


if __name__ == '__main__':
    app.run(debug=True)

