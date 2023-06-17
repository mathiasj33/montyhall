from server.database import db

class Streak(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    length = db.Column(db.Integer)
