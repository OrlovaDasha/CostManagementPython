from app import db


class Goods(db.Model):
    __tablename__ = 'goods'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.DECIMAL, nullable=False)

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return '{} - Name: {} \n Price: {}'.format(id, self.name, self.price)