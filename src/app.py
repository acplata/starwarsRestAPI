"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Vehicle, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Welcome to the Starwars app"
    }

    return jsonify(response_body), 200

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    serialized_users = [user.serialize() for user in users]
    return jsonify(serialized_users)

@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    serialized_characters = [character.serialize() for character in characters]
    return jsonify(serialized_characters)

@app.route('/character/<int:id>', methods=['GET'])
def get_characters_by_id(id):
    character = Character.query.get(id)
    return jsonify(character.serialize())

@app.route('favorite/character/<int:id>', methods=['POST'])
def add_character_to_favorite():
    data = request.get_json()  
    data_name = data.get("name", None)
    data_height = data.get("height", None)
    data_hair_color = data.get("hair_color", None)
    data_eye_color = data.get("eye_color", None)
    data_gender = data.get("gender", None)
    data_birth_year = data.get("birth_year", None)
   
    new_character = Character(name=data_name, gender=data_gender,
                              height=data_height, hair_color=data_hair_color, eye_color=data_eye_color, birth_year=data_birth_year)

    try:
        db.session.add(new_character)  
        db.session.commit()
        return jsonify(new_character.serialize()), 201

    except Exception as error:
        db.session.rollback()
        return error, 500
    
@app.route('favorite/character/<int:id>', methods=['DELETE'])
def delete_character_by_id(id):
    character_to_delete = Character.query.get(id)
    if not character_to_delete:
        return jsonify({'error': 'Character not found'}), 404

    try:
        db.session.delete(character_to_delete)
        db.session.commit()
        return jsonify("character deleted successfully"), 200
    except Exception as error:
        db.session.rollback()
        return error
    
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    serialized_planets = [planet.serialize() for planet in planets]
    return jsonify(serialized_planets)

@app.route('/planet/<int:id>', methods=['GET'])
def get_planets_by_id(id):
    planet = planet.query.get(id)
    return jsonify(planet.serialize())

@app.route('/planet', methods=['POST'])
def create_planet():
    data = request.get_json()  
    data_name = data.get("name", None)
    data_population = data.get("population", None)
    data_climate = data.get("climate", None)
    data_terrain = data.get("terrain", None)
   
    new_planet = Planet(name=data_name, population=data_population,
                              climate=data_climate, terrain=data_terrain)
    
@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    serialized_vehicles = [vehicle.serialize() for vehicle in vehicles]
    return jsonify(serialized_vehicles)

@app.route('/vehicle/<int:id>', methods=['GET'])
def get_vehicles_by_id(id):
    vehicle = vehicle.query.get(id)
    return jsonify(vehicle.serialize())

@app.route('/vehicle', methods=['POST'])
def create_vehicle():
    data = request.get_json()  
    data_name = data.get("name", None)
    data_passengers = data.get("population", None)
    data_model = data.get("model", None)
    data_manufacturer = data.get("manufacturer", None)
    data_starship_class = data.get("starship_class", None)
   
    new_vehicle = Vehicle(name=data_name, model=data_model, passengers=data_passengers,
                              manufacturer=data_manufacturer, starship_class=data_starship_class)

    try:
        db.session.add(new_vehicle)  
        db.session.commit()
        return jsonify(new_vehicle.serialize()), 201

    except Exception as error:
        db.session.rollback()
        return error, 500
    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
