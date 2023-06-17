from flask import Flask, jsonify, request
from flask_cors import CORS
import random
from sqlalchemy import text

from server.database import db

app = Flask(__name__)
# CORS(app, resources={r'/*': {'origins': 'http://localhost:63342'}})
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///montyhall.db'
db.init_app(app)

from models.random_number import RandomNumber
from models.played_game import PlayedGame
from models.streak import Streak

with app.app_context():
    # db.drop_all()
    db.create_all()


@app.get('/random/numbers')
def get_random_numbers():
    query = db.select(RandomNumber.number, db.func.count()).where(RandomNumber.guessed == False).group_by(RandomNumber.number)
    results = db.session.execute(query)
    results = {row[0]: row[1] for row in results}
    return jsonify(results)


@app.post('/random/numbers')
def add_random_number():
    db.session.add(RandomNumber(number=random.randint(1, 10), guessed=False))
    db.session.commit()
    return ''


@app.get('/random/streak')
def get_streak():
    result = db.session.execute(db.select(Streak.length))
    result = list(result)[0][0]
    return jsonify(result)


@app.post('/random/streak')
def set_streak():
    new_streak = request.get_json()
    result = db.session.execute(db.select(Streak.length))
    result = list(result)[0][0]
    print(new_streak)
    if new_streak > result:
        db.session.execute(db.update(Streak).values(length=new_streak))
        db.session.commit()
    return ''


@app.get('/monty/stats')
def get_monty_stats():
    query = 'WITH total_stick AS (SELECT COUNT(*) c FROM played_game g WHERE g.switched = 0),'\
            'total_switch AS (SELECT COUNT(*) c FROM played_game g WHERE g.switched = 1),'\
            'stick_won AS (SELECT COUNT(*) c FROM played_game g WHERE g.switched = 0 AND g.won = 1),'\
            'switch_won AS (SELECT COUNT(*) c FROM played_game g WHERE g.switched = 1 AND g.won = 1)'\
            'SELECT (stick_won.c * 1.0) / total_stick.c AS stick_ratio,' \
                   '(switch_won.c * 1.0) / total_switch.c AS switch_ratio '\
            'FROM stick_won, total_stick, switch_won, total_switch'
    results = db.session.execute(text(query))
    tup = list(results)[0]
    return jsonify({
        'stick_ratio': tup[0],
        'switch_ratio': tup[1]
    })

@app.post('/monty/games')
def add_game():
    game = request.get_json()
    db.session.add(PlayedGame(switched=game['switched'], won=game['won']))
    db.session.commit()
    return ''
