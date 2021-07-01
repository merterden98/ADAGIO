import numpy as np
def main(): 
    print("Hello ")
    markov = np.array([1, 2, 3])
    
    markov = markov/markov.sum(axis = 0)
    
