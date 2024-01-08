#!/bin/python

class Particella():
    def __init__(self, q, e, p=0):
        self.carica=q
        self.en=e
        self.pos=p
        
    def info(self):
            print('*** Particella ***')
            print('carica = {}e, energia = {} MeV'.format(self.carica, self.en))
            print('posizione = {} cm'.format(self.pos))
        
    def interact(self):
        if self.carica==0:  # fotone
            p1=Particella(1,self.en/2,self.pos)
            p2=Particella(-1,self.en/2,self.pos)
        else:   # elettrone/positrone
            p1=Particella(0,self.en/2,self.pos)
            p2=Particella(1,self.en/2,self.pos)
        return [p1,p2]
            
    def propagate(self):
        self.pos+=step*X0
        
        
class Sciame(list):
    def info(self):
        print('*** Sciame ***')
        print('Dimensione sciame = '+str(len(sc)))
        for p in self:
            p.info()
    
    def propagate(self):
        for p in self:
            p.propagate()
            
            
## CONFIGURAZIONE
e0 =        10      # MeV
e_crit =    78.60   # MeV
X0 =        39.31   # cm
dE =        1.822   # MeV/cm
step =      1


## CREAZIONE SCIAME
sc=Sciame()
sc.append(Particella(1,e0))
sc.info()

## EVOLUZIONE SCIAME
for n in range(1,4):
    sc.propagate()
    tmpsc=[]
    for p in sc:
        tmpsc.append(p.interact())
    # tmpsc contiene le particelle prodotte dalle interazioni dello sciame precedente
    tmpsc=Sciame(sum(tmpsc,[]))
    sc=tmpsc
    sc.info()
    print()

breakpoint()
