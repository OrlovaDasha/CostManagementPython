from sqlalchemy.orm import relationship

from app import db


class PurchaseConsist(db.Model):
    __tablename__= 'purchase_consist'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    good_id = db.Column(db.Integer, db.ForeignKey('goods.id'), nullable=False)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    sale = db.Column(db.DECIMAL, nullable=False, default=0)

    def __init__(self, good_id, purchase_id, number):
        self.good_id = good_id
        self.purchase_id = purchase_id
        self.number = number

    def __repr__(self):
        return '{} - Good_id: {} \n Purchase_id: {} \n Number: {}'.format(self.id, self.good_id, self.purchase_id, self.number)