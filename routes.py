from flask import Blueprint, request, jsonify
from movement_engine import MovementEngine
from item import ITEM_REGISTRY
from combat_engine import CombatEngine
from perception_engine import PerceptionEngine

routes = Blueprint('routes', __name__)

# Dummy in-memory map for movement (10x10 grid of unflipped tiles)
MAP_GRID = [[{"flipped": False, "type": "road"} for _ in range(10)] for _ in range(10)]

@routes.route("/move", methods=["POST"])
def move():
    data = request.get_json()
    player = data["player"]
    direction = data["direction"]

    engine = MovementEngine(player["position"], MAP_GRID)
    new_position, tile = engine.move_player(direction)

    player["position"] = new_position
    return jsonify({
        "player": player,
        "tile": tile
    })

@routes.route("/item/use", methods=["POST"])
def use_item():
    data = request.get_json()
    player = data["player"]
    item_id = data["item_id"]

    if item_id not in player.get("inventory", []):
        return jsonify({"message": "Item not found in inventory."}), 400

    item = ITEM_REGISTRY.get(item_id)
    if not item:
        return jsonify({"message": "Invalid item ID."}), 400

    message = item.apply(player)

    if item.type == "consumable":
        player["inventory"].remove(item_id)

    return jsonify({
        "player": player,
        "message": message
    })

@routes.route("/player/nearby", methods=["POST"])
def check_nearby_players():
    data = request.get_json()
    player = data["player"]
    all_players = data["all_players"]

    detected = PerceptionEngine.detect_nearby(player, all_players)

    return jsonify({"detected": detected})
