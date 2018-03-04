from app import db


class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    owner = db.Column(db.Integer, nullable=True)

    def __init__(self, name, category, owner):
        self.name = name
        self.category = category
        self.owner = owner


    def __str__(self):
        return "{} {} {}".format(self.id, self.name, self.category)