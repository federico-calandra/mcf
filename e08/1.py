import numpy as np
from  scipy import integrate
import matplotlib.pyplot as plt


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


def fprime(vout,t,rc,vin):
    DyDt=(vin(t)-vout)/rc
    return DyDt


time=np.linspace(1,10,100)
Vin=vin(time)
Vout=np.empty(0)
for rc in [1, 0.1, 0.01]:
    Vout=np.asanyarray(integrate.odeint(fprime,y0=0,t=time,args=(rc,vin)))
    plt.plot(time,Vin,label='Vin')
    plt.plot(time,Vout,label='Vout_rc'+str(1./rc))
    # plt.plot(time,Vout[1],label='Vout_rc01')
    # plt.plot(time,Vout[2],label='Vout_rc001')
plt.legend()
plt.show()

# np.savetxt((time, Vin, Vout),'data.csv')

breakpoint()
