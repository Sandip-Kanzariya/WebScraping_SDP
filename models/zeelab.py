from extensions import db  

class Zeelab(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    price = db.Column(db.Float)
    product_link = db.Column(db.String(300))
    image_url = db.Column(db.String(300))
    product_info = db.Column(db.String(300))
