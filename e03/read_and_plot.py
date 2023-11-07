import pandas as pd
import matplotlib.pyplot as plt

'''
Creare uno script python che:
legga il file 4FGL_J2202.7+4216_weekly_9_11_2023.csv e crei il DataFrame pandas corrispondente;
stampi il nome delle colonne del DataFrame;
'''

df_data=pd.read_csv('4FGL_J2202.7+4216_weekly_9_11_2023.csv')
print(df_data.columns)
print(df_data['Julian Date'])

'''
produca un grafico del flusso in funzione del Giorno Giuliano (Julian Date)
suggerimento: usare pyplot.plot;
produca un grafico del flusso in funzione del Giorno Giuliano coi punti del grafico demarcati da un simbolo;
suggerimento: usare pyplot.plot con opzione 'o' o equivalente;
'''

plt.plot(df_data['Julian Date'],df_data['Photon Flux [0.1-100 GeV](photons cm-2 s-1)'])
plt.show()
plt.plot(df_data['Julian Date'],df_data['Photon Flux [0.1-100 GeV](photons cm-2 s-1)'], '.')
plt.show()

'''
produca un grafico del flusso in funzione del Giorno Giuliano con barre di errore e salvi il risultato in un file png e/o pdf;
suggerimento: usare pyplot.errorbar;
produca un grafico simile al precedente con asse y logaritmico e salvi il risultato in un file png e/o pdf;
'''

plt.errorbar(df_data['Julian Date'],df_data['Photon Flux [0.1-100 GeV](photons cm-2 s-1)'],df_data['Photon Flux Error(photons cm-2 s-1)'],fmt='.')
plt.savefig("read_and_plot-1.png")
plt.show()

plt.semilogy(df_data['Julian Date'],df_data['Photon Flux [0.1-100 GeV](photons cm-2 s-1)'])
plt.savefig("read_and_plot-2.png")
plt.show()
