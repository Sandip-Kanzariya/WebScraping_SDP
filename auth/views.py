from functools import wraps
from flask import Blueprint, request, jsonify
from flask import current_app as app
from flask_jwt_extended import create_access_token, create_refresh_token, get_current_user, get_jwt, get_jwt_identity, jwt_required
from auth.decorators import auth_role
from auth.helper import add_token_to_database, is_token_revoked, revoke_token
from auth.schemas.user import UserCreateSchema, UserSchema
from extensions import db, pwd_context, jwt
from marshmallow import ValidationError

from models.users import Role, User, UserRole

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")

@auth_blueprint.route("/register", methods=["POST"])
@jwt_required()
@auth_role("super-admin") # Decorators for the methods
def register():
    if not request.is_json:
        return {"message": "Missing JSON in request."}, 400
    
    schema = UserCreateSchema()
    user = schema.load(request.json)

    db.session.add(user)
    db.session.commit()

    user_id = user.id # Get the user id
    admin_role_id = db.session.query(Role.id).filter_by(slug="admin").scalar() # Get the admin role id

    user_role = UserRole(user_id=user_id, role_id=admin_role_id)
    db.session.add(user_role)
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

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    add_token_to_database(access_token)
    add_token_to_database(refresh_token)
    
    return {"access_token": access_token, "refresh_token": refresh_token}, 200

@auth_blueprint.route("/getrole", methods=["GET"])
@jwt_required()
def get_user_role():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    role_slug = user.roles[0].slug
    return {"role": role_slug}, 200

    
@auth_blueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id) # Generate a new access token from refresh token and add to databse 

    add_token_to_database(access_token)
    return {"access_token": access_token}, 200


@auth_blueprint.route("/revoke_access", methods=["DELETE"])
@jwt_required()
def revoke_access_token():
    jti = get_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)
    return jsonify({"message": "token revoked"}), 200


@auth_blueprint.route("/revoke_refresh", methods=["DELETE"])
@jwt_required(refresh=True)
def revoke_refresh_token():
    jti = get_jwt()["jti"]
    user = get_current_user() # Get the current user from token
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)

    schema = UserSchema() # Serialize the user object

    return {"message": "Refresh token revoked", 'user' : schema.dump(user) }, 200



@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_headers, jwt_payload):
    return is_token_revoked(jwt_payload)

# Get Use from JWT 
@jwt.user_lookup_loader
def user_loader_callback(jwt_headers, jwt_payload):
    identity = jwt_payload[app.config["JWT_IDENTITY_CLAIM"]]
    return User.query.get(identity)

@auth_blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400