from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from backend.user_backend import *
from backend.event_backend import *

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
        add_event_to_user(data)
    
    except TypeError as err:
        return jsonify(error=str(err)), 400
    
    except KeyError as err:
        return jsonify(error=str(err)), 400
    
    return jsonify(success="Event Created!"), 200
    

if __name__ == '__main__':
    app.run(debug=True)

