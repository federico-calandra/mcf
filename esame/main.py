import rossi
import numpy as np

""" Questo programma esegue una simulazione montecarlo della propagazione di uno sciame elettromagnetico in un materiale """

## CONFIGURAZIONE SIMULAZIONE
args=rossi.argp()

N=int(input('numero di simulazioni da eseguire (default 5): ') or 5)

# particella
Q=int(input('carica della particella (default -1): ') or -1)
E0=float(input('energia in MeV della particella  (default 1000): ') or 1000)

# evoluzione deterministica
is_deterministic=args.is_deterministic


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
    
    res=rossi.evolve(mat,sw,sw_mask,is_deterministic)
    
    en_ion.append(res[0])
    n_part.append(res[1])
    
breakpoint()
