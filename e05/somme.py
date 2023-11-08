"""
Creare il file python somme.py in cui vanno definite due funzioni:
una funzione che restituisca la somma dei primi n numeri naturali, con n da passare tramite un argomento;
una funzione che restituisca la somma delle radici dei primi n numeri naturali, con n da passare tramite un argomento.
Creare uno script python che importi il modulo somme appena creato e ne utilizzi le funzioni
Esaminare la cartella di lavoro
"""

import numpy as np

def sumN(n):
    r=np.arange(1,n+1)
    return np.sum(r)

def sumNsqrt(n):
    r=np.arange(1,n+1)
    return np.sum(np.sqrt(r))

"""
Modificare il file somme.py aggiungendo:
una funzione che restituisca la somma e il prodotto dei primi n numeri naturali, con n da passare tramite un argomento;
una funzione che restituisca \sum_0^n i^\alpha
,con n da passare tramite un argomento e
da passare tramite keyword (kwargs), con valore di default pari a 1.
Modificare lo script python che importa il modulo somme in modo da utilizzare le funzioni appena create.
"""

def sumProd(n):
    r=np.arange(1,n+1)
    return np.sum(r), np.math.factorial(n)

def summation(n,**kwargs):
    if len(kwargs)==0:
        alpha=1
    else:
        alpha=kwargs['alpha']
        
    s=0
    for i in range(n+1):
        s=s+i**alpha
    return s
