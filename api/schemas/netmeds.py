from extensions import ma
from models.netmeds import Netmeds


# This Schema for Returing the netmeds data
class NetmedsSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Netmeds
        load_instance = True # Load the instance of the model : Use for update
        