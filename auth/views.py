from flask import Blueprint, request, jsonify
from auth.schemas.user import UserCreateSchema, UserSchema
from extensions import db, pwd_context
from marshmallow import ValidationError

from models.users import User

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")

@auth_blueprint.route("/register", methods=["POST"])
def register():
    if not request.is_json:
        return {"message": "Missing JSON in request."}, 400
    
    schema = UserCreateSchema()
    user = schema.load(request.json)

    db.session.add(user)
    db.session.commit()

    schema = UserSchema()

    return {"message": "User created successfully.", "user": schema.dump(user)}, 201


@auth_blueprint.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return {"message": "Missing JSON in request."}, 400
    
    email = request.json.get("email")
    password = request.json.get("password")

    if not email or not password:
        return {"message": "Missing email or password."}, 400
    
    user = User.query.filter_by(email=email).first()

    if not user or not pwd_context.verify(password, user.password):
        return {"message": "Invalid credentials."}, 401

    return {"message": "login"} 

@auth_blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400