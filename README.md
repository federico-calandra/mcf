# Simulazione sciame elettromagnetico

![sciame](https://www.borborigmi.org/wordpress/wp-content/uploads/2012/02/emshower1.gif)

(Credits: http://www.borborigmi.org/2012/02/28/rivelatori-di-particelle-a-lhc-quinta-parte-sciami-di-elettroni-e-fotoni/)

Il programma per la simulazione dello sciame elettromagnetico si trova nella directory [esame](/esame/) ed è composto dagli script `rossi.py` e `main.py`. Il primo è un modulo che contiene la definizione delle classi e della funzione di evoluzione. Il secondo file importa `rossi.py` ed esegue una simulazione montecarlo dell'evoluzione come specificato di seguito:
fissata l'energia della particella incidente E₀, si costruisce un array di 10 valori equispaziati nell'intervallo (0,E₀]. Per ciascuno di questi valori vengono eseguite 100 simulazioni da cui estrarre valore medio e deviazione standard del numero di iterazioni e dell'energia totale di ionizzazione ceduta al materiale.

## Usage
In un sistema operativo Linux la sintassi è la seguente:
        
        python main.py [-c] [-d] [-e] [materiale]

Con il flag `[-c]` vengono utilizzati i valori di default per i parametri di simulazione (step=1, Q=-1, E₀=1 GeV).

Con il flag `[-d]` l'evoluzione non segue le leggi probabilistiche.

Il flag `[-e]` cambia il tipo di simulazione che il programma svolge: con questo flag si eseguono N simulazioni tutte con lo stesso valore E₀ dell'energia incidente (il numero N è inserito dall'utente). Se N=1 il programma mostra i grafici del numero di particelle e dell'energia ceduta in ogni iterazione; se N>1 vengono mostrati i grafici del numero di iterazioni e dell'energia totale ceduta, in funzione dell'indice della simulazione.

Con l'argomento opzionale `materiale` si sceglie il materiale entro cui lo sciame si progapa. I valori permessi sono `h2o`, `pbwo4` oppure `test`; se non è specificato, il programma chiede all'utente di inserire le grandezze relative.

<!--È possibile anche eseguire il modulo `rossi.py` con la stessa sintassi già vista (ad esclusione del flag `-e`) per simulare la propagazione-->

## System requirements
Il codice è progettato per essere eseguito con Python 3. Sono necessarie le librerie `numpy`, `scipy` e `pandas`. Può essere eseguito su sistemi operativi Windows, Linux e macOS.

## Author
Il codice è stato scritto da Federico Calandra come progetto per l'esame del corso di Metodi Computazionali per la Fisica, all'Università degli Studi di Perugia nell'a.a. 2023/2024.

## License
Tutti i file in questo repository sono rilasciati con licenza Open Source.
