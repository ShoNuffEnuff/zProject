from flask import Blueprint, request, jsonify
from user_auth import register_user, login_user

auth = Blueprint('auth', __name__)

@auth.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    success, message = register_user(username, password)
    status = 200 if success else 400
    return jsonify({"message": message}), status

@auth.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    success, message = login_user(username, password)
    status = 200 if success else 401
    return jsonify({"message": message}), status
