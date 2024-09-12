import numpy as np
from formattext import text2vec
import json


global WASTEWORDS
WASTEWORDS = "the a it they their its his her him them"

def Hal_construct(input_array:np.ndarray, window_size:int = 10) -> np.ndarray:
    global WASTEWORDS 
    ## get word vec
    unique_words = np.unique(input_array)
    ## destroy waste words
    WASTEWORDS = text2vec(WASTEWORDS)
    for waste in WASTEWORDS :
        unique_words = np.delete(unique_words, np.where(unique_words == waste))

    
    # initialize Hal 
    hal = np.zeros((unique_words.size, unique_words.size), dtype= int)

    #initialize dict
   
    word2int = {}
    int2word = {}
    for i in range(unique_words.size) :
        word2int[unique_words[i]] = i
        int2word[i] = unique_words[i]
    #don't need unique_words anymore
    print(word2int)
    unique_words = False
    # completing HAL
    for i in range(input_array.size) :

        if not input_array[i] in WASTEWORDS :
            j = i + 1
            while j < input_array.size and j-i<=window_size:

                if not input_array[j] in WASTEWORDS:

                    hal[word2int[input_array[i]]][word2int[input_array[j]]] += window_size - j+i+1;
                j +=1
                

    return hal


def json_extractor(path:str):
    with open(path) as input_file :
        document_list = json.load(input_file)
    return iter(document_list)

def makecorpushals(path:str, window_size : int =10 ) -> None:
    documentiterator = json_extractor(path)
    hal_list = []
    for document in documentiterator:
        hal_list.append(Hal_construct(np.array(document), window_size))
    with open("./hal_matrices.json", 'w') as halw :
        json.dump(hal_list, halw, intend = 4)


    


if __name__ == "__main__" :
    input = np.array(["the", "dog", 'runs', 'through', 'the', 'backyard', 'the', 'backyard', 'is','no','more', 'clean'])
    makecorpushals('./wikipedia_documents_cleaned.json')
    with open("./hal_matrices.json") as f :
        print(json.load(f)[0])
