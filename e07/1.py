"""
Fase preliminare

Creare uno script python che:

legga il file di dati indicato sopra e crei il corrispettivo DataFrame pandas;
calcoli la massa invariante per ogni evento;
produca un istogramma della massa invariante calcolata;
produca un istogramma della massa invariante in un intervallo ristretto attorno al picco più alto;
SUGGERIMENTO: selezionare l'intervallo in modo tale da lasciare del margine attorno al picco in cui sia apprezzabile il livello di fondo;

Fit con Gaussiana singola

Modificare lo script in moto tale che:

definisca una funzione di fit (

) corrispondnete ad una funzoine di Gaus + una polinomiale di primo grado;
esegua il fit dei dati attorno al picco principale con la funzione
;
produca un grafico che mostri:

la funzione di fit ottimizzata sovrapposta ai dati;
lo scarto fra dati e fit (in un pannello separato);
opzionale: lo scarto fra dati e fit diviso per l'errore (in un ulteriore pannello separato);

stampi il valore dei parametri del fit e del

;

Valutare i risultati sia graficamente che quantitativamente;
Fit con Gaussiana doppia

Modificare lo script in moto tale che:

definisca una seconda funzione di fit (

) corrispondnete alla somma di due funzoini di Gaus con stessa media ma diversa sigma e normalizzazione + una polinomiale di primo grado;
ripeta i passi 2,3 e 4 del punto precedente anche per

.

Opzionale

Ripetere l'analisi per il picco a più alta energia. Di che particella potrebbe trattarsi?
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as spo

df_data=pd.read_csv('Jpsimumu.csv')

# calcolo massa invariante da dati sperimentali
mc2=( df_data['E1'] + df_data['E2'] )**2 - ( (df_data['px1']+df_data['px2'])**2 + (df_data['py1']+df_data['py2'])**2 + (df_data['pz1']+df_data['pz2'])**2 )

## plot istogrammi
fig,axs=plt.subplots(1,2)
axs[0].hist(mc2,bins=50)
axs[1].hist(mc2,range=(8,11),bins=100)

ax_prop=[{'xlabel':'mass','ylabel':'# of occurrences','title':'frequency of mass'},
         {'xlabel':'mass','ylabel':'# of occurrences','title':'frequency of mass in interval (8,11)'}]
for key,ax in enumerate(axs.flat):
    ax.set(**ax_prop[key])
    
plt.show()


## estrapolazione dati da istogramma
hist=np.histogram(mc2,range=(8,11),bins=100)
y=hist[0]   # num di eventi in ogni bin
err_y=np.sqrt(y)
x=np.empty(0)   # estremi dei bin
for i in range(len(hist[1])-1):
    x=np.append(x,(hist[1][i+1] + hist[1][i])/2)
    
## stima parametri con gauss1
def gauss(f,beta):
    return 1./f**beta

p_guess=[1]     # a m σ p₁ p₀
p_opt,cov=spo.curve_fit(gauss,,y,p_guess,sigma=err_y,absolute_sigma=True)
# err_p=np.sqrt(np.diag(cov))

## scarto e chi²
y_fit1=gauss1(x,p_opt[0],p_opt[1],p_opt[2],p_opt[3],p_opt[4])
delta_y=y-y_fit1
chi2=np.sum(delta_y**2/y)
print('X² =', chi2)

## confronto grafico
fig,axs=plt.subplots(2)
axs[0].hist(mc2,range=(8,11),bins=100)
axs[0].plot(x,y_fit1)
axs[1].plot(x,delta_y)

ax_prop=[{'xlabel':'mass','ylabel':'# of occurrences','title':'fit of data'},
         {'xlabel':'mass','ylabel':'# of occurrences','title':'deviation from fit'}]
for key,ax in enumerate(axs.flat):
    ax.set(**ax_prop[key])
# plt.axhline(color='gray')
plt.show()

### intorno a 9.5 lo scarto è maggiore

## stima parametri con gauss2
def gauss2(x,a1,a2,mu,sigma1,sigma2,p1,p0):
    r=a1*np.exp( -(x-mu)**2 / (2*sigma1**2) ) + a2*np.exp( -(x-mu)**2 / (2*sigma2**2) ) + p1*x + p0
    return r

p_guess=[1200,1500,9.5,1,0.25,25,1]     # a₁ a₂ m σ₁ σ₂ p₁ p₀
p_opt,cov=spo.curve_fit(gauss2,x,y,p_guess,sigma=err_y,absolute_sigma=True)
# err_p=np.sqrt(np.diag(cov))

y_fit2=gauss2(x,p_opt[0],p_opt[1],p_opt[2],p_opt[3],p_opt[4],p_opt[5],p_opt[6])

## scarto e chi²
delta_y=y-y_fit2
chi2=np.sum(delta_y**2/y)
print('ndof=',ndof)
print('X²/ndof =', chi2)

fig,axs=plt.subplots(2)
axs[0].hist(mc2,range=(8,11),bins=100)
axs[0].plot(x,y_fit2)
axs[1].plot(x,delta_y)

ax_prop=[{'xlabel':'mass','ylabel':'# of occurrences','title':'fit of data'},
         {'xlabel':'mass','ylabel':'# of occurrences','title':'deviation from fit'}]
for key,ax in enumerate(axs.flat):
    ax.set(**ax_prop[key])
# plt.axhline(color='gray')
plt.show()


