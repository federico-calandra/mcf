import numpy as np
from  scipy import integrate
import matplotlib.pyplot as plt

g=9.81
y0=[np.pi/4,0]
l=0.5

def fprime(y,t):
    theta,omega=y
    DyDt=[omega, -g/l*np.sin(theta)]
    return DyDt


time=np.linspace(1,10,100)
y=integrate.odeint(fprime,y0=y0,t=time)
plt.plot(time,y.transpose()[0],label='Θ')
plt.plot(time,y.transpose()[1],label='Θ')
plt.show()

breakpoint()
