from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Power, Hero, HeroPower

# Create the Flask application
def create_app():
    app = Flask(__name__)
    
    # Configure the database URI and disable modification tracking
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize the SQLAlchemy database
    db.init_app(app)
    
    return app

# Create the Flask app and set up migration
app = create_app()
migrate = Migrate(app, db)

# Enable CORS for all routes
CORS(app)

# Define the home route
@app.route('/')
def home():
    return ''

# Retrieve all heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    
    # Format hero data for JSON response
    hero_data = [
        {"id": hero.id, "name": hero.name, "super_name": hero.super_name}
        for hero in heroes
    ]
    
    return jsonify(hero_data)

# Retrieve a specific hero by ID
@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_hero(hero_id):
    hero = Hero.query.get(hero_id)

    if hero is None:
        return jsonify({"error": "Hero not found"}), 404

    # Retrieve powers associated with the hero
    hero_powers = HeroPower.query.filter_by(hero_id=hero.id).all()

    powers = [
        {
            "id": hero_power.id,
            "strength": hero_power.strength,
            "name": hero_power.power.name,
            "description": hero_power.power.description
        }
        for hero_power in hero_powers
    ]

    # Format hero data for JSON response
    hero_data = {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "powers": powers
    }

    return jsonify(hero_data)

# Retrieve all powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    
    # Format power data for JSON response
    power_data = [
        {"id": power.id, "name": power.name, "description": power.description}
        for power in powers
    ]
    
    return jsonify(power_data)

# Retrieve a specific power by ID
@app.route('/powers/<int:power_id>', methods=['GET'])
def get_power(power_id):
    power = Power.query.get(power_id)

    if power is None:
        return jsonify({"error": "Power not found"}), 404

    # Format power data for JSON response
    power_data = {
        "id": power.id,
        "name": power.name,
        "description": power.description
    }

    return jsonify(power_data)

# Update the description of a specific power
@app.route('/powers/<int:power_id>', methods=['PATCH'])
def update_power(power_id):
    power = Power.query.get(power_id)

    if power is None:
        return jsonify({"error": "Power not found"}), 404

    try:
        data = request.get_json()
        power.description = data.get('description', power.description)

        db.session.commit()

        # Format updated power data for JSON response
        updated_power_data = {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }

        return jsonify(updated_power_data)

    except Exception as e:
        # Handle exceptions during the update
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400

# Create a new hero power association
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    try:
        data = request.json
        strength = data.get('strength')
        power_id = data.get('power_id')
        hero_id = data.get('hero_id')

        # Check if the required fields are present
        if not strength or not power_id or not hero_id:
            raise ValueError('Missing required fields')

        # Check if the given hero and power exist
        hero = Hero.query.get(hero_id)
        power = Power.query.get(power_id)

        if not hero or not power:
            raise ValueError('Hero or Power not found')

        # Create a new HeroPower association
        hero_power = HeroPower(strength=strength, hero=hero, power=power)
        db.session.add(hero_power)
        db.session.commit()

        # Fetch the hero data to include in the response
        hero_data = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": [
                {"id": p.id, "name": p.name, "description": p.description}
                for p in hero.powers
            ],
        }

        return jsonify(hero_data), 201  # 201 Created status code

    except ValueError as e:
        # Handle validation errors
        return jsonify({"errors": [str(e)]}), 400

# Run the application
if __name__ == '__main__':
    app.run(port=5555)