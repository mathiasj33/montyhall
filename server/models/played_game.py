from server.database import db

class PlayedGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    switched = db.Column(db.Boolean)
    won = db.Column(db.Boolean)
