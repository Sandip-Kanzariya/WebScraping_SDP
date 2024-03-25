from extensions import ma
from models.zeelab import Zeelab


# This Schema for Returing the zeelab data
class ZeelabSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Zeelab
        load_instance = True # Load the instance of the model : Use for update
        