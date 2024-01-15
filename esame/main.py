import rossi
from numpy import sum as arrsum

import matplotlib.pyplot as plt
import numpy as np

"""
Questo programma esegue una simulazione montecarlo della propagazione di uno sciame elettromagnetico in un materiale 

Variabili:
N : int
    numero di simulazioni da eseguire
en_ion: list
    elenco delle energia cedute al materiale ad ogni step
n_part : list
    elenco del numero di particelle dello sciame ad ogni step
mat : Material
    materiale in cui lo sciame si propaga
Q : int
    carica della particella incidente, può essere 0 (fotone), -1 (elettrone) oppure 1 (positrone)
E0 : float
    energia in MeV della particella incidente
sw : Sciame
    sciame che si propaga nel materiale
sw_mask : list
    lista di bool che identifica quali particelle dello sciame hanno abbastanza energia per interagire con il materiale
is_deterministic : bool
    se True la propagazione non segue la legge probabilistica
"""        

## CONFIGURAZIONE SIMULAZIONE
s,Q,E0,is_det=rossi.config()
N=int(input('numero di simulazioni da eseguire (default 1): ') or 1)
args=rossi.argp()

## SIMULAZIONE EVOLUZIONE SCIAME
en_ion=[]
n_part=[]
tot_ion=[]

for i in range(1,N+1):
    print('********** SIMULAZIONE **********')
    print('N = '+str(i))
    sw=rossi.Swarm([rossi.Particle(Q,E0)])
    sw_mask=[True]
    sw.info()
    print()
    
    if args.material=='h2o':
        mat=rossi.Material('h2o')
    elif args.material=='pbwo4':
        mat=rossi.Material('pbwo4')
    if args.material=='test':
        mat=rossi.Material('test')
    else:
        mat=rossi.Material('test')
    
    sim=rossi.evolve(mat,sw,sw_mask,is_det,s)
    
    en_ion.append(sim[0])
    n_part.append(sim[1])
    tot_ion.append(arrsum(sim[0]))
    print('********************')
    
###################################  TO DO
if N==1:
    print('tot_ion =',tot_ion)
    fig,ax=plt.subplots(1,2,figsize=(13,7))
    ax[0].plot(n_part[0])
    ax_style={'xlabel':'step', 'ylabel':'# di particelle', 'title':'dimensione sciame'}
    ax[0].set(**ax_style)
    ax[1].plot(en_ion[0])
    ax_style={'xlabel':'step', 'ylabel':'energia (MeV)', 'title':'energia persa per ionizzazione durante lo step'}
    ax[1].set(**ax_style)
    
else:
    pass
        
plt.show()
    
# breakpoint()
