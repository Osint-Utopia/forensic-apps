# Guida Utente - Applicazione di Grafologia Forense

## Introduzione

Benvenuti nell'applicazione di Grafologia Forense, uno strumento completo per l'analisi e la verifica di firme e documenti. Questa applicazione combina tecniche di elaborazione delle immagini, machine learning e sistemi di recupero delle informazioni per fornire un'analisi dettagliata di firme e documenti.

## Funzionalità Principali

L'applicazione è organizzata in diverse sezioni, ciascuna dedicata a specifiche funzionalità:

### 1. Pre-elaborazione

Questa sezione permette di caricare e pre-elaborare le immagini di firme e documenti. Il processo di pre-elaborazione include:
- Conversione in scala di grigi
- Normalizzazione dell'immagine
- Riduzione del rumore
- Binarizzazione

**Come utilizzare:**
1. Caricare un'immagine utilizzando il pulsante di upload
2. Cliccare su "Pre-elabora"
3. Visualizzare i risultati della pre-elaborazione

### 2. Comparazione Firme

Questa sezione permette di confrontare due firme per determinare il loro grado di similarità. L'analisi include:
- Estrazione di caratteristiche dalle firme
- Calcolo di metriche di similarità
- Generazione di un report dettagliato

**Come utilizzare:**
1. Caricare due immagini di firme
2. Cliccare su "Confronta"
3. Analizzare il report di similarità generato

### 3. Analisi Font e Inchiostro

Questa sezione analizza il tipo di font e l'inchiostro utilizzato in un documento. L'analisi include:
- Rilevamento delle regioni di testo
- Estrazione del testo
- Analisi del font (serif/sans-serif, monospaced, grassetto, corsivo)
- Analisi dell'inchiostro (tipo, colore, stampato/manoscritto)

**Come utilizzare:**
1. Caricare un'immagine contenente testo
2. Cliccare su "Analizza"
3. Esaminare il report dettagliato sul font e l'inchiostro

### 4. Misurazione e Profilazione

Questa sezione fornisce strumenti per misurare vari aspetti di un documento, come:
- Spazio tra le linee
- Spazio tra le parole
- Margini
- Inclinazione dei caratteri
- Profilo di pressione

**Come utilizzare:**
1. Caricare un'immagine di un documento
2. Cliccare su "Misura"
3. Analizzare le misurazioni e i grafici generati

### 5. Miglioramento Immagini

Questa sezione offre vari filtri e tecniche per migliorare la qualità delle immagini:
- Miglioramento del contrasto
- Sharpening
- Rilevamento dei bordi
- Evidenziazione dei punti di pressione
- Effetto rilievo
- Mappa di calore

**Come utilizzare:**
1. Caricare un'immagine
2. Selezionare il tipo di miglioramento desiderato
3. Cliccare su "Migliora"
4. Visualizzare l'immagine migliorata

### 6. Machine Learning

Questa sezione include due strumenti basati su machine learning:

#### 6.1 Rilevamento Anomalie
Utilizza algoritmi di Isolation Forest per rilevare anomalie nelle firme.

**Come utilizzare:**
1. Caricare un'immagine di firma
2. Cliccare su "Rileva Anomalie"
3. Analizzare il report che indica se la firma è anomala

#### 6.2 Verifica Firme
Utilizza una rete neurale siamese per verificare se due firme appartengono alla stessa persona.

**Come utilizzare:**
1. Caricare due immagini di firme
2. Cliccare su "Verifica"
3. Analizzare il report che indica la probabilità che le firme siano della stessa persona

### 7. Sistema RAG

Questa sezione permette di caricare, consultare e gestire documenti utilizzando un sistema RAG (Retrieval Augmented Generation).

#### 7.1 Caricamento Documenti
**Come utilizzare:**
1. Caricare un documento (PDF, DOCX, PPTX, TXT)
2. Cliccare su "Carica"
3. Verificare che il documento sia stato indicizzato correttamente

#### 7.2 Query
**Come utilizzare:**
1. Inserire una domanda o query nel campo di testo
2. Cliccare su "Esegui Query"
3. Leggere la risposta generata in base ai documenti caricati

#### 7.3 Gestione Documenti
**Come utilizzare:**
1. Cliccare su "Lista Documenti" per vedere tutti i documenti caricati
2. Per eliminare un documento, inserire l'ID del documento e cliccare su "Elimina Documento"

## Consigli per Ottenere Risultati Ottimali

1. **Qualità delle immagini**: Utilizzare immagini ad alta risoluzione per ottenere risultati migliori.
2. **Illuminazione**: Assicurarsi che le immagini siano ben illuminate e non abbiano ombre eccessive.
3. **Contrasto**: Le immagini con buon contrasto tra testo/firma e sfondo producono risultati migliori.
4. **Formati supportati**: L'applicazione supporta i formati immagine più comuni (JPG, PNG) e vari formati di documento (PDF, DOCX, PPTX, TXT).

## Limitazioni

1. Il sistema RAG funziona in modalità di sola ricerca, senza generazione di risposte AI.
2. I modelli di machine learning richiedono un addestramento specifico per casi d'uso particolari.
3. L'analisi del font e dell'inchiostro potrebbe non essere accurata per scritture molto stilizzate o inusuali.

## Risoluzione dei Problemi

Se riscontri problemi con l'applicazione, prova le seguenti soluzioni:

1. **Immagini non caricate correttamente**: Verifica che il formato dell'immagine sia supportato e che la dimensione non sia eccessiva.
2. **Errori nell'analisi**: Prova a migliorare la qualità dell'immagine o a utilizzare la sezione di pre-elaborazione prima dell'analisi.
3. **Prestazioni lente**: Le operazioni di machine learning possono richiedere tempo, specialmente su immagini di grandi dimensioni.

Per ulteriori informazioni o assistenza, consulta la documentazione tecnica o contatta il supporto.
