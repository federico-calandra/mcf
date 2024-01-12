import sciame
import argparse
from itertools import compress

"""
Questo programma simula la propagazione di uno sciame elettromagnetico secondo un modello derivato da quello di Rossi.

Variabili:
mat : sciame.Material
    materiale in cui lo sciame si propaga
Q : int
    carica della particella incidente, può essere 0 (fotone), -1 (elettrone) oppure 1 (positrone)
E0 : float
    energia in MeV della particella incidente
sw : sciame.Sciame
    sciame che si propaga nel materiale
sw_mask : list
    lista di bool che identifica quali particelle dello sciame hanno abbastanza energia per interagire con il materiale
is_deterministic : bool
    se True la propagazione non segue la legge probabilistica
n_part : list
    elenco del numero di particelle dello sciame ad ogni step
"""

def argp():
    """ Inizializza il parser degli argomenti. """
    parser=argparse.ArgumentParser()
    # parser.add_argument('material', choices=['h2o','pbwo4','test'], nargs='?', default='test')
    # parser.add_argument('particle', nargs='?', default='-1,500')
    parser.add_argument('-m','--material')
    parser.add_argument('-d', '--is-deterministic', action='store_true')
    return  parser.parse_args()


## CONFIGURAZIONE
args=argp()

# materiale
if args.material=='h2o':
    mat=sciame.Material('h2o')
elif args.material=='pbwo4':
    mat=sciame.Material('pbwo4')
else:
    mat=sciame.Material('test')
    
# particella
Q=int(input('carica della particella (default -1): ') or -1)
E0=float(input('energia in MeV della particella  (default 1000): ') or 1000)
sw=sciame.Swarm([sciame.Particle(Q,E0)])
sw_mask=[True]
sw.info()
print()

is_deterministic=args.is_deterministic # evoluzione deterministica

# elenco delle energie e num di aprticelle
en_ion=[]
n_part=[]


### EVOLUZIONE SCIAME
n=1
while True in sw_mask:
    # PROPAGAZIONE
    en_ion.append(sw.propagate(mat,sw_mask,is_deterministic))
    n_part.append(len(sw))
    # sw.info() # le particelle con E < Ec cedono energia ma saranno escluse dallo sciame
    
    # escludere particelle che non hanno abbastanza energia
    sw=sciame.Swarm(compress(sw,sw_mask))
    # sw.info() # queste particelle sono quelle che interagiscono
    
    # INTERAZIONE
    sw=sw.interact(is_deterministic)
    sw.info() # risultato dell'interazione
    print('n step = '+str(n)+'\n')
    
    if len(sw)!=0:
        sw_mask=[True]*len(sw)
        n+=1
    else:
        print('Non ci sono più particelle che possono interagire.')
        print()

# breakpoint()
