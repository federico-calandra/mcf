"""
Questo programma importa il modulo 'rossi.py' ed esegue una simulazione montecarlo della propagazione di uno sciame elettromagnetico in un materiale.

Variabili:
n_iter : list
    
en_ion= : list
    
n_part : list
    
tot_ion : list
    
mean_n_iter : numpy.ndarray
    valori medi del numero di step
dev_n_iter : numpy.ndarray
    deviazioni standard del numeo di step
mean_tot_ion : numpy.ndarray
    valori medi dell'energia ceduta al materiale
dev_tot_ion : numpy.ndarray
    deviazioni standard dell'energia ceduta al materiale
E0span : numpy.ndarray
    array delle energie della particella incidente
start_time : str
    istante di inizio della simulazione
"""

import rossi
import matplotlib.pyplot as plt
import numpy as np
from time import ctime
from pandas import DataFrame
from scipy import optimize

def evolve(s,Q,E0,mat,is_det,N):
    """
    oneline

    Argomenti:
    s
    Q
    E0
    materiale
    is_det
    N

    Restituisce:
    n_iter : list
        numero di iterazioni di ciascuna simulazione
    tot_ion : list
        energia totale ceduta al materiale
    """
    
    n_iter=[]
    en_ion=[]
    n_part=[]
    tot_ion=[]

    for i in range(0,N):
        sw=rossi.Swarm([rossi.Particle(Q,E0)])
        sw_mask=[True]

        if i%10==0:
            print('N = ',i+1)
        sim=rossi.evolve(s,sw,sw_mask,mat,is_det)
        
        n_iter.append(sim[0])
        n_part.append(sim[1])
        en_ion.append(sim[2])
        tot_ion.append(np.sum(sim[2]))
        
    if N==1:
        return n_iter,n_part,en_ion,tot_ion
    else:
        return n_iter,tot_ion


## CONFIGURAZIONE SIMULAZIONE
args=rossi.argp()

s,Q,E0,mat,is_det=rossi.config(args.config_default)
mat.info()
print()

if args.same_energy!=True: # 50 simulazioni per 10 valori nell'intervallo (0,E0]
    df=DataFrame(columns=['E0','n_iter','sigma_n_iter','tot_ion','sigma_tot_ion'])
    df['E0']=np.linspace(0,E0,num=11)[1:]
    
    start_time=ctime()
    for e0,i in zip(df['E0'],df['E0'].index):
        print('E0 =',e0,"MeV")
        n_iter,tot_ion=evolve(s,Q,e0,mat,is_det,100)
        
        df.at[i,'n_iter']=np.mean(n_iter)
        df.at[i,'sigma_n_iter']=np.std(n_iter)
        df.at[i,'tot_ion']=np.mean(tot_ion)
        df.at[i,'sigma_tot_ion']=np.std(tot_ion)
    
    print()    
    print(df)
    print()
    df.to_csv(start_time+'.csv',index=False)

    # FIT LINEARE
    def fit_func(x,a,b):
        return a*x+b
    
    p_guess=[0.1,0]
    p_opt,cov=optimize.curve_fit(fit_func,df['E0'],df['n_iter'],p_guess,sigma=df['sigma_n_iter'],absolute_sigma=True)
    fit_n_iter=[fit_func(df['E0'],p_opt[0],p_opt[1]),
                fit_func(df['E0'],p_opt[0]-np.sqrt(cov[0][0]),p_opt[1]-np.sqrt(cov[1][1])),
                fit_func(df['E0'],p_opt[0]+np.sqrt(cov[0][0]),p_opt[1]+np.sqrt(cov[1][1]))]
    
    p_guess=[1,0]
    p_opt,cov=optimize.curve_fit(fit_func,df['E0'],df['tot_ion'],p_guess,sigma=df['sigma_tot_ion'],absolute_sigma=True)
    fit_tot_ion=fit_func(df['E0'],p_opt[0],p_opt[1])
    
    # GRAFICI
    fig,ax=plt.subplots(1,2,figsize=(13,7))
    
    ax[0].errorbar(df['E0'], df['n_iter'], yerr=df['sigma_n_iter'], fmt='o', color='xkcd:crimson', label='dati')
    ax[0].plot(df['E0'],fit_n_iter[0],color='xkcd:teal',label='fit')
    ax[0].plot(df['E0'],fit_n_iter[1],':',color='xkcd:teal',label='incertezza fit')
    ax[0].plot(df['E0'],fit_n_iter[2],':',color='xkcd:teal')
    ax_style={'xlabel':'energia particella incidente (MeV)', 'ylabel':'distanza (cm)', 'title':'lunghezza di penetrazione nel materiale'}
    ax[0].set(**ax_style)
    ax[0].grid(axis='y')
    ax[0].legend()
    
    ax[1].errorbar(df['E0'], df['tot_ion'], yerr=df['sigma_tot_ion'], fmt='o', color='xkcd:crimson', label='dati')
    ax[1].plot(df['E0'],fit_tot_ion,color='xkcd:teal',label='fit')
    ax_style={'xlabel':'energia particella incidente (MeV)', 'ylabel':'energia (MeV)', 'title':'energia totale depositata per ionizzazione'}
    ax[1].set(**ax_style)
    ax[1].grid(axis='y')
    ax[1].legend()
    
    chi2_n_iter=np.sum((df['n_iter']-fit_n_iter[0])**2/df['sigma_n_iter']**2)
    chi2_tot_ion=np.sum((df['tot_ion']-fit_tot_ion)**2/df['sigma_tot_ion']**2)
    print('X² n_iter =',chi2_n_iter)
    print('X² tot_ion =',chi2_tot_ion)
    
    plt.show()
    
