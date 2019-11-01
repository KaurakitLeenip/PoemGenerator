class PoemLine:
    line = []
    rhyme_words = []
    rhyme_scheme = []

    # def set_rhyme_words(self):
    #     for i in range(len(self.rhyme_scheme)):
    #         if self.rhyme_scheme[i][1] > 0:
    #             self.rhyme_words.append(self.line[i])

    def set_rhyme_tags(self):
        for i in range(len(self.rhyme_scheme)):
            self.line[i].rhyme_tag = self.rhyme_scheme[i][1]

    def to_string(self):
        res = ""
        for word in self.line:
            res += (word.word + "\n")
        return res

    def get_rhyme_words(self, scheme):
        for item in self.rhyme_words:
            if item[1] == scheme:
                return item[0]
        return ''

