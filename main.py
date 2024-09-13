# main.py gathers everythings
#  
import HAL
import extract_wikipedia_text
import Bell


Parameters = {
    "pages" : ["First_amendment_to_the_United_States_Constitution"], #list[str]
    "query" : ["governement", "law"], #list[str], .__length__ = 2
    "window" : 10, #int
    # Bell curve computing and printing
    "Bell flag" : True, #Bool
    "window range" : 50 #int
}


if __name__ == "__main__" :
# extract wiki. 
    extract_wikipedia_text.get_pages(Parameters['pages'])
    
