import hashlib
import uuid

# In-memory user store (replace with DB in production)
USER_STORE = {}

def hash_password(password, salt=None):
    if not salt:
        salt = uuid.uuid4().hex
    hash_obj = hashlib.sha256((password + salt).encode())
    return hash_obj.hexdigest(), salt

def register_user(username, password):
    if username in USER_STORE:
        return False, "Username already exists."
    hashed_pw, salt = hash_password(password)
    USER_STORE[username] = {
        "password": hashed_pw,
        "salt": salt
    }
    return True, "User registered successfully."

def login_user(username, password):
    user = USER_STORE.get(username)
    if not user:
        return False, "User not found."

    hashed_input, _ = hash_password(password, user["salt"])
    if hashed_input == user["password"]:
        return True, "Login successful."
    return False, "Incorrect password."
