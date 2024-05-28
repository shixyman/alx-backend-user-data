from flask import Flask, jsonify, request
from auth import Auth

AUTH = Auth()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Bienvenue"})

@app.route("/users", methods=["POST"])
def users():
    """
    Register a new user.

    Expects two form data fields: "email" and "password".

    Returns:
        - If the user is successfully registered:
            {
                "email": "<registered email>",
                "message": "user created"
            }
        - If the user already exists:
            {
                "message": "email already registered"
            }
            with a 400 status code
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")