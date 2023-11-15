"""
Creare uno script python che:
legga il file vel_vs_time.csv scaricato;
produca un grafico della velocità in funzione del tempo;
calcoli la distanza percorsa in funzione del tempo (utilizzando scipy.integrate.simpson);
produca il grafico della distanza percorsa in funzione del tempo.
utilizzare il modulo argparse per permettere di selezionare il garfico da visualizzare o il file da leggere al momento dell'esecuzione.
SUGGERIMENTO: assicurarsi di comprendere bene il comportamento ella funzione scipy.integrate.simpson agli estremi dell'intervallo di integrazione.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simpson
import argparse

def argp():
    parser=argparse.ArgumentParser()
    parser.add_argument('-p', '--plot', action='store')
    return  parser.parse_args()

args=argp()


df_data=pd.read_csv('vel_vs_time.csv')

if args.plot=='v':
    plt.plot(df_data['t'], df_data['v'])
    plt.xlabel('tempo (s)')
    plt.ylabel('velocità (m/s)')
    plt.show()

if args.plot=='s':
    # differenze tra i tempi di campionamenti successivi, prendo la media
    diff=np.empty(0)
    for i in range(len(df_data['t'])-1):
        diff=np.append(diff,df_data['t'][i+1]-df_data['t'][i])

    dt=np.round(np.mean(diff),3)
    print('passo di integrazione:', dt)

    s=np.empty(0)
    for i in range(1,len(df_data['t'])+1):
        y=df_data.iloc[0:i]['v']
        ss=simpson(y, dx=dt)
        s=np.append(s,ss)

    plt.plot(df_data['t'],s)
    plt.xlabel('tempo (s)')
    plt.ylabel('spazio percorso m')
    plt.show()
