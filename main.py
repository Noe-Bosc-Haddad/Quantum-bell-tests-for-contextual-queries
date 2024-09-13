# main.py gathers everythings
#  
import extract_wikipedia_text
import Bell
import matplotlib.pyplot as plt
import numpy as np
from testlocal import test_func 

global Parameters
Parameters = {
    "pages" : ["First_amendment_to_the_United_States_Constitution"], #list[str]
    "query" : ["states", "united"], #list[str], .__length__ = 2
    "window" : 10, #int
#================================================================
####                       FLAGS                             ####
#================================================================
    # Bell curve computing and printing one doc
    "Bell flag" : False, #Bool
    "Plotting" : True, #Bool
    "Printing" : True, #Bool enable some heavy prints
    "Test" : False, #Bool

    #multiple window
    "window range" : 50 #int, LAST TESTED VALUE
}


if __name__ == "__main__" :
# extract wiki. 
    extract_wikipedia_text.get_pages(Parameters['pages'])
    if Parameters["Bell flag"] :
        print("hi")
        Bellparam = Bell.Compute_Bell(Parameters)
        print("Bell's parameter for window_size {} is : {}".format(Parameters["window"], Bellparam))


    if Parameters["Plotting"] :
        print("Constructing tables for plotting")
        WINDOW_TABLE = []
        BELL_TABLE = []
        local_Parameters = Parameters.copy()
        # going thourgh window size:
        print("FOR loop start")
        for window_size in range(1,Parameters["window range"]+1) :
            if Parameters["Printing"] : 
                print("window_size : {}".format(window_size));
            local_Parameters["window"] = window_size
            WINDOW_TABLE.append(window_size)
            BELL_TABLE.append(Bell.Compute_Bell(local_Parameters))
        print("FOR loop end")
        #destruction
        local_Parameters = {}
        fig, ax = plt.subplots(1,1)
        ax.plot(WINDOW_TABLE, BELL_TABLE, marker='o')
        ax.plot(WINDOW_TABLE, np.ones(len(WINDOW_TABLE))*2, linestyle = "dashdot", color = "black")
        ax.plot(WINDOW_TABLE, np.ones(len(WINDOW_TABLE))*2*np.sqrt(2), linestyle = "dotted", color = "black")
        
        ax.set_ylim(0, 2*np.sqrt(2))
        ax.set_xlabel('Window size w')
        ax.set_ylabel('Bell parameter S')
        ax.set_title('Bell parameter as a function of window size w')
        fig.savefig('./fig/Bell_Parameter_main')
    
    if Parameters["Test"] :
        test_func(Parameters)


