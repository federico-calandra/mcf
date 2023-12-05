import numpy as np
from  scipy import integrate
import matplotlib.pyplot as plt

## tensione in ingresso
def vin(t):
    t=np.trunc(t)
    if np.isscalar(t):
        if (t%2) == 0:
            return 1
        elif (t%2) == 1:
            return -1
    else:
        mask=t%2!=0
        vin=np.ones(len(t))
        vin[mask]=-1
        return vin

## eqz differenziale
def fprime(vout,t,rc,vin):
    DyDt=(vin(t)-vout)/rc
    return DyDt


time=np.linspace(1,10,100)
Vin=vin(time)
Vout={}
for rc in [1, 0.1, 0.5]:
    v=integrate.odeint(fprime,y0=0,t=time,args=(rc,vin)).flatten()
    Vout[rc]=v
    plt.plot(time,Vin,label='Vin')
    plt.plot(time,v,label='Vout_RC='+str(rc))
    plt.legend()
    # plt.show()

## costruisco array per csv
d=Vin.copy()
for k in Vout.values():
    d=np.append(d,k)
d=np.reshape(d,(4,100))

np.savetxt('data.csv',d.transpose(),delimiter=', ',header='Vin, Vout_RC1, Vout_RC01, Vout_RC001',comments='')
