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

Q : int
    carica della particella incidente, può essere 0 (fotone), -1 (elettrone) oppure 1 (positrone)
E0 : float
    energia in MeV della particella incidente

"""        

## CONFIGURAZIONE SIMULAZIONE
N=int(input('numero di simulazioni da eseguire (default 1): \n') or 1)
s,(Q,E0),mat,is_det=rossi.config()

## SIMULAZIONE EVOLUZIONE SCIAME
en_ion=[]
n_part=[]
tot_ion=[]

for i in range(1,N+1):
    sw=rossi.Swarm([rossi.Particle(Q,E0)])
    sw_mask=[True]
    sw.info()
    print()

    print('********** SIMULAZIONE **********')
    print('N = '+str(i))
    sim=rossi.evolve(s,sw,sw_mask,mat,is_det)
    
    en_ion.append(sim[0])
    n_part.append(sim[1])
    tot_ion.append(arrsum(sim[0]))
    print('en_ion =',en_ion)
    print('n_part =',n_part)
    print('tot_ion =',tot_ion)  
    
    
    
# # # if N==1:
# # #     print('tot_ion =',tot_ion)
# # #     fig,ax=plt.subplots(1,2,figsize=(13,7))
# # #     ax[0].plot(n_part[0])
# # #     ax_style={'xlabel':'step', 'ylabel':'# di particelle', 'title':'dimensione sciame'}
# # #     ax[0].set(**ax_style)
# # #     ax[1].plot(en_ion[0])
# # #     ax_style={'xlabel':'step', 'ylabel':'energia (MeV)', 'title':'energia persa per ionizzazione durante lo step'}
# # #     ax[1].set(**ax_style)
# # # else:
# # #     pass
# # #         
# # # plt.show()
    
# breakpoint()
