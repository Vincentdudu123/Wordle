import os
#all near 13000 possibilities

import pandas as pd
from wordfreq import word_frequency
if __name__=="__main__":

    ff = os.path.dirname(os.path.realpath(__file__))
    f = "/../database/wordle_web.txt"
    wordle_web=[]
    with open(ff+f) as file:
        content=file.readlines()
        for a in content:
            a=a.split(',')
            a=[x[1:-1] for x in a]
            wordle_web.extend(a)

    wordfrequency=[]
    for i in wordle_web:
        wordfrequency.append(word_frequency(i,'en'))   
        
    df = pd.DataFrame(data=wordle_web,columns=['word'])

    df['freq']=wordfrequency
    with open(ff+"/../database/wordle_web.csv") as file:
        df.to_csv(ff+"/../database/wordle_web.csv",encoding='utf-8')


