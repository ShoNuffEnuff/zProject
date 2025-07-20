from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Player

def register_user(username, password):
    if Player.query.filter_by(username=username).first():
        return False, "Username already exists."

    hashed_pw = generate_password_hash(password)
    new_user = Player(username=username, password=hashed_pw)

    db.session.add(new_user)
    db.session.commit()

    return True, "User registered successfully."

def login_user(username, password):
    user = Player.query.filter_by(username=username).first()
    if not user:
        return False, "User not found."

    if check_password_hash(user.password, password):
        return True, "Login successful."
    return False, "Incorrect password."
