import pandas as pd
import os
from wordfreq import word_frequency

if __name__=="__main__":
    ff = os.path.dirname(os.path.realpath(__file__))
    f = "/../database/wordle.csv"

    wordlist=pd.read_csv(ff+f)
    wordlist=wordlist.loc[wordlist['freq']!=0.0]

    wordlist = wordlist.set_index('word')

    