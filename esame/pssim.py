"""
Questo programma importa il modulo 'rossi.py' ed esegue una simulazione montecarlo della propagazione di uno sciame elettromagnetico in un materiale.

Variabili:
start_time : str
    istante di inizio della simulazione, il formato è 'yyyy_mm_dd--hh_mm_ss'
df : pandas.core.frame.DataFrame
    dataframe contenente i risultati delle simulazioni
fit_n_iter : pandas.core.series.Series
    valori del numero di iterazioni secondo il fit ai minimi quadrati
fit_tot_ion : pandas.core.series.Series
    valori dell'energia totale di ionizzazione secondo il fit ai minimi quadrati
stat_n_iter : list
    media e deviazione standard del numero di iterazioni, nel caso N=1
stat_depth : list
    media e deviazione standard della profondità dello sciame, nel caso N=1
stat_tot_ion : list
    media e deviazione standard dell'energia totale di ionizzazione, nel caso N=1
chi2_depth : float
    valore del chi² per il fit della profondità dello sciame
chi2_tot_ion : float
    valore del chi² per il fit dell'energia totale di ionizzazione
"""

import rossi
import matplotlib.pyplot as plt
import numpy as np
from time import strftime
from pandas import DataFrame
from scipy import optimize

def evolve(s,Q,E0,mat,is_det,N):
    """
    Wrapper per la funzione rossi.evolve che esegue un numero di simulazioni specificato dall'utente.

    Argomenti:
    s : float
        passo della simulazione, in frazione di X0
    Q : int
        carica della particella
    E0 : float
        energia in MeV della particella
    mat : Material
        materiale in cui lo sciame si propaga
    is_det : bool
        se True la simulazione non segue le leggi probabilistiche
    N : int
        numero di simulazioni da eseguire

    Restituisce:
    n_iter : numpy.ndarray
        numero di iterazioni per ogni simulazione
    en_ion= : numpy.ndarray
        energia ceduta in ogni step, per ogni simulazione
    n_part : numpy.ndarray
        numero di particelle in ogni step, per ogni simulazione
    tot_ion : numpy.ndarray
        energia di ionizzaione totale, per ogni simulazione
    """
    
    n_iter=np.array([],dtype=int)
    en_ion=np.array([])
    n_part=np.array([])
    tot_ion=np.array([]) 

    for i in range(0,N):
        sw=rossi.Shower([rossi.Particle(Q,E0)])
        sw_mask=[True]

        if i%10==0:
            print('N = ',i+1)
        sim=rossi.evolve(s,sw,sw_mask,mat,is_det)
        
        n_iter=np.append(n_iter,sim[0])
        n_part=np.append(n_part,sim[1])
        en_ion=np.append(en_ion,sim[2])
        tot_ion=np.append(tot_ion,np.sum(sim[2]))
        
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
    df=DataFrame(columns=['E0','n_iter','sigma_n_iter','depth','sigma_depth','tot_ion','sigma_tot_ion'])
    df['E0']=np.linspace(0,E0,num=11)[1:]
    
    start_time=strftime("%Y_%m_%d--%H_%M_%S")
    for e0,i in zip(df['E0'],df['E0'].index):
        print('E0 =',e0,"MeV")
        n_iter,tot_ion=evolve(s,Q,e0,mat,is_det,100)
        
        df.at[i,'n_iter']=np.mean(n_iter)
        df.at[i,'sigma_n_iter']=np.std(n_iter)
        df.at[i,'depth']=mat.X0*s*np.mean(n_iter)
        df.at[i,'sigma_depth']=mat.X0*s*np.std(n_iter)
        df.at[i,'tot_ion']=np.mean(tot_ion)
        df.at[i,'sigma_tot_ion']=np.std(tot_ion)
    
    print()    
    print(df)
    print()
    df.to_csv(start_time+'.csv',index=False)

    # FIT LINEARE
    def fit_func(x,a,b):
        ''' Funzione per il fit ai minimi quadrati. '''
        return a*x+b
    
    p_guess=[0.1,0]
    p_opt,cov=optimize.curve_fit(fit_func,df['E0'],df['depth'],p_guess,sigma=(df['sigma_depth'] if is_det!=True else None),absolute_sigma=True)
    fit_depth=[fit_func(df['E0'],p_opt[0],p_opt[1]),
                fit_func(df['E0'],p_opt[0]-np.sqrt(cov[0][0]),p_opt[1]-np.sqrt(cov[1][1])), 
                fit_func(df['E0'],p_opt[0]+np.sqrt(cov[0][0]),p_opt[1]+np.sqrt(cov[1][1]))]
    
    p_guess=[1,0]
    p_opt,cov=optimize.curve_fit(fit_func,df['E0'],df['tot_ion'],p_guess,sigma=(df['sigma_tot_ion'] if is_det!=True else None),absolute_sigma=True)
    fit_tot_ion=fit_func(df['E0'],p_opt[0],p_opt[1])
    
    chi2_depth=np.sum((df['n_iter']-fit_depth[0])**2/df['sigma_depth']**2)
    chi2_tot_ion=np.sum((df['tot_ion']-fit_tot_ion)**2/df['sigma_tot_ion']**2)
    print('X² n_iter =',chi2_depth)
    print('X² tot_ion =',chi2_tot_ion)
    
    # GRAFICI
    fig,ax=plt.subplots(1,2,figsize=(13,7))
    fig.suptitle('Q='+str(Q)+', E0='+str(E0)+' MeV, step='+str(s))
    
    ax[0].errorbar(df['E0'], df['depth'], yerr=df['sigma_depth'], fmt='o', color='xkcd:crimson', label='dati')
    ax[0].plot(df['E0'],fit_depth[0],color='xkcd:teal',label='fit')
    ax[0].plot(df['E0'],fit_depth[1],':',color='xkcd:teal',label='incertezza fit')
    ax[0].plot(df['E0'],fit_depth[2],':',color='xkcd:teal')
    ax_style={'xlabel':'energia particella incidente (MeV)', 'ylabel':'profondità (cm)', 'title':'Profondità dello sciame, chi²='+str(np.round(chi2_depth,2))}
    ax[0].set(**ax_style)
    ax[0].grid(axis='y')
    ax[0].legend()
    
    ax[1].errorbar(df['E0'], df['tot_ion'], yerr=df['sigma_tot_ion'], fmt='o', color='xkcd:crimson', label='dati')
    ax[1].plot(df['E0'],fit_tot_ion,color='xkcd:teal',label='fit')
    ax_style={'xlabel':'energia particella incidente (MeV)', 'ylabel':'energia (MeV)', 'title':'Energia totale depositata per ionizzazione, chi²='+str(np.round(chi2_tot_ion,2))}
    ax[1].set(**ax_style)
    ax[1].grid(axis='y')
    ax[1].legend()    
    
    plt.show()
    
