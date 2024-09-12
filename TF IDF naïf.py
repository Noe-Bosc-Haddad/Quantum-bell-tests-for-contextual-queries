# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 08:59:13 2024

@author: Utilisateur
"""

corpus=[["La","chienne","mange"], ["Teddy","mange","le","chien"], ["le","crocodile","mange","Teddy"]]

import numpy as np

#word=word in the query
#corpus=ensemble de documents
#document=page web étudiée

def tf(word, doc) :
    N=0
    for word_2 in doc :
        if word_2==word:
            N+=1
    return N/len(doc)

def idf(word,corpus):
    N=0
    for doc in corpus :
        if word in doc:
            N+=1
    return np.log(len(corpus)/N)

def tfidf(word, doc, corpus) :
    return tf(word, doc)*idf(word, corpus)



