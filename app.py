from flask import Flask, request, jsonify
from functools import wraps

app = Flask(__name__)

# Dummy user registry
users = {
    "admin": "password"
}

# Basic Auth Decorator
def check_auth(username, password):
    return users.get(username) == password

def authenticate():
    return jsonify({"message": "Authentication required."}), 401

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/auth-check', methods=['GET'])
@requires_auth
def protected():
    return jsonify({"message": "You are authenticated!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
