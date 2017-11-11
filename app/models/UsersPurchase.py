from app import db


class UsersPurchase(db.Model):
    __tablename__ = 'users_purchase'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'), nullable=False)

    def __init__(self, user_id, purchase_id):
        self.user_id = user_id
        self.purchase_id = purchase_id

    def __repr__(self):
        return "{} {}".format(self.user_id, self.purchase_id)