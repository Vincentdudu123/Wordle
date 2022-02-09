"""
wordle data base
5 letters
"""
import pandas as pd
import os

class Wordle_functions(object):
    def __init__(self):
        self.ff = os.path.dirname(os.path.realpath(__file__))
        self.f = "/../database/wordle.csv"
        self.word=pd.read_csv(self.ff+self.f)["word"].values.tolist()

    def letterRemain(self, letters):
        remove=[]
        for i in letters:
            for word in self.word:
                if i not in word:
                    if word not in remove:
                        remove.append(word)
        for i in remove:
            self.word.remove(i)
        print(self.word)

    def letterRemove(self, letters):
        remove=[]
        for i in letters:
            for word in self.word:
                if i in word:
                    if word not in remove:
                        remove.append(word)
        for i in remove:
            self.word.remove(i)
        print(self.word)

    def letterSeq(self, letter, seq):
        wordseq=[]
        for word in self.word:
            if letter==word[seq]:
                if word not in wordseq:
                    wordseq.append(word)
        self.word.clear()
        for i in wordseq:
            self.word.append(i)
        print(self.word)

    def letterNotSeq(self, letter, seq):
        remove=[]
        for word in self.word:
            if letter==word[seq]:
                if word not in remove:
                    remove.append(word)
        for i in remove:
            self.word.remove(i)
        print(self.word)

if __name__=="__main__":
    pass