else: # N simulazioni con la stessa E0
    N=0
    while N<=0:
        N=int(input('numero di simulazioni da eseguire (default 1): \n') or 1)

    if N==1:
        n_iter,n_part,en_ion,tot_ion=evolve(s,Q,E0,mat,is_det,N)
        
        fig,ax=plt.subplots(1,2,figsize=(13,7))
        
        ax[0].plot(range(1,n_iter[0]+1),n_part[0],color='xkcd:crimson')
        ax_style={'xlabel':'step', 'ylabel':'# di particelle', 'title':'dimensione sciame','xticks':range(1,n_iter[0]+1)}
        ax[0].set(**ax_style)
        ax[0].grid(axis='y')
        
        ax[1].plot(range(1,n_iter[0]+1),en_ion[0],color='xkcd:crimson')
        ax_style={'xlabel':'step', 'ylabel':'energia (MeV)', 'title':'energia ceduta nello step','xticks':range(1,n_iter[0]+1)}
        ax[1].set(**ax_style)
        ax[1].grid(axis='y')
        
    else:
        n_iter,tot_ion=evolve(s,Q,E0,mat,is_det,N)
        print()
    
        stat_n_iter=[np.round(np.mean(n_iter),0),np.round(np.std(n_iter),0)]
        stat_tot_ion=[np.mean(tot_ion),np.std(tot_ion)]
        print('n_iter = {} ± {}'.format(stat_n_iter[0],stat_n_iter[1]))
        print('tot_ion = {} ± {} MeV'.format(stat_tot_ion[0],stat_tot_ion[1]))
        
        fig,ax=plt.subplots(1,2,figsize=(13,7))
        
        ax[0].plot(range(1,N+1),n_iter,'.',color='xkcd:crimson',label='dati')
        ax[0].hlines(stat_n_iter[0],0,N+1,color='xkcd:teal',label='valore medio')
        ax_style={'xlabel':'N simulazione', 'ylabel':'Iterazioni', 'title':'Numero di iterazioni','ylim':(0,None)}
        ax[0].set(**ax_style)
        ax[0].legend(loc='lower left')
        
        ax[1].plot(range(1,N+1),tot_ion,'.',color='xkcd:crimson',label='dati')
        ax[1].hlines(stat_tot_ion[0],0,N+1,color='xkcd:teal',label='valore medio')
        ax_style={'xlabel':'N simulazione', 'ylabel':'Energia (MeV)', 'title':'Energia di ionizzazione','ylim':(0,E0)}
        ax[1].set(**ax_style)
        ax[1].legend(loc='lower left')
        
    plt.show()

breakpoint()
