import argparse
import random
from itertools import compress
from numpy import exp
from scipy.constants import m_e,c

from numpy import sum as arrsum

"""
Questo programma definisce la classe degli oggetti Particella, Sciame e Materiale e definisce la funzione che simula la propagazione di uno sciame elettromagnetico secondo un modello derivato da quello di Rossi.

Variabili:
s : float
    passo della simulazione, in frazione di X0+
sw : Sciame
    sciame che si propaga nel materiale
Q : int
    carica della particella incidente, può essere 0 (fotone), -1 (elettrone) oppure 1 (positrone)
E0 : float
    energia in MeV della particella incidente
sw_mask : list
    lista di bool che identifica quali particelle dello sciame hanno abbastanza energia per interagire con il materiale
mat : Material
    materiale in cui lo sciame si propaga
is_deterministic : bool
    se True la propagazione non segue la legge probabilistica
en_ion : list
    elenco delle energie cedute dalle particelle in ogni step
n_part : list
    elenco del numero di particelle dello sciame in ogni step
tot_ion : float
    energia totale ceduta al materiale per ionizzazione
"""


class Material():
    """
    Classe che rappresenta il materiale in cui lo sciame si propaga.
    
    Attributi:
    X0 : float
        lunghezza di radiazione in cm
    dE : float
        perdita di energia per ionizzazione, per unità di lunghezza (MeV/cm)
    Ec : float
        energia critica
    en_ion : list
        energia depositata dalle particelle durante lo step

    Metodi:
    __init__ : costruttore della classe
    info : stampa la dimensione e gli attributi delle particelle dello sciame
    """
    
    def __init__(self,name):
        """ 
        Crea il materiale.
        
        Argomenti:
        name : string
            identifica il materiale tra ghiaccio 'h20' e tungstato di piombo 'pbwo4'
        """
        if name=='h2o':
            self.X0=39.31
            self.dE=1.822
            self.Ec=78.6 
        elif name=='pbwo4':
            self.X0=0.89 
            self.dE=10.20
            self.Ec=9.31 
        else:
            self.X0=10
            self.dE=1
            self.Ec=10
    
    def info(self):
        """ Stampa gli attributi del materiale. """
        print('*** Materiale ***')
        print('X0 = {} cm, dE = {} MeV/cm, Ec = {} MeV'.format(self.X0,self.dE,self.Ec))
        # print('energia di ionizzazione = {}'.format())


