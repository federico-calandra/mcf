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

## INPUT CSV
data={}
data['sample1']=pd.read_csv('dati/data_sample1.csv')
data['sample2']=pd.read_csv('dati/data_sample2.csv')
data['sample3']=pd.read_csv('dati/data_sample3.csv')
# breakpoint()


# fig,axs=plt.subplots(1,3)
fft_data={}     # saranno dict di nparray
fft_freqs={}
# rfft_data={}     # saranno dict di nparray
# rfft_freqs={}

# stima parametro
def func(f,beta,a):
    return a/f**beta

for s in ['sample1', 'sample2', 'sample3']:
    plt.plot(data[s]['time'],data[s]['meas'])
    plt.title(s)
    plt.xlabel('time (s)')
    plt.show()
    
    # fft reale
    seq=data[s]['meas'].values
    fft_data[s] = fft.rfft(seq)
    fft_freqs[s] = 0.5 * fft.rfftfreq(len(data[s]['meas']), d=1)
    pwsp=np.abs(fft_data[s])**2
    
    # grafico spettro
    plt.loglog(fft_freqs[s][1:len(pwsp)//2], pwsp[1:len(pwsp)//2])
    plt.title('power spectre '+s)
    # plt.show()
    # breakpoint()
    
    # fit
    p_guess=[1,1]
    x=fft_freqs[s]
    p_opt,cov=optimize.curve_fit(func, x[1:len(pwsp)//2], pwsp[1:len(pwsp)//2], p0=p_guess) #,sigma=err_y,absolute_sigma=True)
    
    fit=func(x,p_opt[0],p_opt[1])
    plt.plot(x,fit)

    plt.show()
    # breakpoint()
    
    
    # ax_prop=[{'xlabel':'mass', 'ylabel':'# of occurences', 'title':'histogram of all events'},
    #          {'xlabel':'mass', 'title':'histogram'},    #..., 
    #          {'xlabel':'massN', 'title':'histogramN'}]
    # for key,ax in enumerate(axs.flat):
    #     ax.set(**ax_prop[key])

    ###  fft complessa
    # # # # # # # # spettro pot
    # # # # # # # plt.plot(fft_freqs[s],fft_data[s])
    # # # # # # # print(len(data[s]['meas'])//2)  # 2048
    # # # # # # # print(fft_freqs[s][:len(data[s]['meas'])//2])
    # # # # # # # # breakpoint()
    # # # # # # # # axs[1].plot(data[s]['time'],data[s]['meas'])
    # # # # # # # # axs[2].plot(data[s]['time'],data[s]['meas'])
    # # # # # # # plt.show()

# ## scarto e chi²
# y_fit1=gauss1(x,p_opt[0],p_opt[1],p_opt[2],p_opt[3],p_opt[4])
# delta_y=y-y_fit1
# chi2=np.sum(delta_y**2/y)
# print('X² =', chi2)
# 
# ## confronto grafico
# fig,axs=plt.subplots(2)
# axs[0].hist(mc2,range=(8,11),bins=100)
# axs[0].plot(x,y_fit1)
# axs[1].plot(x,delta_y)


breakpoint()
