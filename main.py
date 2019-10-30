from nltk.corpus import cmudict
from nltk.corpus import brown
from itertools import combinations, chain
from flask import Flask, render_template, url_for, copy_current_request_context
import nltk
import random
from flask_socketio import SocketIO, emit
from threading import Thread, Event

nltk.download('cmudict')
nltk.download('brown')


d = cmudict.dict()
index = 0
lines = [['RB', 'NNS', 'NN', 'IN', 'DT', 'NN'],
         ['NN', 'NNS', 'RB', 'DT', 'NN'],
         ['IN', 'NN', 'DT', 'NN', 'TO', 'VB'],
         ['CD', 'NN', 'NN', 'VBZ', 'RP', 'TO', 'VB']
         ]

def get_line(syl, rhyming_syls):
    line = ''
    tags = random.choice(lines)
    syl_set = get_syl_set(syl, len(tags), rhyming_syls)
    for i in range(len(tags)):
        try:
            word = get_word(tags[i], syl_set[i][0])
            line += (word.lower() + ' ')

        except KeyError:
            print('fuck')
            continue
    return line + '<br/>'

def get_rhyming_scheme():
    schemeKlon = [1,2,2,1,2,3,1,3]
    global index
    if index >= len(schemeKlon):
        index = 0
    index += 1
    return schemeKlon[index-1]

def check_syl_set(syls, rhyming_syls):
    res = True
    i = 0
    for rhyming in rhyming_syls:
        total = 0
        for syl in syls:
            total += syl
            if total > rhyming:
                res = False
                break
            elif total == rhyming:
                break
    return res

def tag_rhymes(syls, rhyming_syls):
    resArr = [[a, 0] for a in syls]
    for rhyming in rhyming_syls:
        total = 0
        for syl in resArr:
            total += syl[0]
            if total == rhyming:
                syl[1] = get_rhyming_scheme()
                break
    return resArr

def get_syl_set(max, length, rhyming_syls):
    res = []
    if max == length:
        return tag_rhymes([1]*length, rhyming_syls)
    for ans in sum_to_n(max):
        if len(ans) == length and check_syl_set(ans, rhyming_syls):
                print(ans)
                res.append(ans)
    return tag_rhymes(random.choice(res), rhyming_syls)

def sum_to_n(n):
    from operator import sub
    b, mid, e = [0], list(range(1, n)), [n]
    splits = (d for i in range(n) for d in combinations(mid, i))
    return (list(map(sub, chain(s, e), chain(b, s))) for s in splits)

def rhyme(inp, level):
    entries = nltk.corpus.cmudict.entries()
    syllables = [(word, syl) for word, syl in entries if word == inp]
    rhymes = []
    for (word, syllable) in syllables:
        rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
    return set(rhymes)

def doTheyRhyme(word1, word2):
  if word1.find(word2) == len(word1) - len(word2):
      return False
  if word2.find(word1) == len(word2) - len(word1):
      return False

  return word1 in rhyme(word2, 1)

def nsyl(word):
  return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]]

def get_word(tag, syl, rhyme=None):
    raw = tuple({word for word, pos in brown.tagged_words()[:80000] if pos.startswith(tag)})
    res = []
    for word in raw:
        try:
            syls = nsyl(word)
            if syl in syls:
                if rhyme:
                    if doTheyRhyme(word, rhyme):
                        res.append(word)
                else:
                    res.append(word)
        except KeyError:
            continue

    try:
        return random.choice(res)
    except IndexError:
        print(tag, syl, res)
        return 'to'

class RandomThread(Thread):
    def __init__(self):
        self.delay = 1
        super(RandomThread, self).__init__()

    def randomNumberGenerator(self):
        """
        Generate a random number every 1 second and emit to a socketio instance (broadcast)
        Ideally to be run in a separate thread?
        """
        # infinite loop of magical random numbers
        print("Making random numbers")
        while not thread_stop_event.isSet():
            res = get_line(7, [5, 7])
            socketio.emit('newnumber', {'number': res}, namespace='/')
            res = get_line(7, [5, 7])
            socketio.emit('newnumber', {'number': res}, namespace='/')
            res = get_line(7, [5, 7])
            socketio.emit('newnumber', {'number': res}, namespace='/')
            res = get_line(9, [5, 9])
            socketio.emit('newnumber', {'number': res}, namespace='/')
            res = ""
            socketio.emit('newnumber', {'number': res}, namespace='/')
            socketio.emit('newnumber', {'number': "-"*50}, namespace='/')

    def run(self):
        self.randomNumberGenerator()

app = Flask(__name__)
socketio = SocketIO(app)

thread = Thread()
thread_stop_event = Event()
@app.route('/')
def main():
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

