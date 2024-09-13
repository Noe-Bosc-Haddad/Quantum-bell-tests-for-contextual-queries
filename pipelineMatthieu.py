import numpy as np
import matplotlib.pyplot as plt
import json

debug = False
global WASTEWORDS
WASTEWORDS = [
    "the", "a", "an", "this", "that", "these", "those",
    "he", "she", "they", "it", "we", "you", "him", "her", "them", "us",
    "I", "me", "myself", "himself", "herself", "themselves", "itself",
    "and", "or", "but", "so", "yet", "for", "nor",
    "in", "on", "at", "by", "with", "about", "into", "over", "under", "between", "through",
    "is", "are", "was", "were", "be", "being", "been", "have", "has", "had", 
    "do", "does", "did", "will", "would", "should", "can", "could", "may", "might", "must", "shall",
    "very", "really", "just", "too", "quite", "almost", "nearly", "always", "never", "sometimes", "often",
    "not", "no", "yes", "all", "some", "any", "each", "every", "both", "either", "neither"
]
def create_HAL_matrix(document):
    words = np.unique(np.array((document))) #creates unique word vector
    for waste in WASTEWORDS: #delete waste words
        words = np.delete(words, np.where(words == waste))

    
    hal_dict_matrix = {}
    for word in words:
        hal_dict_matrix[word]={}
        for word2 in words:
            hal_dict_matrix[word][word2] = 0
        
    return hal_dict_matrix

def fill_HAL_matrix(document,hal_dict_matrix,window_size):
    window_size_updated = window_size
    len_doc = len(document)
    for i in range(len_doc):
        word = document[i]
        if i+window_size >=len_doc:
           window_size_updated += -1
        if not (word in WASTEWORDS) :
            for k in range(1,window_size_updated+1):
                    word2 = document[i+k]
                    if not (word2 in WASTEWORDS):
                         hal_dict_matrix[word][word2] += window_size-k+1
    return hal_dict_matrix

def hal_dict_to_matrix(hal_dict_matrix):
    hal_matrix = []
    for i in range(len(hal_dict_matrix.keys())):
        hal_matrix.append(list(list(hal_dict_matrix.values())[i].values()))
    return hal_matrix,list(hal_dict_matrix.keys())

def hal_to_symmetric(hal_matrix):
    return hal_matrix + np.transpose(hal_matrix)

def document_vector(hal_matrix_symmetric):
    n_words = len(hal_matrix_symmetric)
    doc_vector = np.array([0]*n_words)
    for i in range(n_words):
        doc_vector[i] = sum(hal_matrix_symmetric[i])
    return doc_vector

def extract_word_vector(hal_matrix_symmetric,words_list,word_to_extract):
    word_position = words_list.index(word_to_extract)
    return hal_matrix_symmetric[word_position]

def normalize_vector(word_vector):
    if np.linalg.norm(word_vector) == 0:
        return word_vector
    else:
        return word_vector/(np.linalg.norm(word_vector))


#Gramm-Schimdt on 2 vectors 'word_vector_normalised' is e_1 and 'word_vector_normalised2' u_2
def base_from_word_vectors(word_vector_normalised,word_vector_normalised2):
    word_vector_ort = word_vector_normalised2 - np.dot(word_vector_normalised2,word_vector_normalised)*word_vector_normalised
    word_vector_normalised_ort = normalize_vector(word_vector_ort)
    return word_vector_normalised,word_vector_normalised_ort

def project_doc_onto_base(base_vector1,base_vector2,document_vector):
    alpha = np.dot(base_vector1,document_vector)
    alpha_ort = np.dot(base_vector2,document_vector)
    normalisation_factor = np.sqrt(alpha**2+alpha_ort**2)
    return alpha/normalisation_factor,alpha_ort/normalisation_factor

def B_matrices(base_vector1,word_vector_normed2):
    p = np.dot(base_vector1,word_vector_normed2)
    ''' B = [   [ 2p²-1         2p.sqrt(1-p²) ]
                [ 2p.sqrt(1-p²)    1-2p²      ] ]
    '''
    B_mat = np.array([[2*p**2-1 ,2*p*np.sqrt(1-p**2)],[2*p*np.sqrt(1-p**2),1-2*p**2]])
    ''' B_x = [ [ -2p.sqrt(1-p²)         2p²-1      ]
                [ 2p²-1             2p.sqrt(1-p²)   ] ]
    '''
    B_mat_x = np.array([[-2*p*np.sqrt(1-p**2),2*p**2-1],[2*p**2-1,2*p*np.sqrt(1-p**2)]])
    B_mat_plus = -(B_mat+B_mat_x)/np.sqrt(2)
    B_mat_minus = (B_mat-B_mat_x)/np.sqrt(2)
    return B_mat_plus,B_mat_minus

def esp(alpha,alpha_ort,matrix):
    document_vector = np.array([alpha,alpha_ort])
    return np.dot(document_vector, np.dot(matrix,document_vector))

def S_query(A_mat,A_mat_x,B_mat_plus,B_mat_minus,alpha,alpha_ort):
    esp_A_Bplus = esp(alpha,alpha_ort,np.dot(A_mat,B_mat_plus))
    if debug:
        print("esp_A_Bplus")
        print(esp_A_Bplus)
        print(' ')
    esp_Ax_Bplus = esp(alpha,alpha_ort,np.dot(A_mat_x,B_mat_plus))
    if debug:
        print("esp_Ax_Bplus")
        print(esp_Ax_Bplus)
        print(' ')
    esp_A_Bminus = esp(alpha,alpha_ort,np.dot(A_mat,B_mat_minus))
    if debug:
        print("esp_A_Bminus")
        print(esp_A_Bminus)
        print(' ')
    esp_Ax_Bminus = esp(alpha,alpha_ort,np.dot(A_mat_x,B_mat_minus))
    if debug:
        print("esp_Ax_Bminus")
        print(esp_Ax_Bminus)
        print(' ')
        print("S_query")
        print(np.abs(esp_A_Bplus + esp_Ax_Bplus) + np.abs(esp_A_Bminus - esp_Ax_Bminus))
        print(' ')
    return np.abs(esp_A_Bplus + esp_Ax_Bplus) + np.abs(esp_A_Bminus - esp_Ax_Bminus)

