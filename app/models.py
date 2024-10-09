from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(DateTime, nullable=False, default=lambda: datetime.utcnow())
    updated_at = db.Column(DateTime, nullable=False, default=lambda: datetime.utcnow())

    # Relationship with HeroPower
    powers = db.relationship('HeroPower', backref='hero', lazy=True)

class Power(db.Model):
    __tablename__ = 'power'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(DateTime, nullable=False, default=lambda: datetime.utcnow())
    updated_at = db.Column(DateTime, nullable=False, default=lambda: datetime.utcnow())

    # Relationship with HeroPower
    heroes = db.relationship('HeroPower', backref='power', lazy=True)

class HeroPower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    hero_id = db.Column(db.Integer, ForeignKey('hero.id'), nullable=False)
    power_id = db.Column(db.Integer, ForeignKey('power.id'), nullable=False)
    created_at = db.Column(DateTime, nullable=False, default=lambda: datetime.utcnow())
    updated_at = db.Column(DateTime, nullable=False, default=lambda: datetime.utcnow())