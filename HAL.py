import numpy as np
import string;
from formattext import text2vec



global WASTEWORDS
WASTEWORDS = "le, la, les, un, une, de, des"

def Hal_construct(input_text:str) -> np.ndarray:
    words_vec = text2vec(input_text)
    unique_words = np.unique(words_vec)
    unique_words.r
