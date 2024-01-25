"""
Questo programma definisce la classe degli oggetti Particella, Sciame e Materiale e definisce la funzione che simula la propagazione di uno sciame elettromagnetico secondo un modello derivato da quello di Rossi.
"""

import argparse
import random
from itertools import compress
from numpy import exp
from numpy import sum as arrsum
from scipy.constants import m_e,c

class Material():
    """ Rappresenta il materiale in cui lo sciame si propaga. """
    
    def __init__(self,X0=None,dE=None,Ec=None,name=None):
        """ 
        Crea il materiale.
        
        Argomenti:
        name : string
            identifica il materiale tra ghiaccio 'h2o' e tungstato di piombo 'pbwo4'
        X0 : float
            lunghezza di radiazione (cm)
        dE : float
            perdita di energia per ionizzazione, per unità di lunghezza (MeV/cm)
        Ec : float
            energia critica (MeV)
        """  
        
        if name=='h2o':
            self.X0=39.31 # cm
            self.dE=1.82 # MeV/cm
            self.Ec=78.60 # MeV
        elif name=='pbwo4':
            self.X0=0.89 # cm
            self.dE=10.20 # MeV/cm
            self.Ec=9.31 # MeV
        elif name=='test':
            self.X0=10 # cm
            self.dE=1 # MeV/cm
            self.Ec=10 # MeV
        else:
            self.X0=X0
            self.dE=dE
            self.Ec=Ec
            
    def info(self):
        """ Stampa gli attributi del materiale. """
        print('*** Materiale ***')
        print('X0 = {} cm, dE = {} MeV/cm, Ec = {} MeV'.format(self.X0,self.dE,self.Ec))
            

class Particle():
    """ Rappresenta una particella dello sciame. """
    
    def __init__(self, q, e, x=0):
        """
        Crea una particella.
        
        Argomenti:
        q : int
            carica della particella
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
            indice di sw_mask corrispondente alla particella considerata
        
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
            # probabilità di interazione 1-e^(-7s/9)
            rnd=random.uniform(0,1)
            if rnd<=(1-exp(-7*s/9) if is_det==False else 1):
                p1=Particle(1,self.e/2,self.x)
                p2=Particle(-1,self.e/2,self.x)
                prod=[p1,p2]
            else:
                prod=[self]
                
        else:   # elettrone/positrone
            # probabilità di interazione 1-e^(-s)
            rnd=random.uniform(0,1)
            if rnd<=(1-exp(-s) if is_det==False else 1):
                p1=Particle(self.q,self.e/2,self.x)
                p2=Particle(0,self.e/2,self.x)
                prod=[p1,p2]
            else:
                prod=[self]
        return prod


class Shower(list):
    """ Rappresenta lo sciame di particelle. """
    
    def __init__(self,*args): # con *args si può creare uno sciame a partire da una particella esistente
        ''' Crea uno sciame '''
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
        tmpsc=Shower(sum(tmpsc,[])) # equivalente del metodo flatten di numpy
        return tmpsc


def argp():
    """ Inizializza il parser degli argomenti. """
        
    parser=argparse.ArgumentParser()
    parser.add_argument('-c','--config-default',action='store_true')
    parser.add_argument('-d','--is-deterministic',action='store_true')
    parser.add_argument('-e','--same-energy',action='store_true')
    parser.add_argument('material',nargs='?',default=None)
    return  parser.parse_args()


def config(config_default):
    """
    Chiede all'utente di inserire i parametri necessari per la simulazione.
    
    Argomenti;
    config_default : bool
        se True vengono utilizzati i parametri di default per la simulaizione
    
    Restituisce:
    s : float
        passo della simulazione, in frazione di X0
    Q : int
        carica della particella incidente, 0 (fotone), -1 (elettrone) oppure 1 (positrone)
    E0 : float
        energia in MeV della particella incidente
    mat : Material
        materiale in cui lo sciame si propaga
    is_det : bool
        se True la simulazione non segue le leggi probabilistiche
    """
    
    args=argp()  
 
    # materiale
    if args.material=='h2o':
        mat=Material(name='h2o')
    elif args.material=='pbwo4':
        mat=Material(name='pbwo4')
    elif args.material=='test':
        mat=Material(name='test')
    else: # ==None
        X0=float(input('lunghezza di radiazione [cm] (default 0.89)\n') or 0.89)
        dE=float(input('perdita per ionizzazione [MeV/cm] (default 10.20)\n') or 10.20)
        Ec=float(input('energia critica [MeV] (default 9.31)\n') or 9.31)
        mat=Material(X0,dE,Ec)
    
    # step e carica
    if config_default==True:
        s=1
        Q=-1
        E0=1e3
    else:
        s=0
        Q=None
        E0=0
        while (s<=0) or (s>1):
            s=float(input('passo della simulazione (default 1.0)\n') or 1.0)
        while Q not in [-1,0,1]:
            Q=int(input('carica della particella (default -1)\n') or -1)
        while E0<=0:
            E0=float(input('energia della particella [MeV] (default 1000.0)\n') or 1e3)

    # switch evoluzione deterministica
    is_det=args.is_deterministic
    
    return s,Q,E0,mat,is_det


def evolve(s,sw,sw_mask,mat,is_det):
    """
    Calcola la propagazione e l'interazione di tutte le particelle dello sciame.
    
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
    n_iter : int
        numero totale degli step eseguiti
    n_part : list
        elenco del numero di particelle nello sciame in ogni step
    en_ion : list
        energia cedute al materiale in ogni step
    """
    
    n_part=[]
    en_ion=[]
      
    n=1
    while True in sw_mask:
        # PROPAGAZIONE
        en_ion.append(sw.propagate(s,sw_mask,mat,is_det))
        n_part.append(len(sw))
        # sw.info() # risultato della propagazione
        
        # escludere particelle che non hanno abbastanza energia
        sw=Shower(compress(sw,sw_mask))
        # sw.info() # queste particelle sono quelle che interagiscono
        
        # INTERAZIONE
        sw=sw.interact(s,is_det)
        if __name__=='__main__':
            sw.info() # risultato dell'interazione
            print('n step = '+str(n)+'\n')
        
        if len(sw)!=0:
            sw_mask=[True]*len(sw)
            n+=1
        else:
            if '__name__'=='__main__':
                print('Non ci sono più particelle che possono interagire.')
                print()
            n_iter=n
    return n_iter,n_part,en_ion


if __name__=='__main__':
    ## CONFIGURAZIONE SIMULAZIONE
    args=argp()

    s,Q,E0,mat,is_det=config(args.config_default)
    mat.info()
    
    sw=Shower([Particle(Q,E0)])
    sw_mask=[True]
    sw.info()
    print()
    
    ## SIMULAZIONE EVOLUZIONE SCIAME
    n_iter,n_part,en_ion=evolve(s,sw,sw_mask,mat,is_det)
    tot_ion=arrsum(en_ion)
    
    print('n_iter =',n_iter)
    # print('n_part =',n_part)
    # print('en_ion =',en_ion)
    print('tot_ion =',tot_ion)
       
# breakpoint()
