from nltk.corpus import cmudict, brown
from nltk import pos_tag
from nltk import word_tokenize
from pronouncing import rhymes
import random

class Poem_Word:
    word = ""
    rhyme_tag = 0
    no_syls = 0
    tag = ''
    d = cmudict.dict()

    def rhyme(self, inp, level):
        entries = cmudict.entries()
        syllables = [(word, syl) for word, syl in entries if word == inp]
        rhymes = []
        for (word, syllable) in syllables:
            rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
        return set(rhymes)

    def doTheyRhyme(self, word2):
        if self.word.find(word2) == len(self.word) - len(word2):
            return False
        if word2.find(self.word) == len(word2) - len(self.word):
            return False

        return self.word in self.rhyme(word2, 1)


    def nsyl(self, word):
        return [len(list(y for y in x if y[-1].isdigit())) for x in self.d[word.lower()]]

    def find_rhymes(self, word, syl):
        arr = rhymes(word)
        res = []
        for item in arr:
            syls = self.nsyl(item)
            if syl in syls or syl+1 in syls or syl-1 in syls:
                res.append(item)
        return res

    def get_word(self, tag, syl, rhyme=None):
        raw = tuple({word for word, pos in brown.tagged_words()[:80000] if pos.startswith(tag)})
        self.tag = tag
        self.no_syls = syl
        res = []
        for word in raw:
            try:
                syls = self.nsyl(word)
                if syl in syls:
                    if rhyme:
                        rhyme_words = self.find_rhymes(rhyme.word, syl)
                        if rhyme_words:
                            res.extend(self.find_rhymes(rhyme.word, syl))
                            break
                        else:
                            res.append("REDACTED")
                            break
                    else:
                        res.append(word.lower())
            except KeyError:
                continue

        try:
            self.word = random.choice(res)
        except IndexError:
            print(tag, syl, res)
            self.no_syls = 1
            self.word = "to"
