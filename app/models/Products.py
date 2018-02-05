from app import db


class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)

    def __str__(self):
        return "{} {} {}".format(self.id, self.name, self.category)