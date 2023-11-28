import numpy as np
import scipy.integrate
import matplotlib.pyplot as plt

def Vin(t):
    if np.trunc(t) % 2 == 0:
        return 1
    elif np.trunc(t) % 2 == 1:
        return -1
    

