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
from scipy import fft
import my

def stylePlot(Xdata, Ydata, style=None):     # data,style sono dict
    fig,ax=plt.subplots(figsize=(10,8))
    ax.plot(Xdata,Ydata)
    if style!=None:
        ax.set(**style)
    return fig,ax

# leggi csv
data=pd.read_csv('dati/copernicus_PG_selected.csv')
c=data.columns  # col1=tempo  col2=concentrazione CO₂

# grafico temporale
ax_style={'xlabel':'day', 'ylabel':'CO', 'title':''}
stylePlot(data[c[1]], data[c[2]], ax_style)
plt.show()

# fft
fft_data={}
fft_freqs={}
pwsp={}

breakpoint()

seq=data[c[2]].values
fft_data = fft.rfft(seq)
fft_freqs = 0.5 * fft.rfftfreq(len(data[c[2]])) #, d=1) ?????
pwsp=np.abs(fft_data)**2

fig2,ax2=plt.subplots(figsize=(10,8))
ax2.plot(data[c[1]], data[c[2]])
# ax_style={'xlabel':'day', 'ylabel':'CO', 'title':''}
# ax1.set(**ax_style)
plt.show()

# 6 grafici delle sorgenti
fig2,ax2=plt.subplots(2,3,figsize=(10,8))
ax2=ax2.flatten()


for i,df in data.items():
    ax2[i].plot(df[c[1]], df[c[3]])
    ax2[i].set(**ax_style[i])

# spettri di potenza
fig3,ax3=plt.subplots(figsize=(10,8))
ax_style={'xlabel':'??', 'ylabel':'???', 'title':'spettri potenza'}

for i in range(len(fft_data)):  # len(fft_data)=6
    ax3.loglog(fft_freqs[i][1:len(pwsp[i])//2], pwsp[i][1:len(pwsp[i])//2])
    ax3.set(**ax_style)

plt.show()

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
