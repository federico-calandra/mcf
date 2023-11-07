import pandas as pd
import matplotlib.pyplot as plt
from numpy import log10

'''
Creare uno script python che combini il grafico del punto 2.7 assieme agli istogrammi dei punti 2.9 e 2.10 in un'unica immagine come in figura e salvi il risultato in un file png e in un file pdf.
'''

df_data=pd.read_csv('4LAC_DR2_sel.csv')


Axes=plt.subplot(2, 2, 1)
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


Axes=plt.subplot(2, 2, 3)
plt.hist(df_data.loc[df_data['CLASS']=='bll']['PL_Index'], bins=50, range=(1.3,3.3),
         alpha=0.5, label='bll')

plt.hist(df_data.loc[df_data['CLASS']=='fsrq']['PL_Index'], bins=50, range=(1.3,3.3),
         alpha=0.5, label='bll')
plt.xlabel('PL_Index')
plt.ylabel('Num. of occurrences')
plt.legend()


Axes=plt.subplot(2, 2, 4)
plt.hist(log10(df_data.loc[df_data['CLASS']=='bll']['nu_syn']), bins=50, range=(10,21),
         alpha=0.5, label='bll')

plt.hist(log10(df_data.loc[df_data['CLASS']=='fsrq']['nu_syn']), bins=50, range=(10,21),
         alpha=0.5, label='fsrq')
plt.xlabel('log10(nu_syn)')
plt.ylabel('Num. of occurrences')
plt.legend()

plt.savefig('read_and_plot3.png')
plt.show()
