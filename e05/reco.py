"""
Passo 2:
Creare il file reco.py che definisca la classe Hit.
Un oggetto di tipo Hit deve contenere informazioni su:
Id Modulo;
Id Sensore;
Time Stamp rivelazione.
Oggetti di tipo Hit devono essere ordinabili in base al Time Stamp ed eventualmente in base alla Id del Modulo e del Sensore.
"""

class Hit:    
    def __init__(self,m,s,t):
        self.modulo=m
        self.sensore=s
        self.time=t

    def __lt__(self,other):
        return self.time < other.time
