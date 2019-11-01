from nltk.corpus import cmudict
from nltk.corpus import brown
from itertools import combinations, chain
from flask import Flask, render_template, url_for, copy_current_request_context
import nltk
import random
from flask_socketio import SocketIO, emit
from threading import Thread, Event
from poem_line import PoemLine
from poem import Poem

nltk.download('cmudict')
nltk.download('brown')


d = cmudict.dict()


class RandomThread(Thread):
    def __init__(self):
        self.delay = 1
        super(RandomThread, self).__init__()

    def randomNumberGenerator(self):
        while not thread_stop_event.isSet():
            poem = Poem()
            line = poem.get_line(7, [5, 7])
            socketio.emit('newnumber', {'number': line}, namespace='/')
            line = poem.get_line(7, [5, 7])
            socketio.emit('newnumber', {'number': line}, namespace='/')
            line = poem.get_line(7, [5, 7])
            socketio.emit('newnumber', {'number': line}, namespace='/')
            line = poem.get_line(9, [5, 9])
            socketio.emit('newnumber', {'number': line}, namespace='/')
            poem.lines = []
            socketio.emit('newnumber', {'number': "-"*50}, namespace='/')

    def run(self):
        self.randomNumberGenerator()

app = Flask(__name__)
socketio = SocketIO(app)

thread = Thread()
thread_stop_event = Event()
@app.route('/')
def main():
    # poem = Poem()
    # poem.get_line(7, [5,7])
    # poem.get_line(7, [5,7])
    return render_template('index.html')


@socketio.on('connect', namespace='/')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = RandomThread()
        thread.start()

@socketio.on('disconnect', namespace='/')
def test_disconnect():
    print('Client disconnected')

if __name__ == "__main__":
    socketio.run(app)
    # main()

