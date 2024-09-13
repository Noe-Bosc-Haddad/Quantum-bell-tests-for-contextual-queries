import numpy as np;


def make_document_vector(hal_matrix_symetric):
    doc_vec = np.sum(hal_matrix_symetric, axis = 1)
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
    p = np.dot(word1[0], word2[0])
    B_mat = np.array([[2*p**2-1, 2*p*np.sqrt(1-p**2)], [2*p*np.sqrt(1-p**2), 1-2*p**2]])
    B_mat_x = np.array([[-2*p*np.sqrt(1-p**2),2*p**2-1], [2*p**2-1,2*p*np.sqrt(1-p**2)]])
    B_mat_plus = -(B_mat+B_mat_x)/np.sqrt(2)
    B_mat_minus = (B_mat-B_mat_x)/np.sqrt(2)
    return B_mat_plus, B_mat_minus

global A_mat, A_mat_x
A_mat = np.array([[1,0],[0,-1]])
A_mat_x = np.array([[0,1],[1,0]])

def project_document2wordbase(vector1, vector2, document_vector):

    alpha = np.dot(vector1, document_vector)
    alpha_ort = np.dot(vector2, document_vector)
    normalisation_coefficient = np.sqrt(alpha**2 + alpha_ort**2)
    return  alpha/normalisation_coefficient, alpha_ort/normalisation_coefficient

def esperance(alpha, alpha_ort, matrix) :
    document_vector = np.array([alpha, alpha_ort])
    return np.dot(document_vector, np.dot(matrix, document_vector))

def Bell_query(B_mat_plus, B_mat_minus, alpha, alpha_ort):
    esp_A_Bplus = esperance(alpha, alpha_ort, np.dot(A_mat, B_mat_plus))
    esp_Ax_Bplus = esperance(alpha, alpha_ort, np.dot(A_mat_x, B_mat_plus))
    esp_A_Bminus = esperance(alpha, alpha_ort, np.dot(A_mat,B_mat_minus ))
    esp_Ax_Bminus = esperance(alpha, alpha_ort, np.dot(A_mat_x, B_mat_minus))
    return np.abs(esp_A_Bplus+esp_Ax_Bplus) + np.abs(esp_A_Bminus- esp_Ax_Bminus)



    
