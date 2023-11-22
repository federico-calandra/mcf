"""
Il file `oscilloscope.csv`  precedentemente scaricato e contiene il sgenale di due canali di un oscilloscopio.
Creare uno script python che:
1. legga il file di dati;
2. produca il grafico dei segnali dell'oscilloscopio;
3. calcoli la derivata del segnale attraverso la differenza centrale;
4. produca il grafico della derivata calcolata;
5. OPZIONALE: ricavarere posizione e valore dei minimi dei segnali;
6. OPZIONALE: trovare le coincidenze fra i due segnali; 
7. OPZIONALE: stimare l'efficienza dei due canali dell'oscilloscopio;
SUGGERIMENTO: per il calclo della differenza centrale definire una funzione;
SUGGERIMENTO: per la differenza centrale provare più valori di n ed individuare quello più adatto ai dati.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def cdiff(x,y):
    Dy = np.empty(0)
    for i in range(1,len(x)-1):
        Dy = np.append(Dy,(y[i+1] - y[i-1]) / (x[i+1] - x[i-1]))
    return Dy

df_data=pd.read_csv('oscilloscope.csv')

D_sig1=cdiff(df_data['time'],df_data['signal1'])
D_sig2=cdiff(df_data['time'],df_data['signal2'])

plt.plot(df_data['time'], df_data['signal1'], label='sig1')
plt.plot(df_data['time'].iloc[1:-1], D_sig1, label='D(sig1)')
plt.legend()
plt.show()

plt.plot(df_data['time'], df_data['signal2'], label='sig2')
plt.plot(df_data['time'].iloc[1:-1], D_sig2, label='D(sig2)')
plt.legend()
plt.show()
