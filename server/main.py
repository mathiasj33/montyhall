import random

from flask import Flask, jsonify, request
from flask_cors import CORS

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
    query = db.select(RandomNumber.number, db.func.count()).where(RandomNumber.guessed == False).group_by(
        RandomNumber.number)
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
    query = db.Select(PlayedGame.switched, PlayedGame.won, db.func.count()) \
        .group_by(PlayedGame.switched, PlayedGame.won)
    results = db.session.execute(query)
    results = [r for r in results]
    filter_results = lambda switched, won: [r[2] for r in results if r[0] == switched and r[1] == won][0]
    stick_won = filter_results(False, True)
    stick_lost = filter_results(False, False)
    switch_won = filter_results(True, True)
    switch_lost = filter_results(True, False)
    return jsonify({
        'stick_ratio': stick_won / (stick_won + stick_lost),
        'switch_ratio': switch_won / (switch_won + switch_lost)
    })


@app.post('/monty/games')
def add_game():
    game = request.get_json()
    db.session.add(PlayedGame(switched=game['switched'], won=game['won']))
    db.session.commit()
    return ''
