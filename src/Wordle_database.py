"""
wordle data base
5 letters
"""
from nltk.corpus import words
import string
import pandas as pd
from tqdm import tqdm

def wordleDatabase(f):
    alphabet=string.ascii_lowercase
    wordlist=[]
    setofwords=set(words.words())
    for j in tqdm(range(int(26**5))):
        i=int(j%26)
        i1=int(j/26)
        ii=int(i1%26)
        ii1=int(i1/26)
        iii=int(ii1%26)
        iii1=int(ii1/26)
        iv=int(iii1%26)
        iv1=int(iii1/26)
        v=int(iv1%26)
        v1=int(iv1/26)
        word = alphabet[i]+alphabet[ii]+alphabet[iii]+alphabet[iv]+alphabet[v]

        if word in setofwords:
            wordlist.append(word)
    
    df = pd.DataFrame(data=wordlist,columns=['word'])
    df.to_csv(f,encoding='utf-8')




if __name__=="__main__":
    f = "database/wordle.csv"
    wordleDatabase(f)
