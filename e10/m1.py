import random
import numpy as np

class Walker():
    def __init__(self):
        self.xpos=0
        self.ypos=0
        self.dist=0
        
    def walk(self,step,N):
        tmpx=0
        tmpy=0
        for i in range(N):
            theta=np.random.uniform(low=0,high=2*np.pi)
            tmpx=tmpx + step*np.cos(theta)
            tmpy=tmpy + step*np.sin(theta)
            self.xpos=np.append(self.xpos, tmpx)
            self.ypos=np.append(self.ypos, tmpy) 
            self.dist=np.append(self.dist, tmpx**2+tmpy**2)
