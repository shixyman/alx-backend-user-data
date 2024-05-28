from flask import Flask, request, abort, make_response, jsonify
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

@app.route('/sessions', methods=['POST'])
def login():
    """Respond to the POST /sessions route"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not auth.valid_login(email, password):
        abort(401)

    session_id = auth.create_session(email)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)
    return response

@app.route('/sessions', methods=['DELETE'])
def logout():
    """Respond to the DELETE /sessions route"""
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)

    user = auth.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    auth.destroy_session(user.id)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")