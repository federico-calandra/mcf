"""
Partendo dalla formula per il periodo T appena ricavata, produrre uno script python che:
calcoli il periodo T in funzione del punto di partenza x₀ (utilizzando scipy.integrate.simpson);
produca un grafico di T in funzione di x₀;
ripetere l'analisi precedente per un'energia potenziale del tipo V(x)=kx² e confrontare i risultati;
provare formule alternative per V(x) (rispettando la condizione di simmetria rispetto all'origine) e confrontare i risultati.
Esempi: kx⁴, k|x|^(3/2);
utilizzare il modulo argparse per permettere all'utente di scegliere le opzioni sul potenziale da visualizzare.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simpson
import argparse

## PARSER
def argp():
    parser=argparse.ArgumentParser()
    parser.add_argument('-V4', action='store_true')
    parser.add_argument('-V15', action='store_true')
    return  parser.parse_args()

args=argp()

m=1
dx=0.001

def V4(x,k=1):
    return k*x**4

def V15(x,k=1):
    return np.abs(k*x**1.5)

x0=np.linspace(dx,1,10)

if args.V4==True:
    T=np.empty(0)
    for w in x0:
        xt=np.arange(0,w,dx)
        tt=1./np.sqrt( V4(w)-V4(xt) )
        T=np.append(T,simpson(tt, dx=dx))
        
    plt.plot(x0,T)
    plt.show()
    
if args.V15==True:
    T=np.empty(0)
    for w in x0:
        xt=np.arange(0,w,dx)
        tt=1./np.sqrt( V15(w)-V15(xt) )
        T=np.append(T,simpson(tt, dx=dx))
        
    plt.plot(x0,T)
    plt.show()

else:
    T4=np.empty(0)
    for w in x0:
        xt=np.arange(0,w,dx)
        tt=1./np.sqrt( V4(w)-V4(xt) )
        T4=np.append(T4,simpson(tt, dx=dx))
        
    T15=np.empty(0)
    for w in x0:
        xt=np.arange(0,w,dx)
        tt=1./np.sqrt( V15(w)-V15(xt) )
        T15=np.append(T15,simpson(tt, dx=dx))
        
    plt.subplot(1,2,1)
    plt.plot(x0,T4)
    plt.subplot(1,2,2)
    plt.plot(x0,T15)
    plt.show()
