from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from werkzeug.exceptions import BadRequest

auth = Blueprint("auth", __name__, url_prefix="/auth/")


"""
POST http://localhost:5000/auth/
Body:
{
	"username": "walter.bates",
	"password": "admin123"
}
"""
@auth.post("/")
def login():
    try:
        req_data = request.get_json(force=True)

        username = req_data['username']
        password = req_data['password']

        if not username:
            return jsonify({"msg": "Missing username"}), 400
        if not password:
            return jsonify({"msg": "Missing password"}), 400

        if(username != 'walter.bates' or password != 'admin123'):
            return jsonify({"msg": "Bad username or password"}), 401
        
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
        
    except (BadRequest, KeyError):
        return jsonify({"msg": "Provide 'username' and 'password' in JSON format in the request body"}), 400