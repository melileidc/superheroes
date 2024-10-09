# Importing necessary modules
from models import db, Hero, Power, HeroPower
from random import choice
from app import create_app
from datetime import datetime

# Create the Flask app
app = create_app()

# Use the app context to interact with the database
with app.app_context():
    # Step 1: Check if tables exist, if not, create them
    db.create_all()
    

    # Step 2: Seeding powers
    print("🦸‍♀️ Seeding powers...")
    powers_data = [
        {"name": "Super Strength", "description": "Gives immense physical strength", "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()},
        {"name": "Flight", "description": "Allows the hero to fly", "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()},
        {"name": "Superhuman Senses", "description": "Enhanced senses at a super-human level", "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()},
        {"name": "Elasticity", "description": "Can stretch the body to extreme lengths", "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()}
    ]

    for data in powers_data:
        power = Power(**data)
        db.session.add(power)

    db.session.commit()

    # Step 3: Seeding heroes
    print("🦸‍♀️ Seeding heroes...")
    heroes_data = [
        {"name": "Kamala Khan", "super_name": "Ms. Marvel", "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()},
        {"name": "Doreen Green", "super_name": "Squirrel Girl", "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()},
        {"name": "Gwen Stacy", "super_name": "Spider-Gwen", "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()},
        {"name": "Janet Van Dyne", "super_name": "The Wasp", "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()},
        {"name": "Wanda Maximoff", "super_name": "Scarlet Witch", "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()},
        {"name": "Carol Danvers", "super_name": "Captain Marvel", "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()},
        {"name": "Jean Grey", "super_name": "Dark Phoenix", "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()},
        {"name": "Ororo Munroe", "super_name": "Storm", "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()},
        {"name": "Kitty Pryde", "super_name": "Shadowcat", "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()},
        {"name": "Elektra Natchios", "super_name": "Elektra", "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()}
    ]

    for data in heroes_data:
        hero = Hero(**data)
        db.session.add(hero)

    db.session.commit()

    # Step 4: Adding powers to heroes
    print("🦸‍♀️ Adding powers to heroes...")

    strengths = ["Strong", "Weak", "Average"]
    heroes = Hero.query.all()
    powers = Power.query.all()

    for hero in heroes:
        for _ in range(choice([1, 2, 3])):
            power = choice(powers)
            strength = choice(strengths)
            hero_power = HeroPower(hero_id=hero.id, power_id=power.id, strength=strength, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
            db.session.add(hero_power)

    db.session.commit()

    print("🦸‍♀️ Done seeding!")