import pipelineMatthieu as pM 
import numpy as np 
import Bell
from HAL import Hal_construct
import json

def test_func(Parameters):
    input_doc = ["the", "dog", "barks", "a", "lot", "barks", "make", "noise", "I", "don't", "like", "noise", "it", 'makes', "me", "angry"]
    print("compare HAL.py and pipeline.py : ")
    hal_pip = np.array(pM.hal_dict_to_matrix(pM.fill_HAL_matrix(input_doc,pM.create_HAL_matrix(input_doc),10))[0])
    hal_whole = Hal_construct(np.array(input_doc),10)
    print("HAL is pipeline.py : ", np.isclose(hal_pip,hal_whole[0])) # IS TRUE !!!!
    print("===============================")
    print("Bell test")
    print("===============================")
    word1 = "dog"
    word2 = "noise"
    Bell_pip = pM.Bell_l(input_doc, word1, word2, 10)
    hal_doc = hal_whole[0]
    word1 = hal_whole[1]["dog"]
    word2 = hal_whole[1]["noise"]
    vector_word1 = Bell.normalize_vector(hal_doc[word1])
    vector_word2 = Bell.normalize_vector(hal_doc[word2])
    base1_vector,base1_vector_ort = Bell.make_base_2query_w1(vector_word1, vector_word2) #base of vector1 (word1)
    doc_vector = Bell.make_document_vector(Bell.make_hal_symmetric(hal_doc))
    projected_doc_vector, projected_doc_vector_ort = Bell.project_document2wordbase(base1_vector,base1_vector_ort,doc_vector)
    B_plus, B_minus = Bell.B_matrix(vector_word1, vector_word2)
    Bell_Bell = Bell.Bell_query(B_plus, B_minus, projected_doc_vector, projected_doc_vector_ort)
    print("same Bell in pip and main : ", np.isclose(Bell_pip, Bell_Bell))
    print(Bell_Bell)
    print(Bell_pip)
    print("vector_doc correct : ", np.isclose(doc_vector , pM.document_vector(pM.hal_to_symmetric(hal_pip))))
     
        
    print("================================")
    print("bigger test")
    print("================================")
    with open("./json_data/wikipedia_documents_cleaned.json") as file :
        input_doc = json.load(file)[0]
        hal_pip = np.array(pM.hal_dict_to_matrix(pM.fill_HAL_matrix(input_doc,pM.create_HAL_matrix(input_doc),10))[0])
        hal_hal = Hal_construct(np.array(input_doc),10)[0]
    print("HAL is pipeline.py : ", np.isclose(hal_pip,hal_hal), "\n searching FALSE in table : ", False in np.isclose(hal_pip, hal_hal)) # We construct the same TABLES HAL IS OK
    print("===============================")
    print("Bell test")
    print("===============================")
    word1 = "united"
    word2 = "states"
    Bell_pip = pM.Bell_l(input_doc, word1, word2, 10)
    Bell_Bell = Bell.Compute_Bell(Parameters)
    print("same Bell in pip and main : ", np.isclose(Bell_pip, Bell_Bell))
    print(Bell_Bell)

