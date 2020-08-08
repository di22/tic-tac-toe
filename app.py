from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

count = 0
middle = ((0, 1), (1, 0), (1, 2), (2, 1))
opposit = ((0, 0), (0, 2), (1, 1), (2, 0), (2, 2))
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
    global count
    count = count + 1
    if count % 2 == 0:
        session["board"][row][col] = session["sign"] = "X"
    else:
        session["board"][row][col] = session["sign"] = "O"
    find_winner(row, col)
    return redirect(url_for('index'))


def find_winner(row, col):
    global winner
    global loser
    global items_count
    if ((session["board"][row][0] == session["board"][row][1] == session["board"][row][2])
            or (session["board"][0][col] == session["board"][1][col] == session["board"][2][col])):
        winner = True
        return render_template("game.html", game=session["board"], winner=winner, loser=loser)

    if session["board"][0][0] == session["board"][1][1] == session["board"][2][2] is not None \
            or session["board"][2][0] == session["board"][1][1] == session["board"][0][2] is not None:
        winner = True
        return render_template("game.html", game=session["board"], winner=winner, loser=loser)
    items_count = 0
    for i in session["board"]:
        if not None in i:
            items_count = items_count + 1
    if items_count == 3:
        loser = True
        return render_template("game.html", game=session["board"], winner=winner, loser=loser)


@app.route('/reset')
def reset():
    return redirect(url_for('index'))
