from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from passlib.context import CryptContext
from flask_cors import CORS
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
cors = CORS()
jwt = JWTManager()