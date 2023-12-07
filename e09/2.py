"""
Realizzare uno script python che:
Legga i tre file messi a disposizione;
Produca un grafico dei tre segnali di ingresso;
Calcoli la trasformata di Fourier dei segnali di ingreso e produca il grafico dello spettro di potenza;
Faccia il fit dei tre spettri di potenza per determinarne l'andamento in funzione della frequenza e identifichi il tipo di rumore per ogni serie di dati.
Confronti i tre spettri di potenza e i relativi fit
Interpretare i risultati conforntando i tre spettri di potenza assieme ai segnali.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import fft, optimize   

# leggi csv
source=['4FGL_J0721.9+7120_weekly_9_15_2023_mcf.csv',
       '4FGL_J0721.9+7120_weekly_9_15_2023_mcf.csv',
       '4FGL_J1256.1-0547_weekly_9_15_2023_mcf.csv',
       '4FGL_J2202.7+4216_weekly_9_15_2023_mcf.csv',
       '4FGL_J2232.6+1143_weekly_9_15_2023_mcf.csv',
       '4FGL_J2253.9+1609_weekly_9_15_2023_mcf.csv']

data={}
for i,s in zip(range(len(source)),source):
    data[i]=pd.read_csv('dati/'+s)
    # print('len(data)=',len(data[i]))
    c=data[i].columns
print(data)
# breakpoint()

# # # ## GRAFICI
# # # # axs1=plt.axes()
# # # # fig,axs=plt.subplots(2,3)
# # # # axs=axs.reshape(6)
# # # 
# # # # for i,f in zip(range(len(fnames)),fnames):
# # # #     breakpoint()
# # # #     plt.plot( source_data[i][c[1]], source_data[i][c[3]] )
# # # #     axs1.plot( source_data[i][c[1]], source_data[i][c[3]])
# # # #     axs[i].plot( source_data[i][c[1]], source_data[i][c[3]])
# # # # plt.show()
# breakpoint()

# fft
fft_data={}     # saranno dict di nparray
fft_freqs={}
pwsp={}
for i,df in data.items():
    seq=df[c[3]].values
    fft_data[i] = fft.rfft(seq)
    fft_freqs[i] = 0.5 * fft.rfftfreq(len(df[c[3]])) #, d=1) ?????
    pwsp[i]=np.abs(fft_data[i])**2
print(fft_data)
print(fft_freqs)
print(pwsp)
breakpoint()


# #     # grafico spettro
# #     plt.loglog(fft_freqs[s][1:len(pwsp)//2], pwsp[1:len(pwsp)//2])
# #     plt.title('power spectre '+s)
# #     # plt.show()
# #     # breakpoint()
# #     
# #     # fit  # provare a togliere i primi n campioni
# #     p_guess=[1,1]
# #     x=fft_freqs[s]
# #     p_opt,cov=optimize.curve_fit(func, x[1:len(pwsp)//2], pwsp[1:len(pwsp)//2], p0=p_guess) #,sigma=err_y,absolute_sigma=True)
# #     
# #     fit=func(x,p_opt[0],p_opt[1])
# #     plt.plot(x,fit)
# # 
# #     plt.show()


breakpoint()
