import numpy as np;
import json
import HAL


def make_document_vector(hal_matrix_symetric):
    doc_vec = np.sum(hal_matrix_symetric, axis = 0)
    return doc_vec


def make_hal_symmetric(hal_matrix):
    return hal_matrix + np.transpose(hal_matrix)

def normalize_vector(word_vector):
    return word_vector/(np.linalg.vector_norm(word_vector))


def make_base_2query_w1(word_vector1,word_vector2):
    normalized1 = normalize_vector(word_vector1)
    word_orthogonal = word_vector2 - np.dot(word_vector2,word_vector1)*word_vector1
    
    return (normalized1, normalize_vector(word_orthogonal))

def B_matrix(word1, word2):
    p = np.dot(word1, word2)
    B_mat = np.array([[2*p**2-1, 2*p*np.sqrt(1-p**2)], [2*p*np.sqrt(1-p**2), 1-2*p**2]])
    B_mat_x = np.array([[-2*p*np.sqrt(1-p**2),2*p**2-1], [2*p**2-1,2*p*np.sqrt(1-p**2)]])
    B_mat_plus = -(B_mat+B_mat_x)/np.sqrt(2)
    B_mat_minus = (B_mat-B_mat_x)/np.sqrt(2)
    return B_mat_plus, B_mat_minus

def project_document2wordbase(vector1, vector2, document_vector):

    alpha = np.dot(vector1, document_vector)
    alpha_ort = np.dot(vector2, document_vector)
    normalisation_coefficient = np.sqrt(alpha**2 + alpha_ort**2)
    return  alpha/normalisation_coefficient, alpha_ort/normalisation_coefficient

def esperance(alpha, alpha_ort, matrix) :
    document_vector = np.array([alpha, alpha_ort])
    return np.dot(document_vector, np.dot(matrix, document_vector))

def Bell_query(B_mat_plus, B_mat_minus, alpha, alpha_ort):
     
    A_mat = np.array([[1,0],[0,-1]])
    A_mat_x = np.array([[0,1],[1,0]])

    esp_A_Bplus = esperance(alpha, alpha_ort, np.dot(A_mat, B_mat_plus))
    esp_Ax_Bplus = esperance(alpha, alpha_ort, np.dot(A_mat_x, B_mat_plus))
    esp_A_Bminus = esperance(alpha, alpha_ort, np.dot(A_mat,B_mat_minus ))
    esp_Ax_Bminus = esperance(alpha, alpha_ort, np.dot(A_mat_x, B_mat_minus))
    return np.abs(esp_A_Bplus+esp_Ax_Bplus) + np.abs(esp_A_Bminus- esp_Ax_Bminus)



def Compute_Bell(Parameters: dict) -> np.float64  :
    if Parameters["Printing"]: 
        print("Making HAL matrix")    
    HAL.makecorpushals("./json_data/wikipedia_documents_cleaned.json", window_size=Parameters["window"], 
                      target= "json_data/{}_window_{}.json".format(Parameters['pages'][0], Parameters["window"]))
    if Parameters["Printing"] :
        print("done")
        #loading HAL matrix and dictionaries
        print("fetching matrix")
    with open("./json_data/{}_window_{}.json".format(Parameters['pages'][0], Parameters["window"])) as jsonfile :
        file = json.load(jsonfile)["document0"]
        word2int = file["word2int"]
        hal_doc = file["HAL"]
    file = None
    try :
        if Parameters["Printing"] :
            print("Computing Bell")
        word1_index = word2int[Parameters["query"][0]]
        word2_index = word2int[Parameters["query"][1]]
        vector_word1 = normalize_vector(hal_doc[word1_index])
        vector_word2 = normalize_vector(hal_doc[word2_index])
        base1_vector,base1_vector_ort = make_base_2query_w1(vector_word1, vector_word2) #base of vector1 (word1)
        doc_vector = normalize_vector(make_document_vector(make_hal_symmetric(hal_doc)))
        projected_doc_vector, projected_doc_vector_ort = project_document2wordbase(base1_vector,base1_vector_ort,doc_vector)
        B_plus, B_minus = B_matrix(vector_word1, vector_word2)
        return Bell_query(B_plus, B_minus, projected_doc_vector, projected_doc_vector_ort)
            

        
    except Exception as err:
        print("The query word << {} >> is not in the document".format(err))
        return np.float64(-1.0)



    
