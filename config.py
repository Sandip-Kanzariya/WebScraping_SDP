from datetime import timedelta
import os 

from dotenv import load_dotenv

load_dotenv()

FLASK_RUN_HOST = os.environ.get("FLASK_RUN_HOST", "0.0.0.0")
FLASK_RUN_PORT = os.environ.get("FLASK_RUN_PORT", 5000)
FLASK_DEBUG = os.environ.get("FLASK_DEBUG", False)  
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_TOKEN_LOCATION = ["headers"]
JWT_IDENTITY_CLAIM = "user_id" # "sub" is default value
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=10)
IMAGE_UPLOAD_FOLDER = os.environ.get("IMAGE_UPLOAD_FOLDER")
TESSERACT_CMD = os.environ.get("TESSERACT_CMD")
FLASK_SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'fallback-secret-key')