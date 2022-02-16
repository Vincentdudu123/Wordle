import matplotlib.pyplot as plt
import pandas as pd
import os
import math
import numpy as np

if __name__=="__main__":
    ff = os.path.dirname(os.path.realpath(__file__))
    f = "/../database/guess_short.csv"
    df=pd.read_csv(ff+f)
    guess=df['guess'].values.tolist()
    
    results=[]

    plt.xlabel('Trials')
    plt.ylabel('Guesses')
    plt.hist(guess,8,alpha=0.75)
    plt.grid(True)
    plt.savefig("guess_short.png")

