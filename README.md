# POP&&SOLVE
 
#### Collezione di script per effettuare un backup strutturato delle proprie sottoposizioni su https://training.olinfo.it/.

## Struttura del backup

La soluzione di un problema sarà salvata nella cartella

> downloaded -> competizione -> edizione -> gara -> problema

## Installazione:

Basterà scaricare il sorgente da github, recarsi nella sua cartella ed eseguire

> python trainingBackup.py

Basterà attendere l'aggiornamento dei file per poter poi procedere con il download (questo sarà gestito in automatico).

Ad ogni esecuzione dello script con sorgente dei dati locale (per impostarlo su online basterà cambiare il valore di ONLINE con False nello script) si riceverà un log di quanti problemi non sono ancora stati collocati in una determinata competizione / gara.

La lista di questi problemi sarà presente in

> files -> remaining.json

Al fine di poterli visionare e categorizzare.

Chiunque è libero di contribuire all'aggiornamento dei file json al fine di garantire una continuità al progetto.