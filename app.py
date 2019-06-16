import pronunciation
import judge
import play
from flask import Flask, render_template, request, abort, redirect, url_for
import record
from random import randint
app = Flask(__name__)
history = ['Hello']
file_wav = ""


@app.route('/')
def index():
    word = request.args.get('word')
    if word:
        history.append(word)
    score = request.args.get('score', '-1')
    return render_template('index.html', word=history[-1], score=score)


@app.route('/judge/')
def judge_():
    record.save()
    return_list = pronunciation.pronunciation(history[-1])
    global file_wav 
    file_wav = return_list[0]
    s = judge.judge("record.wav", return_list[0])

    return redirect(url_for('index', score=str(int(s))))
    # return str(s)


@app.route('/play/')
def play_wav():
    play.play(file_wav)
    return


@app.route('/review/')
def review():

    return render_template('history.html', words=history[1:])
