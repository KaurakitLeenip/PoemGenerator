from nltk.corpus import cmudict
from nltk.corpus import brown
from itertools import combinations, chain
from flask import Flask, render_template, url_for, copy_current_request_context
import nltk
import random
from flask_socketio import SocketIO, emit
from threading import Thread, Event
from poem_line import PoemLine
from poem_word import Poem_Word

class Poem:
    index = 0
    tag_set = [['RB', 'NNS', 'NN', 'IN', 'DT', 'NN'],
               ['NN', 'NNS', 'RB', 'DT', 'NN'],
               ['IN', 'NN', 'DT', 'NN', 'TO', 'VB'],
               ['CD', 'NN', 'NN', 'VBZ', 'RP', 'TO', 'VB']
               ]
    lines = []

    def clear(self):
        self.lines = []
        self.index = 0

    #check if the poem currently has a word with a specified rhyming tag
    def check_rhyme_tags(self, rhyme_tag):
        for line in self.lines:
            for word in line.line:
                if word.rhyme_tag == rhyme_tag:
                    return word

    def populate(self):
        line = self.get_line(7, [5, 7])
        line = self.get_line(7, [5, 7])
        line = self.get_line(7, [5, 7])
        line = self.get_line(9, [5, 9])
        return line

    def get_line(self, syl, rhyming_syls):
        line = PoemLine()
        line.line = []
        line.rhyme_words = []
        tags = random.choice(self.tag_set)
        line.rhyme_scheme = self.get_syl_set(syl, len(tags), rhyming_syls)
        for i in range(len(tags)):
            word = Poem_Word()
            #if the word is tagged as a rhyming word
            #and if the poem has an existing word that is tagged as such
            scheme = line.rhyme_scheme[i][1]
            if scheme > 0 and self.check_rhyme_tags(scheme):
                word.get_word(tags[i], line.rhyme_scheme[i][0], self.check_rhyme_tags(scheme))
                line.line.append(word)
            # just add it normally
            else:
                word.get_word(tags[i], line.rhyme_scheme[i][0])
                line.line.append(word)

        line.set_rhyme_tags()
        self.lines.append(line)
        return line.to_string()

    def get_rhyming_scheme(self):
        schemeKlon = [1, 2, 2, 1, 2, 3, 1, 3]
        if self.index >= len(schemeKlon):
            index = 0
        self.index += 1
        return schemeKlon[self.index - 1]

    def check_syl_set(self, syls, rhyming_syls):
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

    def tag_rhymes(self, syls, rhyming_syls):
        resArr = [[a, 0] for a in syls]
        for rhyming in rhyming_syls:
            total = 0
            for syl in resArr:
                total += syl[0]
                if total == rhyming:
                    syl[1] = self.get_rhyming_scheme()
                    break
        return resArr

    def get_syl_set(self, max, length, rhyming_syls):
        res = []
        if max == length:
            return self.tag_rhymes([1] * length, rhyming_syls)
        for ans in self.sum_to_n(max):
            if len(ans) == length and self.check_syl_set(ans, rhyming_syls):
                res.append(ans)
        return self.tag_rhymes(random.choice(res), rhyming_syls)

    def sum_to_n(self, n):
        from operator import sub
        b, mid, e = [0], list(range(1, n)), [n]
        splits = (d for i in range(n) for d in combinations(mid, i))
        return (list(map(sub, chain(s, e), chain(b, s))) for s in splits)


