"""
Passo 3:
Creare uno script python che svolga le seguenti operazioni:
Importi il modulo reco;
Legga i file di dati e, per ognuno di essi, produca un array di reco.Hit;
SUGGERIMENTO: creare un funzione da richiamare per ogni file;
Produca un array che corrisponda alla conbinazione, ordinata temporalmente, di tutti i reco.Hit;
Produca un istogramma dei Δt fra reco.Hit consecutivi;
SUGGERIMENTO: valutare l'utilizzo dell' overloading degli operatori + o - (__add__, __sub__)
Come stabilire la finestra temporale da applicare ai Δt che permetta di raggruppare gli Hit dello stesso evento ma separi quelii apparteneti ad eventi differenti?
"""

import reco
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

hit=np.empty(0)

df_data=pd.read_csv('hit_times_M0.csv')
for i,r in df_data.iterrows():
    # r[0] è mod_id
    # r[1] è det_id
    # r[2] è hit_time
    d=reco.Hit(r[0], r[1], r[2])
    hit=np.append(hit,d)

df_data=pd.read_csv('hit_times_M1.csv')
for i,r in df_data.iterrows():
    d=reco.Hit(r[0], r[1], r[2])
    hit=np.append(hit,d)
    
df_data=pd.read_csv('hit_times_M2.csv')
for i,r in df_data.iterrows():
    d=reco.Hit(r[0], r[1], r[2])
    hit=np.append(hit,d)
    
df_data=pd.read_csv('hit_times_M3.csv')
for i,r in df_data.iterrows():
    d=reco.Hit(r[0], r[1], r[2])
    hit=np.append(hit,d)
    
hit=np.sort(hit)
diff=np.empty(0)

for i in range(len(hit)-1):
    diff=np.append(diff,hit[i+1].time-hit[i].time) 
# mask sulle differenze nulle
mask_diff=diff!=0

plt.hist(np.log10(diff[mask_diff]),bins=100)
plt.xlabel('log10(Δhit_time)')
plt.ylabel('# of occurrences')
plt.yscale('log')
plt.show()
