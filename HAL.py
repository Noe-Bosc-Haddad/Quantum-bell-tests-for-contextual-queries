from typing import Tuple
import numpy as np
import json



def Hal_construct(input_array:np.ndarray, window_size:int = 10) -> Tuple[np.ndarray, dict, dict]:
    ## get word vec
    unique_words = np.unique(input_array)
    WASTEWORDS = ["the","a","their","theirs","it","its", "they","an"]
    ## destroy waste words
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
    unique_words = False
    # completing HAL
    for i in range(len(input_array)) :

        if not input_array[i] in WASTEWORDS :
            j = i + 1
            while j < len(input_array) and j-i<=window_size:

                if not input_array[j] in WASTEWORDS:

                    hal[word2int[input_array[i]]][word2int[input_array[j]]] += window_size - j+i+1;
                j +=1
                

    return hal, word2int, int2word


def json_extractor(path:str) -> list[list[str]]:
    with open(path) as input_file :
        document_list = json.load(input_file)
    return document_list

def makecorpushals(path:str, window_size : int =10 ) -> None:
    documentiterator = json_extractor(path)
    dump = {}
    i = 0
    for document in documentiterator:
        (HAL, word2int, int2word) = Hal_construct(np.array(document), window_size)
        dump["document{}".format(i)] = {"HAL" : HAL.tolist(), "word2int":word2int, "int2word":int2word}
        i+=1
    with open("./hal_matrices.json", 'w') as halw :
        json.dump(dump, halw)


    


if __name__ == "__main__" :
    input = np.array(["the", "dog", 'runs', 'through', 'the', 'backyard', 'the', 'backyard', 'is','no','more', 'clean'])
    makecorpushals('./wikipedia_documents_cleaned.json')
