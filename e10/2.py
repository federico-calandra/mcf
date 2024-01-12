import numpy as np

def pphi(phi):
    return 0.25*np.sin(phi/2)

def phi():
    prob_cum = np.random.random()
    phi = 2*np.arccos(1-2*prob_cum)
    return phi


