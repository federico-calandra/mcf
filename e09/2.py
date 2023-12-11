"""
Produrre uno script python che:
Legga i file di dati e generi un DataFrame pandas per ciascuno di essi;
Generi un grafico di tutte le curve di luce (Flusso vs Giorno Giuliano) sovrapposte con una legenda che identifichi le sorgenti;
Generi un unico grafico con 6 pannelli sovrapposti, in ogni pannello deve comparire la curva di luce di una sorgente (Usare due colori diversi per BLL e FSRQ);

SUGGERIMENTO: per ottimizzare la scrittura del codice, provare ad usare un dictionary per immagazzinare le informazioni sulle diverse sorgenti in modo da sfruttare i cicli for per le diverse operazioni.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import fft
import my

## LEGGI CSV
source=['4FGL_J0721.9+7120_weekly_9_15_2023_mcf.csv',
       '4FGL_J0721.9+7120_weekly_9_15_2023_mcf.csv',
       '4FGL_J1256.1-0547_weekly_9_15_2023_mcf.csv',
       '4FGL_J2202.7+4216_weekly_9_15_2023_mcf.csv',
       '4FGL_J2232.6+1143_weekly_9_15_2023_mcf.csv',
       '4FGL_J2253.9+1609_weekly_9_15_2023_mcf.csv']

data={}
for i,s in zip(range(len(source)),source):
    data[i]=pd.read_csv('dati/'+s)
    c=data[i].columns

## GRAFICI CURVE DI LUCE
fig1,ax1=plt.subplots(figsize=(10,7))
fig2,ax2=plt.subplots(2,3,figsize=(10,7),sharex=True)
ax2=ax2.reshape(6)
for i,df in data.items():
    ax1.plot(df[c[1]], df[c[3]], label='sorg'+str(i+1))
    ax2[i].plot(df[c[1]], df[c[3]])
    ax_style={'xlabel':c[1], 'ylabel':c[3], 'title':'sorg'+str(i+1)}
    ax2[i].set(**ax_style)
    
ax_style={'xlabel':c[1], 'ylabel':c[3], 'title':'Curve di luce'}
ax1.set(**ax_style)
ax1.legend()
plt.show()

"""
Calcoli la trasformata di Fourier delle curve di luce;
Generi un grafico con gli spettri di potenza delle diverse sorgenti sovrapposti (Provare anche a raggruppare BLL e FSRQ per colore);
Generi un grafico con gli spettri di potenza delle diverse sorgenti sovrapposti e normalizzati ai rispettivi coefficiente di ordine zero (Raggruppare BLL e FSRQ per colore);
Che significato ha la normalizzazione?
Cosa si può concludere dal risultato?
"""

## CALCOLA FFT
fft_data={}     # dict di nparray
fft_freqs={}
pwsp={}
p3={}        # dict di tuple (fig,ax)

for i,df in data.items():
    dt=df[c[1]][1]-df[c[1]][0]
    seq=df[c[3]].values
    fft_data[i], fft_freqs[i], pwsp[i], p3[i]=my.fourier(seq)
    
# # # ## GRAFICI SPETTRI DI POTENZA
# # # fig3,ax1=plt.subplots(figsize=(10,7))
# # # # fig2,ax2=plt.subplots(2,3,figsize=(10,7),sharex=True)
# # # # ax2=ax2.reshape(6)
# # # for i,df in data.items():
# # #     ax1.plot(df[c[1]], df[c[3]], label='sorg'+str(i+1))
# # #     # ax2[i].plot(df[c[1]], df[c[3]])
# # #     # ax_style={'xlabel':c[1], 'ylabel':c[3], 'title':'sorg'+str(i+1)}
# # #     # ax2[i].set(**ax_style)

breakpoint()
