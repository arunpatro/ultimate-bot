from flask import render_template
from app import app
from flask import request, jsonify, json
from glob import glob
import random
import library as lib
import numpy as np

app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

ttt = lib.TicTacToe()
mttt = lib.MasterTicTacToe()
ttt.reset()
mttt.reset()

@app.route('/')
def index():
    ttt.reset()
    mttt.reset()
    return render_template('index.html')

@app.route('/ultimate')
def ultimate():
    ttt.reset()
    mttt.reset()
    return render_template('ultimate.html')

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

@app.route('/mplay', methods=['GET', 'POST'])
def mplay():
    data=None
    if request.method == "POST":
        data = json.loads(request.get_data())
    move = int(data['move'][-1])
    game = int(data['game'][-1])
    player = int(data['player'])
    position = lib.MOVES[move]
    mttt.active_sub_board = game
    p = mttt.play(position)
    print('Player {} and move {}'.format(player, move))
    print(mttt.board)
    mttt.render()
    wp = lib.who_win(mttt)
    out = {
        'wp': wp,
        'winblock': 0,
        'game': 0,
        'player': 0,
    }
    if p[0]:
        out['winblock'] = 1
        out['game'] = p[1]
        out['player'] = p[2]
    print out
    return jsonify(out)

# @app.route('/mrandom', methods=['GET', 'POST'])
# def mrandom():
#     data=None
#     if request.method == "POST":
#         data = json.loads(request.get_data())
#     game = int(data['game'][-1])
#     player = int(data['player'])
#     mttt.active_sub_board = game
#     p = mttt.playRandom()
#     print(mttt.board)
#     mttt.render()
#     wp = lib.who_win(mttt)
#     out = {
#         'wp': wp,
#         'block': 0,
#         'game': 0,
#         'player': 0,
#     }
#     if p[0]:
#         out['block'] = 1
#         out['game'] = p[1]
#         out['player'] = p[2]
#     return jsonify(out)

@app.route('/score', methods=['GET', 'POST'])
def score():
    stats = lib.getWinningStats(ttt)
    stats = stats * 100 / np.sum(stats)
    out = {
        'stats': list(stats)
    }
    return jsonify(out)
