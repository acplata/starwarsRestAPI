from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            
        }

class Character(db.Model):
    __tablename__ = "character"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    height = db.Column(db.Integer, unique=False, nullable=False)
    hair_color = db.Column(db.String(40), unique=False, nullable=False)
    eye_color = db.Column(db.String(40), unique=False, nullable=False)
    gender = db.Column(db.String(40), unique=False, nullable=False)
    birth_year = db.Column(db.Integer, unique=False, nullable=False)

    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"), nullable=True)
    vehicles = db.relationship("Vehicle", backref="favorite")
    favorites = db.relationship("Favorite", backref="character")

    def __repr__(self):

        return f'Character {self.name}'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "birth_year": self.birth_year
        }
    
class Planet(db.Model):
    __tablename__ = "planet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    population = db.Column(db.Integer, unique=True, nullable=False)
    climate = db.Column(db.String(100), unique=False, nullable=False)
    terrain = db.Column(db.String(100), unique=False, nullable=False)

    favorites = db.relationship("Favorite", backref="planet")
    characters = db.relationship("Character", backref="planet")

    def __repr__(self):

        return f'Planet {self.name}'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain
        }
    
class Vehicle(db.Model):
    __tablename__ = "vehicle"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    passengers = db.Column(db.Integer, unique=True, nullable=False)
    model = db.Column(db.String(100), unique=True, nullable=False)
    manufacturer = db.Column(db.String(100), unique=True, nullable=False)
    starship_class = db.Column(db.String(100), unique=True, nullable=False)

    favorites = db.relationship("Favorite", backref="vehicle")
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"), nullable=False)

    def __repr__(self):

        return f'Vehicle {self.name}'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "passengers": self.passengers,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "starship_class" : self.starship_class
        }

class Favorite(db.Model):
    __tablename__ = "favorite"
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"), nullable=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicle.id"), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"), nullable=True)

    def __repr__(self):

        return f'Favorite {self.id}'

    def serialize(self):
        return {
            "id": self.id,
           
        }