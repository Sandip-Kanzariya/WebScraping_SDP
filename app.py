from flask import Flask, jsonify, redirect, request, url_for
from extensions import jwt
from extensions import db, migrate, cors
from auth.views import auth_blueprint
from api.views import product_blueprint

# Image Store
from werkzeug.utils import secure_filename
import os
# Text Extraction From Image
import pytesseract
from PIL import Image

app = Flask(__name__)

app.config.from_object("config") # Load configurations from config.py file
db.init_app(app) 
migrate.init_app(app, db)
jwt.init_app(app)

app.register_blueprint(blueprint=auth_blueprint)
app.register_blueprint(blueprint=product_blueprint)

# For supporting Cross-Origin Resource Sharing (CORS) so, the frontend can access the API.
cors.init_app(app) 


pytesseract.pytesseract.tesseract_cmd = app.config.get("TESSERACT_CMD")

app.secret_key = app.config.get("FLASK_SECRET_KEY")
app.config["UPLOAD_FOLDER"] = app.config.get("IMAGE_UPLOAD_FOLDER")

# Text Extraction From Image 
@app.route('/uploader', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.form['image']
        f.save(os.path.join(os.path.join(app.config['UPLOAD_FOLDER']), secure_filename(f.filename)))
        return redirect(url_for('medicine_image', filename=f.filename))
    return "No file uploaded."

@app.route("/image-search")
def medicine_image():
    # Take image from user
    imagefile = "static/images/"
    imagefile += request.args.get("filename")
    # Open the image file using Pillow's Image module
    img = Image.open(imagefile)
    # OCR configurations
    myconfig = r'--psm 6 --oem 3'
    # Perform OCR on the image and extract text using pytesseract
    text = pytesseract.image_to_string(img, config=myconfig)
    text = text.replace('\n', ' ')
    text = text[:-1]
    
    # this text need to be given to NLP Model for extracting medicine names...
    
    return jsonify(text)

if __name__ == '__main__':
    app.run(
        host=app.config.get("FLASK_RUN_HOST"),
        port=app.config.get("FLASK_RUN_PORT"),
        debug=app.config.get("FLASK_DEBUG"),
    )