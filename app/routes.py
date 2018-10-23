from flask import render_template
from app import app
from flask import request, jsonify, json
from glob import glob
import random
import library as lib
import numpy as np

app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

ttt = lib.TicTacToe()
ttt.reset()

@app.route('/')
def index():
    ttt.reset()
    return render_template('index.html')

@app.route('/reset')
def reset():
    ttt.reset()
    return jsonify(False)

@app.route('/play', methods=['GET', 'POST'])
def play():
    data=None
    if request.method == "POST":
        data = json.loads(request.get_data())
    move = int(data['move'][-1])
    player = int(data['player'])
    position = lib.MOVES[move]
    ttt.play(position)
    print('Player {} and move {}'.format(player, move))
    print(ttt.board)
    wp = lib.who_win(ttt)
    out = {
        'wp': wp
    }
    return jsonify(out)

@app.route('/score', methods=['GET', 'POST'])
def score():
    stats = lib.getWinningStats(ttt)
    stats = stats * 100 / np.sum(stats)
    out = {
        'stats': list(stats)
    }
    return jsonify(out)
