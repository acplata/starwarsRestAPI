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

@app.route('/favorite/character/<int:id>', methods=['POST'])
def add_character_to_favorite(id):
    data = request.get_json()  
    data_user_id = data.get("user_id", None)

    new_favorite = Favorite(character_id=id, user_id=data_user_id)

    try:
        db.session.add(new_favorite)  
        db.session.commit()
        return jsonify(new_favorite.serialize()), 201

    except Exception as error:
        db.session.rollback()
        return error, 500
    
@app.route('/favorite/character/<int:id>', methods=['DELETE'])
def delete_character_by_id(id):
    character_to_delete = Favorite.query.filter_by(character_id=id)
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

@app.route('/favorite/planet/<int:id>', methods=['POST'])
def add_planet_to_favorite(id):
    data = request.get_json()  
    data_user_id = data.get("user_id", None)

    new_favorite = Favorite(planet_id=id, user_id=data_user_id)

    try:
        db.session.add(new_favorite)  
        db.session.commit()
        return jsonify(new_favorite.serialize()), 201

    except Exception as error:
        db.session.rollback()
        return error, 500
    
@app.route('/favorite/planet/<int:id>', methods=['DELETE'])
def delete_planet_by_id(id):
    planet_to_delete = Favorite.query.filter_by(planet_id=id)
    if not planet_to_delete:
        return jsonify({'error': 'planet not found'}), 404

    try:
        db.session.delete(planet_to_delete)
        db.session.commit()
        return jsonify("planet deleted successfully"), 200
    except Exception as error:
        db.session.rollback()
        return error
    
@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    serialized_vehicles = [vehicle.serialize() for vehicle in vehicles]
    return jsonify(serialized_vehicles)

@app.route('/vehicle/<int:id>', methods=['GET'])
def get_vehicles_by_id(id):
    vehicle = vehicle.query.get(id)
    return jsonify(vehicle.serialize())

@app.route('/favorite/vehicle/<int:id>', methods=['POST'])
def add_vehicle_to_favorite(id):
    data = request.get_json()  
    data_user_id = data.get("user_id", None)

    new_favorite = Favorite(vehicle_id=id, user_id=data_user_id)

    try:
        db.session.add(new_favorite)  
        db.session.commit()
        return jsonify(new_favorite.serialize()), 201

    except Exception as error:
        db.session.rollback()
        return error, 500
    
@app.route('/favorite/vehicle/<int:id>', methods=['DELETE'])
def delete_vehicle_by_id(id):
    vehicle_to_delete = Favorite.query.filter_by(vehicle_id=id)
    if not vehicle_to_delete:
        return jsonify({'error': 'vehicle not found'}), 404

    try:
        db.session.delete(vehicle_to_delete)
        db.session.commit()
        return jsonify("vehicle deleted successfully"), 200
    except Exception as error:
        db.session.rollback()
        return error

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
