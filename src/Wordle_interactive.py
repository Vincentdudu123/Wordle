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
        self.f = "/../database/wordle_short.csv"
        self.df=pd.read_csv(self.ff+self.f)
        self.df=self.df.set_index('word')

    
    def guessing(self,initguess,answer):
        for i, x in enumerate(answer):
            if x=='g':
                self.letterSeq(initguess[i],i)
            elif x=='y':
                self.letterRemain(initguess[i],i)
            else:
                self.letterRemove(initguess[i])
        word=self.sampling()
        print(word)
    
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
        return df['entropy_distri'].idxmax()

    def getentropy(self,word):
        df=self.df.copy()           
        Entropie=0.0
        for j0 in range(3):
            for j1 in range(3):
                for j2 in range(3):
                    for j3 in range(3):
                        for j4 in range(3):
                            j=[j0,j1,j2,j3,j4]
                            dff=self.elimate(df,word,j)
                            if dff.shape[0]!=0:
                                Entropie += dff.shape[0]/df.shape[0]*math.log2(1/(dff.shape[0]/df.shape[0]))
        return Entropie
    def elimate(self,dff,word,j):
        df = dff.copy()
        for i in range(len(j)):
            if j[i]==0:
                df=self.letterSeqE(df,word[i],i)
            elif j[i]==1:
                df=self.letterRemainE(df,word[i],i)
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

    def letterRemainE(self, dff, letter, seq):
        df=dff.copy()
        for word in df.index.tolist():
            if letter not in word or letter == word[seq]:
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
        for word in self.df.index.tolist():
            if letter==word[seq]:
                pass
            else:
                self.df=self.df.drop(word)

    def letterRemain(self, letter, seq):
        for word in self.df.index.tolist():
            if letter not in word or letter==word[seq]:
                self.df=self.df.drop(word)

    def letterRemove(self, letter):
        remove=[]
        for word in self.df.index.tolist():
            if letter in word:
                self.df=self.df.drop(word)



if __name__=="__main__":
    ff = os.path.dirname(os.path.realpath(__file__))
    f = "/../database/wordle_short.csv"
    df=pd.read_csv(ff+f)
    word=df['word'].values.tolist()
    guesses=[]
    for i in tqdm(range(len(word))):
        a=Wordle()
        a.feedword(word[i],"crane")
        guesses.append(a.guesses)
        print(np.mean(guesses))
    df = pd.DataFrame(data=guesses,columns=['guess'])
    with open(ff+"/../database/guess_short.csv") as file:
        df.to_csv(ff+"/../database/guess_short.csv",encoding='utf-8')    
