"""
Creare il file python somme.py in cui vanno definite due funzioni:
una funzione che restituisca la somma dei primi n numeri naturali, con n da passare tramite un argomento;
una funzione che restituisca la somma delle radici dei primi n numeri naturali, con n da passare tramite un argomento.
Creare uno script python che importi il modulo somme appena creato e ne utilizzi le funzioni
Esaminare la cartella di lavoro
"""

import somme, os

print('somma',somme.sumN(5))
print('somma radice',somme.sumNsqrt(5))
print('contenuto cartella')
os.system('ls')

"""
Modificare lo script python che importa il modulo somme in modo da utilizzare le funzioni appena create.
"""

s,p=somme.sumProd(5)
print('somma e prodotto',s,p)
print('somma parziale',somme.summation(3,alpha=2))
