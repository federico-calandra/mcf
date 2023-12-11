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
import my

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import fft, optimize   

## LEGGI CSV
data={}
data['sample1']=pd.read_csv('dati/data_sample1.csv')
data['sample2']=pd.read_csv('dati/data_sample2.csv')
data['sample3']=pd.read_csv('dati/data_sample3.csv')

fft_data={}     # sono dict di nparray
fft_freqs={}

## FUNZIONE PER FIT
def func(f,beta,a):
    return a/f**beta

for s in ['sample1', 'sample2', 'sample3']:
    ## GRAFICO TEMPORALE
    fig1,ax1=plt.subplots()
    ax1.plot(data[s]['time'],data[s]['meas'])
    ax_style={'xlabel':'time (s)', 'ylabel':'amplitude', 'title':s}
    ax1.set(**ax_style)
    plt.show()
    
    # FFT REALE
    seq=data[s]['meas'].values
    fft_data[s] = fft.rfft(seq)
    fft_freqs[s] = 0.5 * fft.rfftfreq(len(data[s]['meas']), d=1)
    pwsp=np.absolute(fft_data[s])**2
    
    # GRAFICI SPETTRO
    fig2,ax2=plt.subplots(1,3)
    ax2[0].plot(fft_freqs[s][:len(pwsp)//2], pwsp[:len(pwsp)//2])
    ax2[1].semilogy(fft_freqs[s][:len(pwsp)//2], pwsp[:len(pwsp)//2])
    ax2[2].loglog(fft_freqs[s][:len(pwsp)//2], pwsp[:len(pwsp)//2],'.')
    ax_style=[{'xlabel':'frequency (1/s)', 'ylabel':'absolute value of coefficient'},
              {'xlabel':'frequency (1/s)', 'ylabel':'ln(absolute value of coefficient)'},
              {'xlabel':'ln(frequency)', 'ylabel':'ln(absolute value of coefficient)'}]
    ax2[0].set(**ax_style[0])
    ax2[1].set(**ax_style[1])
    ax2[2].set(**ax_style[2])
    plt.show()
    
    ## FIT
    p_guess=[1,1]
    x=fft_freqs[s]
    p_opt,cov=optimize.curve_fit(func, x[1:len(pwsp)//2], pwsp[1:len(pwsp)//2], p0=p_guess)
    fit=func(x,p_opt[0],p_opt[1])
    plt.plot(x,fit)
    plt.show()
