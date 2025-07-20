from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

from auth_routes import auth
from models import db, Player, Inventory, Quest, Clue, EventLog
from combat_engine import CombatEngine

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Secure config from .env
app.secret_key = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize DB and auth routes
db.init_app(app)
app.register_blueprint(auth)

# RUN THIS ONCE TO CREATE TABLES IN NEON - THEN COMMENT OUT
with app.app_context():
    db.create_all()
    print("Tables created successfully on Neon")

@app.route("/combat/start", methods=["POST"])
def start_combat():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    player = Player.query.filter_by(username=session["user"]).first()
    if not player:
        return jsonify({"error": "Player not found"}), 404

    monster = {
        "name": "Goblin",
        "health": 5,
        "attack": 2
    }

    engine = CombatEngine(player.to_dict(), monster)
    result = engine.run_combat_loop()

    player.apply_update(result["player"])
    db.session.commit()

    event = EventLog(player_id=player.id, event_type="combat", message="Started combat with Goblin.")
    db.session.add(event)
    db.session.commit()

    return jsonify(result)

@app.route("/combat/turn", methods=["POST"])
def combat_turn():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    player = Player.query.filter_by(username=session["user"]).first()
    if not player:
        return jsonify({"error": "Player not found"}), 404

    engine = CombatEngine(player.to_dict(), data["enemy"])
    result = engine.resolve_turn()

    player.apply_update(result["player"])
    db.session.commit()

    return jsonify(result)

@app.route("/combat/retreat", methods=["POST"])
def combat_retreat():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    player = Player.query.filter_by(username=session["user"]).first()
    if not player:
        return jsonify({"error": "Player not found"}), 404

    engine = CombatEngine(player.to_dict(), data["enemy"])
    engine.attempt_retreat()
    result = engine.resolve_turn()

    player.apply_update(result["player"])
    db.session.commit()

    return jsonify(result)

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully."})

if __name__ == "__main__":
    if __name__ == "__main__":
        app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

