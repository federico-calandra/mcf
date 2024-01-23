import rossi
from numpy import sum as arrsum
# import matplotlib.pyplot as plt
import numpy as np

"""
Questo programma importa il modulo 'rossi.py' ed esegue una simulazione montecarlo della propagazione di uno sciame elettromagnetico in un materiale 

Variabili:
N : int
    numero di simulazioni da eseguire
s : float
    passo della simulazione, in frazione di X0
Q : int
    carica della particella incidente, 0 (fotone), -1 (elettrone) oppure 1 (positrone)
E0 : float
    energia in MeV della particella incidente
mat : Material
    materiale in cui lo sciame si propaga
is_det : bool
    se True la propagazione non segue la legge probabilistica
sw : Sciame
    sciame che si propaga nel materiale
sw_mask : list
    lista di bool che identifica quali particelle dello sciame interagiscono nello step
n_step : int
    numero totale degli step eseguiti
en_ion : list
    elenco delle energie cedute dalle particelle in ogni step
n_part : list
    elenco del numero di particelle dello sciame in ogni step
tot_ion : float
    energia totale ceduta al materiale per ionizzazione
"""        

## CONFIGURAZIONE SIMULAZIONE
N=0
while N<=0:
    N=int(input('numero di simulazioni da eseguire (default 1): \n') or 1)
args=rossi.argp()
s,Q,E0,mat,is_det=rossi.config(args.config_default)
mat.info()
print()

## SIMULAZIONE EVOLUZIONE SCIAME
n_step=[]
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
    n_step.append(sim[0]-1)
    en_ion.append(sim[1])
    n_part.append(sim[2])
    tot_ion.append(arrsum(sim[1]))
    print('n_step =',n_step)
    print('en_ion =',en_ion)
    print('n_part =',n_part)
    print('tot_ion =',tot_ion)  
    
    
## ANALISI RISULTATI
if N==1:
    fig,ax=plt.subplots(1,2,figsize=(13,7))
    ax[0].plot(n_part[0])
    ax_style={'xlabel':'step', 'ylabel':'# di particelle', 'title':'dimensione sciame'}
    ax[0].set(**ax_style)
    ax[1].plot(en_ion[0])
    ax_style={'xlabel':'step', 'ylabel':'energia (MeV)', 'title':'energia ceduta nello step'}
    ax[1].set(**ax_style)
    plt.show()

else:
    pass
    # if energy_step=='False': # N simulazioni con la stessa energia
    #     pass
    # else: # N simulazioni con energia a crescere
    #     pass
    
# breakpoint()
