
from extensions import ma
from models.truemeds import Truemeds# This Schema for Returing the truemeds data

class TruemedsSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Truemeds
        load_instance = True # Load the instance of the model : Use for update
        