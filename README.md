# Readme
Il programma per la simulazione dello sciame elettromagnetico si trova nella directory `esame` ed è composto dagli script `rossi.py` e `main.py`. Il primo è un modulo che contiene la definizione delle classi e della funzione di evoluzione. Il secondo importa `rossi.py` ed esegue un certo numero di simulazioni (scelto dall'utente).

## Requisiti di Sistema
Il codice è progettato per essere eseguito con Python 3. Sono necessarie le librerie `numpy`, `scipy`. Può essere eseguito su sistemi operativi Windows, Linux e macOS.

## Come lanciare il programma
In un sistema operativo Linux la sintassi è la seguente:

        python main.py [-c] [-d] [<materiale>]

Con il flag `[-c]` si utilizzano i valori di default per i parametri di simulazione.

Con il flag `[-d]` la propagazione non segue le leggi probabilistiche.

Il campo opzionale `<materiale>` può essere `h2o`, `pbwo4` oppure `test`; se omesso si utilizza il materiale `pbwo4`.

La stessa sintassi è valida anche per `rossi.py`, ma in questo caso viene eseguita solamente 1 simulazione.

## Autore
Il codice è stato scritto da Federico Calandra come progetto per l'esame di Metodi Computazionali per la Fisica.

## Licenza
Tutti i file in questo repository sono rilasciati con licenza open source.
