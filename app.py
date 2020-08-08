from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
import random

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

moves = []
winner = False
loser = False
items_count = 0


@app.route('/')
def index():
    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["sign"] = "X"
    return render_template("game.html", game=session["board"], winner=winner, loser=loser)


@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    moves.append([row, col])

    number = random.randint(1, 100)
    if number % 2 == 0:
        session["board"][row][col] = session["sign"] = "X"
    else:
        session["board"][row][col] = session["sign"] = "O"
    find_winner(row, col)
    return redirect(url_for('index'))


def find_winner(row, col):
    global winner
    global loser

    if ((session["board"][row][0] == session["board"][row][1] == session["board"][row][2])
            or (session["board"][0][col] == session["board"][1][col] == session["board"][2][col])):
        winner = True
        return render_template("game.html", game=session["board"], winner=winner, loser=loser)

    if session["board"][0][0] == session["board"][1][1] == session["board"][2][2] is not None \
            or session["board"][2][0] == session["board"][1][1] == session["board"][0][2] is not None:
        winner = True
        return render_template("game.html", game=session["board"], winner=winner, loser=loser)

    if len(moves) == 9 and winner == False:
        loser = True
        return render_template("game.html", game=session["board"], winner=winner, loser=loser)


@app.route('/reset')
def reset():
    global winner
    global loser
    winner = False
    loser = False
    session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
    return redirect(url_for('index'))


@app.route('/return')
def re():
    indx = len(moves)
    row = moves[indx - 1][0]
    col = moves[indx - 1][1]
    session["board"][row][col] = None
    moves.pop()
    return redirect(url_for('index'))
