from flask import Flask
from extensions import db, migrate
from auth.views import auth_blueprint
from api.views import product_blueprint

app = Flask(__name__)

app.config.from_object("config")
db.init_app(app) 
migrate.init_app(app, db)
app.register_blueprint(blueprint=auth_blueprint)
app.register_blueprint(blueprint=product_blueprint)

if __name__ == '__main__':
    app.run(
        host=app.config.get("FLASK_RUN_HOST"),
        port=app.config.get("FLASK_RUN_PORT"),
        debug=app.config.get("FLASK_DEBUG"),
    )