class Particle():
    """
    Classe che rappresenta una particella dello sciame.
    
    Attributi:
    q : int
        carica della particella, può essere 0 (fotone), -1 (elettrone) oppure 1 (positrone)
    e : float
        energia in MeV della particella
    x : float
        posizione in cm della particella rispetto al punto di ingreso nel materiale

    Metodi:
    __init__ : costruttore della classe
    info : stampa gli attributi della particella
    propagate : calcola la propagazione della particella e la perdita di energia per ionizzazione
    interact : calcola i prodotti dell'interazione della particella con il materiale
    """
    
    def __init__(self, q, e, x=0):
        """
        Crea una particella.
        
        Argomenti:
        q : int
            carica della particella, può essere 0 (fotone), -1 (elettrone) oppure 1 (positrone)
        e : float
            energia in MeV della particella
        x : float
            posizione in cm della particella rispetto al punto di ingreso nel materiale
        """
        self.q=q
        self.e=e
        self.x=x
        
    def info(self):
        """ Stampa gli attributi della particella. """
        print('q = {}, E = {:f} MeV, x = {} cm'.format(self.q, self.e, self.x))
            
    def propagate(self,s,sw_mask,mat,is_det,i):
        """
        Calcola la propagazione della particella e la perdita di energia per ionizzazione.
    
        Argomenti:
        s : float
            passo della simulazione, in frazione di X0
        sw_mask : list
            lista di bool che identifica quali particelle potranno interagire
        mat : Material
            materiale in cui la patricella si propaga
        is_det : bool
            se True la simulazione non segue le leggi probabilistiche
        i : int
            indice della list sw_mask corrispondente alla particella considerata
        
        Restituisce:
        en_ion : float
            energia di ionizzazione ceduta dalla particella al materiale
        """
        
        random.seed()
        if self.q==0: # fotone
            if self.e>2*m_e*c**2: # ha abbastanza energia
                en_ion=0 # si propaga senza perdite
                self.x+=mat.X0*s
            else: # non può propagarsi
                en_ion=(random.uniform(0,self.e) if is_det==False else self.e)
                self.e-=en_ion # cede energia al materiale
                sw_mask[i]=False # viene esclusa dall'interazione
                
        else: # elettrone/positrone
            if self.e>mat.dE*mat.X0*s: # ha abbastanza energia
                en_ion=mat.dE*mat.X0*s
                self.x+=mat.X0*s
                self.e-=en_ion
            else: # non può propagarsi
                en_ion=(random.uniform(0,self.e) if is_det==False else self.e)
                self.e-=en_ion
                sw_mask[i]=False
                
        return en_ion
            
    def interact(self,s,is_det):
        """
        Calcola i prodotti dell'interazione della particella con il materiale.
        
        Argomenti:
        s : float
            passo della simulazione, in frazione di X0
        is_det : bool
            se True la simulazione non segue le leggi probabilistiche
        
        Restituisce:
        prod : list
            lista contenente le particelle prodotte
        """
        
        random.seed()
        if self.q==0:  # fotone
            # probabilità di interazione 1-e^(-s), s=1 ⇒ P=0.56
            rnd=random.uniform(0,1)
            if rnd>=(1-exp(-s) if is_det==False else 0):
                p1=Particle(1,self.e/2,self.x)
                p2=Particle(-1,self.e/2,self.x)
                prod=[p1,p2]
            else:
                prod=[self]
                
        else:   # elettrone/positrone
            # probabilità di interazione 1-e^(-7s/9), s=1 ⇒ P=0.68
            rnd=random.uniform(0,1)
            if rnd>=(1-exp(-7*s/9) if is_det==False else 0):
                p1=Particle(self.q,self.e/2,self.x)
                p2=Particle(0,self.e/2,self.x)
                prod=[p1,p2]
            else:
                prod=[self]
        return prod


class Swarm(list):
    """
    Classe che rappresenta lo sciame di particelle.
        
    Attributi:
    dim : int
        nunmero di particelle che compongono lo sciame

    Metodi:
    __init__ : costruttore della classe che chiama il costruttore della classe madre
    info : stampa la dimensione e gli attributi delle particelle dello sciame
    propagate : calcola la propagazione della particella e la perdita di energia per ionizzazione
    interact : calcola i prodotti dell'interazione della particella con il materiale
    """
    
    def __init__(self,*args): # con *args si può creare uno sciame a partire da una particella esistente
        super().__init__(*args)
        self.dim=len(self)
    
    def info(self):
        """ Stampa la dimensione dello sciame e gli attributi delle particelle. """
        print('*** Sciame ***')
        print('Dimensione sciame = '+str(len(self)))
        for p in self:
            p.info()
            
    def propagate(self,s,sw_mask,mat,is_det):
        """
        La funzione propaga ogni particella dello sciame tenendo conto dell'energia di ionizzazione.
        
        Argomenti:
        s : float
            passo della simulazione, in frazione di X0
        sw_mask : list
            lista di bool che identifica quali particelle dello sciame partecipano all'interazione
        mat : Material
            materiale in cui lo sciame si propaga
        is_det : bool
            se True la simulazione non segue le leggi probabilistiche
        
        Restituisce:
        en_ion : float
            energia ceduta dalle particelle dello sciame nello step corrente
        """
        en_ion=0
        for p,i in zip(self,range(len(self))):
            en_ion+=p.propagate(s,sw_mask,mat,is_det,i)
        return en_ion
    
    def interact(self,s,is_det):
        """
        La funzione calcola i prodotti dell'interazione di ogni particella dello sciame.
        
        Argomenti:
        s : float
            passo della simulazione, in frazione di X0
        is_det : bool
            se True la simulazione non segue le leggi probabilistiche
        
        Restituisce:
        tmpsc : Sciame
            sciame delle particelle risultanti dall'interazione
        """
        
        tmpsc=[]
        for p in self:
            tmpsc.append(p.interact(s,is_det))
        # tmpsc contiene le particelle prodotte dalle interazioni dello sciame
        tmpsc=Swarm(sum(tmpsc,[])) # equivalente del metodo flatten di numpy
        return tmpsc


