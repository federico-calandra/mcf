import random
import numpy as np
import matplotlib.pyplot as plt
import m1

rw_step=1
rwN=100

walkers=np.empty(0)
for i in range(10):
    walkers=np.append(walkers,m1.Walker())  # array di walker

fig1,ax1=plt.subplots()
fig2,ax2=plt.subplots()

for w in walkers:
    w.walk(rw_step,rwN)
    print(w.dist)
    ax1.plot(w.xpos,w.ypos)
    ax2.plot(w.dist)
    
plt.show()

