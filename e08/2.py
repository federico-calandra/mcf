import numpy as np
from  scipy import integrate
import matplotlib.pyplot as plt

g=9.81
time=np.linspace(1,10,100)

def fprime(y,t):
    theta,omega=y
    DyDt=[omega, -g/l*np.sin(theta)]
    return DyDt

y0=[np.pi/4,0]
l=0.5
y=integrate.odeint(fprime,y0=y0,t=time)
plt.plot(time,y.transpose()[0],label='Θ')
plt.xlabel('t (s)')
plt.ylabel('θ (rad)')
plt.title('l=0.5 m   θ₀=45°')
plt.show()

y0=[np.pi/4,0]
l=1
y=integrate.odeint(fprime,y0=y0,t=time)
plt.plot(time,y.transpose()[0],label='Θ')
plt.xlabel('t (s)')
plt.ylabel('θ (rad)')
plt.title('l=1 m   θ₀=45°')
plt.show()

y0=[np.pi/6,0]
l=0.5
y=integrate.odeint(fprime,y0=y0,t=time)
plt.plot(time,y.transpose()[0],label='Θ')
plt.xlabel('t (s)')
plt.ylabel('θ (rad)')
plt.title('l=0.5 m   θ₀=30°')
plt.show()
