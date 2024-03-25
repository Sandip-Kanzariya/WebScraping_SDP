from flask import Blueprint, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from api.resources import netmeds, zeelab, truemeds

product_blueprint = Blueprint("product", __name__, url_prefix="/product")
api = Api(product_blueprint, errors=product_blueprint.errorhandler)

# 
api.add_resource(netmeds.NetmedsList, "/netmeds")


# 
api.add_resource(zeelab.ZeelabList, "/zeelab")


# 
api.add_resource(truemeds.TruemedsList, "/truemeds")

@product_blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400


