import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as spo

df_data=pd.read_csv('Jpsimumu.csv')

mc2=( df_data['E1'] + df_data['E2'] )**2 - ( (df_data['px1']+df_data['px2'])**2 + (df_data['py1']+df_data['py2'])**2 + (df_data['pz1']+df_data['pz2'])**2 )

# plt.subplot(1,2,1)
# plt.hist(mc2,bins=50)
# plt.subplot(1,2,2)
hist=plt.hist(mc2,range=(8,11),bins=100)
plt.show()

y=hist[0]
x=np.empty(0)
for i in range(len(hist[1])-1):
    x=np.append(x,(hist[1][i+1] + hist[1][i])/2)
    

def gauss1(x,a,mu,sigma,p1,p0):
    return a*np.exp( -(x-mu)**2 / (2*sigma**2) ) + p1*x + p0

def gauss2(a1,a2,mu,sigma,p1,p0):
    return a1*np.exp( -(x-mu)**2 / (2*sigma1**2) ) + a2*np.exp( -(x-mu)**2 / (2*sigma2**2) ) + p1*x + p0

p_guess=[1200,9,1,50,1]

p_opt,c=spo.curve_fit(gauss1,x,y,p_guess)

hist=plt.hist(mc2,range=(8,11),bins=100)
plt.plot(x,gauss1(x,p_opt[0],p_opt[1],p_opt[2],p_opt[3],p_opt[4]))
plt.show()

