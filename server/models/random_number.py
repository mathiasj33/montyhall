from server.database import db

class RandomNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    guessed = db.Column(db.Boolean)