def argp():
    """ Inizializza il parser degli argomenti. """
    parser=argparse.ArgumentParser()
    parser.add_argument('-d', '--is-deterministic', action='store_true')
    parser.add_argument('material', choices=['h2o','pbwo4','test'], nargs='?', default='test')
    return  parser.parse_args()


def config():
    """
    La funzione chiede all'utente di inserire i parametri necessari per la simulazione.
    
    Restituisce:
    s : float
        passo della simulazione, in frazione di X0
    sw : Sciame
        sciame che si propaga nel materiale
    Q : int
        carica della particella incidente, può essere 0 (fotone), -1 (elettrone) oppure 1 (positrone)
    E0 : float
        energia in MeV della particella incidente
    sw_mask : list
        lista di bool che identifica quali particelle dello sciame partecipano all'interazione
    mat : Material
        materiale in cui lo sciame si propaga
    is_det : bool
        se True la simulazione non segue le leggi probabilistiche
    """
    
    s=0
    while (s<=0) or (s>1):
        s=float(input('passo della simulazione (default 1.0): \n') or 1.0)
    
    # particella incidente e sciame iniziale
    Q=int(input('carica della particella (default -1): \n') or -1)
    E0=float(input('energia in MeV della particella  (default 1000.0): \n') or 1000.0)
    sw=Swarm([Particle(Q,E0)])
    sw_mask=[True]
    
    args=argp()
    
    # materiale
    if args.material=='h2o':
        mat=Material('h2o')
    elif args.material=='pbwo4':
        mat=Material('pbwo4')
    if args.material=='test':
        mat=Material('test')
    else:
        mat=Material('test')
    
    # switch evoluzione deterministica
    is_det=args.is_deterministic
    
    if __name__=='__main__':
        return s,sw,sw_mask,mat,is_det
    else:
        return s,(Q,E0),mat,is_det


def evolve(s,sw,sw_mask,mat,is_det):
    """
    Funzione che calcola la propagazione e l'interazione di tutte le particelle dello sciame.
    
    Argomenti:
    s : float
        passo della simulazione, in frazione di X0
    sw : Sciame
        sciame che si propaga nel materiale
    sw_mask : list
        lista di bool che identifica quali particelle dello sciame partecipano all'interazione
    mat : Material
        materiale in cui lo sciame si propaga
    is_det : bool
        se True la simulazione non segue le leggi probabilistiche
    
    Restituisce:
    en_ion : list
        elenco delle energie cedute dalle particelle in ogni step
    n_part : list
        elenco del numero di particelle nello sciame in ogni step
    """
    
    en_ion=[]
    n_part=[]
      
    n=1
    while True in sw_mask:
        # PROPAGAZIONE
        en_ion.append(sw.propagate(s,sw_mask,mat,is_det))
        n_part.append(len(sw))
        # sw.info() # risultato della propagazione
        
        # escludere particelle che non hanno abbastanza energia
        sw=Swarm(compress(sw,sw_mask))
        # sw.info() # queste particelle sono quelle che interagiscono
        
        # INTERAZIONE
        sw=sw.interact(s,is_det)
        sw.info() # risultato dell'interazione
        print('n step = '+str(n)+'\n')
        
        if len(sw)!=0:
            sw_mask=[True]*len(sw)
            n+=1
        else:
            print('Non ci sono più particelle che possono interagire.')
            print()
    return en_ion,n_part


if __name__=='__main__':
    ## CONFIGURAZIONE SIMULAZIONE
    s,sw,sw_mask,mat,is_det=config()
    sw.info()
    print()
    
    ## SIMULAZIONE EVOLUZIONE SCIAME
    en_ion,n_part=evolve(s,sw,sw_mask,mat,is_det)
    tot_ion=arrsum(en_ion)
    print('en_ion =',en_ion)
    print('n_part =',n_part)
    print('tot_ion =',tot_ion)  
    
# breakpoint()
