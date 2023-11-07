import pandas as pd
import matplotlib.pyplot as plt
from numpy import log10

'''
Creare un secondo script python che:
legga il file 4LAC_DR2_sel.csv e crei il DtaFrame pandas corrispondente;
stampi il nome delle colonne del DataFrame;
stampi un estratto del contenuto del DataFrame;
'''

df_data=pd.read_csv('4LAC_DR2_sel.csv')
print(df_data.columns)
print(df_data.tail(10))

'''
produca un grafico dell'indice spettrale (PL_Index) in funzione del flusso (Flux1000);
suggerimento: usare pyplot.scatter;
produca un grafico dell'indice spettrale (PL_Index) in funzione del flusso (Flux1000) con asse x logaritmico;
produca un grafico dell'indice spettrale (PL_Index) in funzione del logaritmo in base 10 della variabile nu_syn;
'''

plt.scatter(df_data['Flux1000'],df_data['PL_Index'],marker='.')
plt.xlabel('Flux1000 (ph cm$^{-2}$ s$^{-1}$)')
plt.ylabel('PL_Index')
plt.show()

plt.semilogx(df_data['Flux1000'],df_data['PL_Index'],'.')
plt.xlabel('Flux1000 (ph cm$^{-2}$ s$^{-1}$)')
plt.ylabel('PL_Index')
plt.show()

plt.scatter(log10(df_data['nu_syn']),df_data['PL_Index'],marker='.')
plt.xlabel('log10(nu_syn)')
plt.ylabel('PL_Index')
plt.show()

'''
produca un grafico dell'indice spettrale (PL_Index) in funzione del logaritmo in base 10 della variabile nu_syn distinguendo le sorgenti di classe (CLASS) bll e fsrq con la corrispondente legenda (gli altri tipi di sorgente non vanno considerate nel grafico);
suggerimento: usare .loc per la serezione dei valori nel DataFrame;
suggerimento: usare l'opzione alpha per la trasparenza;
'''

plt.scatter(log10(df_data.loc[df_data['CLASS']=='bll']['nu_syn']),
            df_data.loc[df_data['CLASS']=='bll']['PL_Index'],
            marker='.', alpha=0.5, label='bll')
plt.xlabel('log10(nu_syn)')
plt.ylabel('PL_Index')

plt.scatter(log10(df_data.loc[df_data['CLASS']=='fsrq']['nu_syn']),
            df_data.loc[df_data['CLASS']=='fsrq']['PL_Index'],
            marker='.', alpha=0.5, label='fsrq')
plt.xlabel('log10(nu_syn)')
plt.ylabel('PL_Index')
plt.legend()
plt.show()

'''
produca un grafico analogo a quello del punto 7 ma che mostri anche l'incertezza sulla stima dell'indice spettrale (Unc_PL_Index);
suggerimento: usare pyplot.errorbar;
'''

plt.errorbar(log10(df_data.loc[df_data['CLASS']=='bll']['nu_syn']),
             df_data.loc[df_data['CLASS']=='bll']['PL_Index'],
             df_data.loc[df_data['CLASS']=='bll']['Unc_PL_Index'],
             fmt='.', alpha=0.5, label='bll')
plt.xlabel('log10(nu_syn)')
plt.ylabel('PL_Index')

plt.errorbar(log10(df_data.loc[df_data['CLASS']=='fsrq']['nu_syn']),
             df_data.loc[df_data['CLASS']=='fsrq']['PL_Index'],
             df_data.loc[df_data['CLASS']=='fsrq']['Unc_PL_Index'],
             fmt='.', alpha=0.5, label='fsrq')
plt.xlabel('log10(nu_syn)')
plt.ylabel('PL_Index')
plt.legend()
plt.show()

'''
produca l'istogramma sovrapposto dell'indice spettrale per le sorgent di tipo bll e fsrq con la relativa legenda;
suggerimento: usare pyplot.hist definendo lo stesso numero di bin e lo stesso intervallo per l'asse x;
suggerimento: usare l'opzione alpha per la trasparenza;
produca un grafico analogo al precedente per il logaritmo in base 10 del valore nu_syn.

'''

print('max PL_Index,bll =',df_data.loc[df_data['CLASS']=='bll']['PL_Index'].min())
print('min PL_Index,bll =',df_data.loc[df_data['CLASS']=='bll']['PL_Index'].max())
print('max PL_Index,fsrq =',df_data.loc[df_data['CLASS']=='fsrq']['PL_Index'].min())
print('min PL_Index,fsrq =',df_data.loc[df_data['CLASS']=='fsrq']['PL_Index'].max())

plt.hist(df_data.loc[df_data['CLASS']=='bll']['PL_Index'], bins=50, range=(1.3,3.3),
         alpha=0.5, label='bll')

plt.hist(df_data.loc[df_data['CLASS']=='fsrq']['PL_Index'], bins=50, range=(1.3,3.3),
         alpha=0.5, label='bll')
plt.xlabel('PL_Index')
plt.ylabel('Num. of occurrences')
plt.legend()
plt.show()

print(df_data.loc[df_data['CLASS']=='bll']['nu_syn'])
print(df_data.loc[df_data['CLASS']=='fsrq']['nu_syn'])

print('max Log(nu_syn),bll =',log10(df_data.loc[(df_data['CLASS']=='bll')&(df_data['nu_syn']!=0)]['nu_syn']).min())
print('min Log(nu_syn),bll =',log10(df_data.loc[(df_data['CLASS']=='bll')&(df_data['nu_syn']!=0)]['nu_syn']).max())
print('max Log(nu_syn),fsrq =',log10(df_data.loc[(df_data['CLASS']=='fsrq')&(df_data['nu_syn']!=0)]['nu_syn']).min())
print('min Log(nu_syn),fsrq =',log10(df_data.loc[(df_data['CLASS']=='fsrq')&(df_data['nu_syn']!=0)]['nu_syn']).max())

plt.hist(log10(df_data.loc[df_data['CLASS']=='bll']['nu_syn']), bins=50, range=(10,21),
         alpha=0.5, label='bll')

plt.hist(log10(df_data.loc[df_data['CLASS']=='fsrq']['nu_syn']), bins=50, range=(10,21),
         alpha=0.5, label='fsrq')
plt.xlabel('log10(nu_syn)')
plt.ylabel('Num. of occurrences')
plt.legend()
plt.show()