def Bell_l(document, word1, word2, window_size):
    if debug:
        print(' ')
        print('-------------------------------------')
        print('Window size :', window_size)
        print(' ')
    hal_dict_matrix = create_HAL_matrix(document)
    hal_dict_matrix = fill_HAL_matrix(document,hal_dict_matrix, window_size)
    if debug:
        print("hal_dict_matrix")
        print(hal_dict_matrix)
        print(' ')
    hal_matrix, words_list= hal_dict_to_matrix(hal_dict_matrix)
    if debug:
        print('hal_matrix')
        print(hal_matrix)
        print(' ')
        print('words_list')
        print(words_list)
        print(' ')
    # hal_matrix_symmetric= hal_to_symmetric(hal_matrix)
    hal_matrix_symmetric = hal_matrix   #testing 
    if debug:
        print('hal_matrix_symmetric')
        print(hal_matrix_symmetric)
        print(' ')
    doc_vector = document_vector(hal_matrix_symmetric)
    if debug:
        print('doc_vector')
        print(doc_vector)
        print(' ')
    word_vector_1 = extract_word_vector(hal_matrix_symmetric,words_list, word1)
    if debug:
        print('word_vector_1')
        print(word_vector_1)
        print(' ')
    word_vector_2 = extract_word_vector(hal_matrix_symmetric,words_list, word2)
    if debug:
        print('word_vector_2')
        print(word_vector_2)
        print(' ')
    word_vector_normed_1 = normalize_vector(word_vector_1)
    if debug:
        print('word_vector_normed_1')
        print(word_vector_normed_1)
        print(' ')
    word_vector_normed_2 = normalize_vector(word_vector_2)
    if debug:
        print('word_vector_normed_2')
        print(word_vector_normed_2)
        print(' ')
    base_vector_1,base_vector_2 = base_from_word_vectors(word_vector_normed_1,word_vector_normed_2)
    if debug:
        print('base_vector_1')
        print(base_vector_1)
        print(' ')
        print('base_vector_2')
        print(base_vector_2)
        print(' ')
    alpha, alpha_ort = project_doc_onto_base(base_vector_1,base_vector_2,doc_vector)
    if debug:
        print('alpha')
        print(alpha)
        print(' ')
        print('alpha_ort')
        print(alpha_ort)
        print(' ')
    B_mat_plus, B_mat_minus = B_matrices(word_vector_normed_1,word_vector_normed_2)
    if debug:
        print('B_mat_plus')
        print(B_mat_plus)
        print(' ')
        print('B_mat_minus')
        print(B_mat_minus)
        print(' ')
    A_mat = [[1,0],[0,-1]]
    A_mat_x = [[0,1],[1,0]]
    return S_query(A_mat,A_mat_x,B_mat_plus,B_mat_minus,alpha,alpha_ort)

def Bell(document, word1, word2, min, max):
    X = []
    Y = []
    for l in range(min, max):
        X.append(l)
        Y.append(Bell_l(document, word1, word2, l))
    return X, Y

#with open('wikipedia_documents_cleaned.json', 'r') as f:
#    corpus = json.load(f)

word1 = "united"
word2 = "states" 

'''
document = [
    "Le", "droit", "du", "sol", "en", "France", "est", "un", "principe", "juridique", "selon", "lequel", 
    "une", "personne", "née", "sur", "le", "territoire", "français", "peut", "acquérir", "la", "nationalité", 
    "française", "sous", "certaines", "conditions", "Ce", "système", "s'oppose", "au", "droit", "du", "sang", 
    "qui", "repose", "sur", "la", "transmission", "de", "la", "nationalité", "par", "les", "parents", "Le", 
    "droit", "du", "sol", "en", "France", "existe", "depuis", "plusieurs", "siècles", "Il", "permet", "à", 
    "un", "enfant", "né", "en", "France", "de", "devenir", "français", "automatiquement", "à", "sa", "majorité", 
    "s'il", "a", "résidé", "sur", "le", "territoire", "français", "de", "manière", "continue", "Il", "peut", 
    "également", "demander", "la", "nationalité", "à", "partir", "de", "l'âge", "de", "13", "ans", "sous", 
    "certaines", "conditions", "Le", "droit", "du", "sol", "est", "au", "cœur", "des", "débats", "sur", 
    "l'immigration", "et", "la", "nationalité", "en", "France"
]
'''
with open('./json_data/wikipedia_documents_cleaned.json') as file :
    document = json.load(file)[0]



def print_graph(document, word1, word2, min, max):
    X, Y = Bell(document, word1, word2, min, max)
    fig, ax = plt.subplots(1,1)
    ax.plot(X, Y, marker='o')
    ax.plot(X, np.ones(len(X))*2, linestyle = "dashdot", color = "black")
    ax.plot(X, np.ones(len(X))*2*np.sqrt(2), linestyle = "dotted", color = "black")
     
    ax.set_ylim(0, 2*np.sqrt(2)+0.1)
    ax.set_xlabel('Window size w')
    ax.set_ylabel('Bell parameter S')
    ax.set_title('Bell parameter as a function of window size w')
    fig.savefig('./fig/Bell_Parameter_main')

     
#print_graph(document, word1, word2, 1, 100)

