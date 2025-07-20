from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    health = db.Column(db.Integer, default=10)
    max_health = db.Column(db.Integer, default=10)
    food = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50))
    poison_turns = db.Column(db.Integer, default=0)
    x = db.Column(db.Integer, default=0)
    y = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "username": self.username,
            "health": self.health,
            "max_health": self.max_health,
            "food": self.food,
            "status": self.status,
            "poison_turns": self.poison_turns,
            "x": self.x,
            "y": self.y,
        }

    def apply_update(self, state):
        self.health = state.get("health", self.health)
        self.food = state.get("food", self.food)
        self.status = state.get("status", self.status)
        self.poison_turns = state.get("poison_turns", self.poison_turns)
        self.x = state.get("x", self.x)
        self.y = state.get("y", self.y)

class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id', ondelete='CASCADE'))
    item_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, default=1)

class Quest(db.Model):
    __tablename__ = 'quests'

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id', ondelete='CASCADE'))
    quest_text = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='active')

class Clue(db.Model):
    __tablename__ = 'clues'

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id', ondelete='CASCADE'))
    clue_text = db.Column(db.Text, nullable=False)

class EventLog(db.Model):
    __tablename__ = 'events_log'

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id', ondelete='CASCADE'))
    event_type = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    occurred_at = db.Column(db.DateTime, default=datetime.utcnow)
