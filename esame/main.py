import rossi
import numpy as np

""" Questo programma esegue una simulazione montecarlo della propagazione di uno sciame elettromagnetico in un materiale """

## CONFIGURAZIONE SIMULAZIONE
s,Q,E0,is_det=rossi.config()
N=int(input('numero di simulazioni da eseguire (default 5): ') or 5)
args=rossi.argp()

## SIMULAZIONE EVOLUZIONE SCIAME
en_ion=[]
n_part=[]

for i in range(1,N+1):
    print('*** SIMULAZIONE ***')
    print('N = '+str(i))
    sw=rossi.Swarm([rossi.Particle(Q,E0)])
    sw_mask=[True]
    sw.info()
    print()
    
    if args.material=='h2o':
        mat=rossi.Material('h2o')
    elif args.material=='pbwo4':
        mat=rossi.Material('pbwo4')
    else:
        mat=rossi.Material('test')
    
    res=rossi.evolve(mat,sw,sw_mask,is_det,s)
    
    en_ion.append(res[0])
    n_part.append(res[1])
    
# breakpoint()
