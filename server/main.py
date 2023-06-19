import os

from flask import Flask, jsonify, request, abort
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
    db.session.add(Streak(length=1))
    db.session.commit()
    db.create_all()


@app.before_request
def authorize():
    if request.method in ['GET', 'OPTIONS'] or request.endpoint == 'login':
        return
    auth_header = request.headers.get('Authorization')
    try:
        assert auth_header.split(' ')[1] == os.environ['MH_API_KEY']
    except:
        abort(401)


@app.post('/api/v1/login')
def login():
    password = request.get_json()
    if password != os.environ['MH_PASSWORD']:
        abort(401)
    return jsonify(os.environ['MH_API_KEY'])

def get_numbers(guessed):
    query = db.select(RandomNumber.number, db.func.count()).where(RandomNumber.guessed == guessed).group_by(
        RandomNumber.number)
    results = db.session.execute(query)
    results = {row[0]: row[1] for row in results}
    return results


@app.get('/v1/random/dice_rolls')
def get_dice_rolls():
    dice_rolls = get_numbers(False)
    return jsonify(dice_rolls)


@app.get('/v1/random/guesses')
def get_random_guesses():
    guesses = get_numbers(True)
    return jsonify(guesses)


@app.post('/v1/random/dice_rolls')
def add_dice_roll():
    roll = request.get_json()
    db.session.add(RandomNumber(number=roll, guessed=False))
    db.session.commit()
    return ''


@app.post('/v1/random/guesses')
def add_random_guess():
    guess = request.get_json()
    db.session.add(RandomNumber(number=guess, guessed=True))
    db.session.commit()
    return ''


@app.get('/v1/random/streak')
def get_streak():
    result = db.session.execute(db.select(Streak.length))
    result = list(result)[0][0]
    return jsonify(result)


@app.post('/v1/random/streak')
def set_streak():
    new_streak = request.get_json()
    db.session.execute(db.update(Streak).values(length=new_streak))
    db.session.commit()
    return ''


@app.get('/v1/monty/stats')
def get_monty_stats():
    query = db.Select(PlayedGame.switched, PlayedGame.won, db.func.count()) \
        .group_by(PlayedGame.switched, PlayedGame.won)
    results = db.session.execute(query)
    results = [r for r in results]

    def filter_results(switched, won):
        num = [r[2] for r in results if r[0] == switched and r[1] == won]
        if len(num) == 0:
            return 0
        return num[0]

    stick_won = filter_results(False, True)
    stick_lost = filter_results(False, False)
    switch_won = filter_results(True, True)
    switch_lost = filter_results(True, False)
    return jsonify({
        'stick_ratio': 0 if stick_won == 0 else stick_won / (stick_won + stick_lost),
        'switch_ratio': 0 if switch_won == 0 else switch_won / (switch_won + switch_lost)
    })


@app.post('/v1/monty/games')
def add_game():
    game = request.get_json()
    db.session.add(PlayedGame(switched=game['switched'], won=game['won']))
    db.session.commit()
    return ''
