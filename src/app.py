from flask import Flask, jsonify, request
import os
import json

app = Flask(__name__)

# Configuration
# SECRET_KEY = "super_secret_key_123"  # This is a secret key, should be moved to environment variables
DATABASE_FILE = "data/db.json"

def load_database():
    if not os.path.exists(DATABASE_FILE):
        return {"users": [], "posts": []}
    with open(DATABASE_FILE, "r") as f:
        return json.load(f)

def save_database(data):
    os.makedirs(os.path.dirname(DATABASE_FILE), exist_ok=True)
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/api/users", methods=["GET"])
def get_users():
    db = load_database()
    return jsonify(db["users"])

@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    db = load_database()
    db["users"].append(data)
    save_database(db)
    return jsonify({"message": "User created successfully"}), 201

@app.route("/api/posts", methods=["GET"])
def get_posts():
    db = load_database()
    return jsonify(db["posts"])

@app.route("/api/posts", methods=["POST"])
def create_post():
    data = request.get_json()
    db = load_database()
    db["posts"].append(data)
    save_database(db)
    return jsonify({"message": "Post created successfully"}), 201

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000) 