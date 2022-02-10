import os
#all near 13000 possibilities

import pandas as pd
from wordfreq import word_frequency
if __name__=="__main__":

    ff = os.path.dirname(os.path.realpath(__file__))
    f = "/../database/wordle_short.txt"
    
        
    df = pd.read_csv(ff+f,sep=" ",names=['word','freq'])

    with open(ff+"/../database/wordle_short.csv") as file:
        df.to_csv(ff+"/../database/wordle_short.csv",encoding='utf-8')


