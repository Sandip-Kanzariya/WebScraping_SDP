from extensions import db  

class Netmeds(db.Model):


    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    price = db.Column(db.Float)
    product_link = db.Column(db.String(200))
    image_url = db.Column(db.String(200))
    