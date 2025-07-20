from flask import Flask, request, jsonify, session
from flask_cors import CORS
from combat_engine import CombatEngine
# from monster_registry import MONSTER_REGISTRY
from auth_routes import auth

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.secret_key = "your_super_secret_key_here"  # Replace with a secure key in production

app.register_blueprint(auth)

@app.route("/combat/start", methods=["POST"])
def start_combat():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    player = request.json["player"]
    monster_id = CombatEngine.get_random_monster()
    enemy = MONSTER_REGISTRY[monster_id]
    engine = CombatEngine(player, enemy)
    result = engine.run_combat_loop()
    return jsonify(result)

@app.route("/combat/turn", methods=["POST"])
def combat_turn():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    player = data["player"]
    enemy = data["enemy"]
    engine = CombatEngine(player, enemy)
    result = engine.resolve_turn()
    return jsonify(result)

@app.route("/combat/retreat", methods=["POST"])
def combat_retreat():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    player = data["player"]
    enemy = data["enemy"]
    engine = CombatEngine(player, enemy)
    engine.attempt_retreat()
    result = engine.resolve_turn()
    return jsonify(result)

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully."})

if __name__ == "__main__":
    app.run(debug=True)

