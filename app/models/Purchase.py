from app import db


class Purchase(db.Model):
    __tablename__ = 'purchase'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    purchase_date = db.Column(db.TIMESTAMP, nullable=False)
    shop = db.Column(db.String, nullable=False)
    price = db.Column(db.DECIMAL, nullable=False)
    payment_type = db.Column(db.VARCHAR(4), nullable=False, default='cash')

    def __init__(self, date, shop, price, payment_type):
        self.purchase_date = date
        self.shop = shop
        self.price = price
        self.payment_type = payment_type

    def __repr__(self):
        return '{} - Date: {} \n Shop : {} \n Price: {} \n Type {}'.format(self.id, self.purchase_date, self.shop,
                                                                           self.price, self.payment_type)