else: # N simulazioni con la stessa E0
    N=0
    while N<=0:
        N=int(input('Numero di simulazioni da eseguire (default 1): \n') or 1)

    if N==1:
        n_iter,n_part,en_ion,tot_ion=evolve(s,Q,E0,mat,is_det,N)
        
        fig,ax=plt.subplots(1,2,figsize=(13,7))
        fig.suptitle('Particella Q='+str(Q)+', E0='+str(E0)+' MeV, step='+str(s))
        
        ax[0].plot(range(1,n_iter[0]+1),n_part,color='xkcd:crimson')
        ax_style={'xlabel':'step', 'ylabel':'# di particelle', 'title':'Dimensione sciame','xticks':range(1,n_iter[0]+1)}
        ax[0].set(**ax_style)

        ax[0].grid(axis='y')
        
        ax[1].plot(range(1,n_iter[0]+1),en_ion,color='xkcd:crimson')
        ax_style={'xlabel':'step', 'ylabel':'energia (MeV)', 'title':'Energia ceduta nello step','xticks':range(1,n_iter[0]+1)}
        ax[1].set(**ax_style)
        ax[1].grid(axis='y')
        
    else:
        n_iter,tot_ion=evolve(s,Q,E0,mat,is_det,N)
        print()
    
        stat_n_iter=[np.round(np.mean(n_iter),0),np.round(np.std(n_iter),0)]
        stat_depth=[mat.X0*s*np.round(np.mean(n_iter),0),mat.X0*s*np.round(np.std(n_iter),0)]
        stat_tot_ion=[np.mean(tot_ion),np.std(tot_ion)]
        print('n_iter = {} ± {}'.format(stat_n_iter[0],stat_n_iter[1]))
        print('depth = {} ± {} cm'.format(stat_depth[0],stat_depth[1]))
        print('tot_ion = {} ± {} MeV'.format(stat_tot_ion[0],stat_tot_ion[1]))
        
        fig,ax=plt.subplots(1,2,figsize=(13,7))
        fig.suptitle('Particella Q='+str(Q)+', E0='+str(E0)+' MeV, step='+str(s))
        
        ax[0].plot(range(1,N+1),mat.X0*s*n_iter,'.',color='xkcd:crimson',label='dati')
        ax[0].hlines(stat_depth[0],0,N+1,color='xkcd:teal',label='valore medio')
        ax_style={'xlabel':'N simulazione', 'ylabel':'Profondià (cm)', 'title':'Profondità dello sciame','ylim':(0,None)}
        ax[0].set(**ax_style)
        ax[0].legend(loc='lower left')
        
        ax[1].plot(range(1,N+1),tot_ion,'.',color='xkcd:crimson',label='dati')
        ax[1].hlines(stat_tot_ion[0],0,N+1,color='xkcd:teal',label='valore medio')
        ax_style={'xlabel':'N simulazione', 'ylabel':'Energia (MeV)', 'title':'Energia di ionizzazione','ylim':(0,E0)}
        ax[1].set(**ax_style)
        ax[1].legend(loc='lower left')
        
    plt.show()

# breakpoint()
