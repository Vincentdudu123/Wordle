"""
wordle data base
5 letters
"""
from matplotlib.pyplot import xlabel
import pandas as pd
import os
import math
import numpy as np

from tqdm import tqdm
import multiprocessing as mp

class Wordle(object):

    def __init__(self):
        self.ff = os.path.dirname(os.path.realpath(__file__))
        self.f = "/../database/wordle.csv"
        self.df=pd.read_csv(self.ff+self.f)
        self.df=self.df.loc[self.df['freq']!=0.0].set_index('word')
        self.word=self.df.index.tolist()
        self.guesses=0

    def feedword(self,feedword,initguess):
        self.answer=feedword
        self.guessing(initguess)
    
    def guessing(self,initguess):
        self.guesses+=1
        print(initguess)
        result=0
        for i, x in enumerate(initguess):
            if x==self.answer[i]:
                self.letterSeq(x,i)
            elif x!=self.answer[i] and x in self.answer:
                self.letterRemain(x)
                self.letterNotSeq(x,i)
                result+=1
            else:
                self.letterRemove(x)
                result+=2
        if result==0:
            print("the guesses: %i" % self.guesses)
            return self.guesses
        word=self.sampling()
        self.guessing(word)
    
    def sampling(self):
        df=self.df.copy()
        print("the shape of the remaining dataset %i" % df.shape[0])
        pool=mp.Pool(mp.cpu_count()-2)
        Entropyset=[tqdm(pool.imap(self.getentropy,  df.index.tolist()), total=len(df.index.tolist()))]# for word in df.index.tolist()]
        pool.close()
        '''
        for i in tqdm(range(self.df.shape[0])):
            word=self.df.index.tolist()[i]
            Entropylist=[]
            for j0 in range(3):
                for j1 in range(3):
                    for j2 in range(3):
                        for j3 in range(3):
                            for j4 in range(3):
                                j=[j0,j1,j2,j3,j4]
                                dff=self.elimate(df,word,j)
                                if dff.shape[0]!=0:
                                    Entropylist.append(self.calculateEntropy(dff))
            Entropyset.append(np.average(np.asarray(Entropylist)))
        '''
        df['entropy_distri']=Entropyset[0]
        return df['entropy_distri'].idxmin()

    def getentropy(self,word):
        df=self.df.copy()            
        Entropylist=[]
        for j0 in range(3):
            for j1 in range(3):
                for j2 in range(3):
                    for j3 in range(3):
                        for j4 in range(3):
                            j=[j0,j1,j2,j3,j4]
                            dff=self.elimate(df,word,j)
                            if dff.shape[0]!=0:
                                Entropylist.append(self.calculateEntropy(dff))
        return np.average(np.asarray(Entropylist))
    def elimate(self,dff,word,j):
        df = dff.copy()
        for i in range(len(j)):
            if j[i]==0:
                df=self.letterSeqE(df,word[i],i)
            elif j[i]==1:
                df=self.letterRemainE(df,word[i])
                df=self.letterNotSeqE(df,word[i],i)
            else:
                df=self.letterRemoveE(df,word[i])
        return df
        #return self.calculateEntropy(df)                           


    def calculateEntropy(self,dff):
        df=dff.copy()       
        probability=df['freq'].sum()
        df['freq']/=probability

        Entropy=[]
        for index,row in df.iterrows():
            Entropy.append(row['freq']*math.log(1/row['freq'],2.0))
        return np.sum(np.asarray(Entropy))


        pass


    def letterSeqE(self, dff, letter, seq):
        df=dff.copy()
        #print(df.shape,letter,seq)
        for word in df.index.tolist():
            if letter==word[seq]:
                pass
            else:
                df=df.drop(word)
        #print(df.shape)
        return df

    def letterRemainE(self, dff, letter):
        df=dff.copy()
        remove=[]
        for word in df.index.tolist():
            if letter not in word:
                df=df.drop(word)
        return df


    def letterNotSeqE(self, dff, letter, seq):
        df=dff.copy()
        remove=[]
        for word in df.index.tolist():
            if letter==word[seq]:                
                df=df.drop(word)
        return df

    def letterRemoveE(self, dff, letter):
        df=dff.copy()
        remove=[]
        for word in df.index.tolist():
            if letter in word:
                df=df.drop(word)
        return df

    def letterSeq(self, letter, seq):
        wordseq=[]
        for word in self.word:
            if letter==word[seq]:
                if word not in wordseq:
                    wordseq.append(word)
            else:
                self.df=self.df.drop(word)
        self.word.clear()
        for i in wordseq:
            self.word.append(i)

    def letterRemain(self, letter):
        remove=[]
        for word in self.word:
            if letter not in word:
                if word not in remove:
                    remove.append(word)
        for i in remove:
            self.word.remove(i)
            self.df=self.df.drop(i)


    def letterNotSeq(self, letter, seq):
        remove=[]
        for word in self.word:
            if letter==word[seq]:
                if word not in remove:
                    remove.append(word)
        for i in remove:
            self.word.remove(i)
            self.df=self.df.drop(i)

    def letterRemove(self, letter):
        remove=[]
        for word in self.word:
            if letter in word:
                if word not in remove:
                    remove.append(word)
        for i in remove:
            self.word.remove(i)
            self.df=self.df.drop(i)


if __name__=="__main__":
    a=Wordle()
    a.feedword("humor","crane")

