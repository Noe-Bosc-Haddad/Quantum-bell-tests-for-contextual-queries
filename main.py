# main.py gathers everythings
#  
import HAL
import extract_wikipedia_text
import Bell
import json


Parameters = {
    "pages" : ["First_amendment_to_the_United_States_Constitution"], #list[str]
    "query" : ["government", "law"], #list[str], .__length__ = 2
    "window" : 10, #int
    # Bell curve computing and printing one doc
    "Bell flag" : True, #Bool
    #multiple window
    "window range" : 50 #int
}


if __name__ == "__main__" :
# extract wiki. 
    extract_wikipedia_text.get_pages(Parameters['pages'])
    if Parameters["Bell flag"] :
        print("Making HAL matrix")    
        HAL.makecorpushals("./json_data/wikipedia_documents_cleaned.json", window_size=Parameters["window"], 
                           target= "json_data/{}_window_{}.json".format(Parameters['pages'][0], Parameters["window"]))
        print("done")
        #loading HAL matrix and dictionaries
        print("fetching matrix")
        with open("./json_data/{}_window_{}.json".format(Parameters['pages'][0], Parameters["window"])) as jsonfile :
            file = json.load(jsonfile)["document0"]
            word2int = file["word2int"]
            hal_doc = file["HAL"]
        file = None
        try :
            print("Computing Bell")
            word1_index = word2int[Parameters["query"][0]]
            word2_index = word2int[Parameters["query"][1]]
            vector_word1 = Bell.normalize_vector(hal_doc[word1_index])
            vector_word2 = Bell.normalize_vector(hal_doc[word2_index])
            base1_vector,base1_vector_ort = Bell.make_base_2query_w1(vector_word1, vector_word2) #base of vector1 (word1)
            doc_vector = Bell.normalize_vector(Bell.make_document_vector(Bell.make_hal_symmetric(hal_doc)))
            projected_doc_vector, projected_doc_vector_ort = Bell.project_document2wordbase(base1_vector,base1_vector_ort,doc_vector)
            B_plus, B_minus = Bell.B_matrix(vector_word1, vector_word2)
            print("Bell factor result for {} window size : {}".format(Parameters["window"],Bell.Bell_query(B_plus, B_minus, projected_doc_vector, projected_doc_vector_ort)))
            

            
        except Exception as err:
            print("The query word << {} >> is not in the document".format(err))
            
            

        

