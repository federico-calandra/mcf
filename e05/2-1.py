import pandas as pd
import matplotlib.pyplot as plt
from numpy import log10,abs
import numpy as np

'''
Passo 1:
Creare uno script python che esegua le seguenti operazioni:
Legga uno o più file di input;
Produca un istogramma dei tempi per uno dei moduli (file);
Produca un istogramma delle differenze di tempi (
) fra Hit consecutivi per uno dei moduli;
SUGGERIMENTO: usare il log_10(delta t);
Interpretare il grafico risultante.
'''

df_data=pd.read_csv('hit_times_M0.csv')

plt.hist(log10(df_data['hit_time']),bins=100)
plt.xlabel('log10(hit_time)')
plt.ylabel('# of occurrences')
plt.show()

diff=np.empty(0)
for i in range(len(df_data['hit_time'])-1):
    diff=np.append(diff,df_data['hit_time'][i+1]-df_data['hit_time'][i]) 
# mask sulle differenze nulle
mask_diff=diff!=0

plt.hist(log10(diff[mask_diff]),bins=100)
plt.xlabel('log10(Δhit_time)')
plt.ylabel('# of occurrences')
plt.show()

