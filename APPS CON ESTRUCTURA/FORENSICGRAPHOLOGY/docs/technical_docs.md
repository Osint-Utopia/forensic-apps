# Documentazione Tecnica - Applicazione di Grafologia Forense

## Architettura del Sistema

L'applicazione di Grafologia Forense è strutturata in moduli indipendenti che lavorano insieme per fornire un'analisi completa di firme e documenti. L'architettura è basata su Python con un'interfaccia utente Gradio.

### Struttura delle Directory

```
forensic_graphology/
├── app.py                 # Punto di ingresso dell'applicazione
├── requirements.txt       # Dipendenze Python
├── README.md              # Documentazione generale
├── hf-space.yaml          # Configurazione per Hugging Face Spaces
├── src/                   # Codice sorgente
│   ├── preprocessing.py   # Pre-elaborazione delle immagini
│   ├── signature_analysis.py # Analisi delle firme
│   ├── font_analysis.py   # Analisi di font e inchiostro
│   ├── measurement.py     # Strumenti di misurazione
│   ├── image_enhancer.py  # Miglioramento delle immagini
│   ├── ml_models.py       # Modelli di machine learning
│   └── rag_system.py      # Sistema RAG
├── models/                # Directory per i modelli addestrati
├── uploads/               # Directory per i file caricati
├── results/               # Directory per i risultati generati
├── vector_store/          # Directory per il vector store
└── docs/                  # Documentazione
    ├── user_guide.md      # Guida utente
    └── technical_docs.md  # Documentazione tecnica
```

## Moduli Principali

### 1. Preprocessing (preprocessing.py)

Questo modulo gestisce la pre-elaborazione delle immagini di firme e documenti.

**Classi principali:**
- `ImagePreprocessor`: Classe per la pre-elaborazione delle immagini

**Metodi principali:**
- `load_image(image_path)`: Carica un'immagine da un percorso
- `convert_to_grayscale(image)`: Converte un'immagine in scala di grigi
- `normalize_image(image)`: Normalizza un'immagine
- `denoise_image(image)`: Riduce il rumore in un'immagine
- `binarize_image(image)`: Converte un'immagine in bianco e nero
- `preprocess_signature(image_path)`: Applica tutte le fasi di pre-elaborazione a un'immagine di firma

### 2. Signature Analysis (signature_analysis.py)

Questo modulo fornisce funzionalità per l'analisi e la comparazione di firme.

**Classi principali:**
- `SignatureAnalyzer`: Classe per l'analisi delle firme

**Metodi principali:**
- `extract_features_orb(image)`: Estrae caratteristiche ORB da un'immagine
- `extract_signature_metrics(image)`: Estrae metriche grafometriche da una firma
- `compare_signatures(image1_path, image2_path)`: Confronta due firme
- `visualize_comparison(comparison_result)`: Visualizza il risultato del confronto
- `generate_comparison_report(comparison_result)`: Genera un report testuale del confronto

### 3. Font Analysis (font_analysis.py)

Questo modulo analizza il tipo di font e l'inchiostro utilizzato nei documenti.

**Classi principali:**
- `FontAnalyzer`: Classe per l'analisi di font e inchiostro

**Metodi principali:**
- `detect_text_regions(image)`: Rileva le regioni di testo in un'immagine
- `extract_text(image, regions)`: Estrae il testo dalle regioni rilevate
- `analyze_font(image, regions)`: Analizza il tipo di font
- `analyze_ink(image)`: Analizza il tipo di inchiostro

### 4. Measurement (measurement.py)

Questo modulo fornisce strumenti per la misurazione di vari aspetti dei documenti.

**Classi principali:**
- `MeasurementTool`: Classe per la misurazione dei documenti

**Metodi principali:**
- `measure_line_spacing(image)`: Misura lo spazio tra le linee
- `measure_word_spacing(image)`: Misura lo spazio tra le parole
- `measure_margins(image)`: Misura i margini del documento
- `measure_character_slant(image)`: Misura l'inclinazione dei caratteri
- `create_digital_ruler(image)`: Crea un righello digitale
- `generate_measurement_report(image)`: Genera un report completo di misurazione

### 5. Image Enhancer (image_enhancer.py)

Questo modulo fornisce funzionalità per il miglioramento delle immagini.

**Classi principali:**
- `ImageEnhancer`: Classe per il miglioramento delle immagini

**Metodi principali:**
- `enhance_contrast(image, method)`: Migliora il contrasto di un'immagine
- `sharpen_image(image, kernel_size, strength)`: Applica un filtro di sharpening
- `apply_edge_detection(image, method)`: Applica un rilevatore di bordi
- `highlight_pressure_points(image)`: Evidenzia i punti di pressione
- `apply_emboss_effect(image)`: Applica un effetto di rilievo
- `create_signature_heatmap(image)`: Crea una mappa di calore della firma

### 6. Machine Learning Models (ml_models.py)

Questo modulo implementa modelli di machine learning per l'analisi delle firme.

**Classi principali:**
- `SignatureFeatureExtractor`: Estrae caratteristiche dalle firme
- `AnomalyDetector`: Rileva anomalie nelle firme usando Isolation Forest
- `SignatureVerifier`: Verifica l'autenticità delle firme usando una rete siamese
- `SiameseNetwork`: Implementazione della rete neurale siamese

**Metodi principali:**
- `extract_features(image_path)`: Estrae caratteristiche da un'immagine di firma
- `fit(signatures_df)`: Addestra il modello di rilevamento anomalie
- `predict(signature_path)`: Predice se una firma è anomala
- `verify(image_path1, image_path2)`: Verifica se due firme sono della stessa persona

### 7. RAG System (rag_system.py)

Questo modulo implementa un sistema RAG per la consultazione di documenti.

**Classi principali:**
- `DocumentProcessor`: Elabora e estrae testo dai documenti
- `VectorStore`: Gestisce il vector store per il sistema RAG
- `RAGSystem`: Implementa il sistema RAG completo

**Metodi principali:**
- `extract_text(file_path)`: Estrae il testo da un documento
- `process_document(file_path)`: Elabora un documento e lo divide in chunk
- `add_document(document_info)`: Aggiunge un documento al vector store
- `search(query, k)`: Cerca documenti simili a una query
- `query(query_text)`: Esegue una query sul sistema RAG

## Interfaccia Utente (app.py)

L'interfaccia utente è implementata utilizzando Gradio, una libreria Python per la creazione di interfacce web per modelli di machine learning.

**Funzioni principali:**
- `preprocess_image(image)`: Pre-elabora un'immagine
- `compare_signatures(image1, image2)`: Confronta due firme
- `analyze_font_and_ink(image)`: Analizza font e inchiostro
- `measure_document(image)`: Misura un documento
- `enhance_image(image, enhancement_type)`: Migliora un'immagine
- `detect_anomalies(image)`: Rileva anomalie in una firma
- `verify_signatures(image1, image2)`: Verifica due firme
- `upload_document(file)`: Carica un documento nel sistema RAG
- `query_rag(query_text)`: Esegue una query sul sistema RAG

## Dipendenze Principali

- **OpenCV**: Elaborazione delle immagini
- **NumPy**: Operazioni numeriche
- **Pandas**: Manipolazione dei dati
- **Matplotlib**: Visualizzazione
- **Scikit-learn**: Algoritmi di machine learning
- **PyTorch**: Deep learning
- **Gradio**: Interfaccia utente
- **LangChain**: Framework per il sistema RAG
- **Sentence-Transformers**: Modelli di embedding
- **ChromaDB**: Database vettoriale
- **PyMuPDF, python-docx, python-pptx**: Estrazione di testo da documenti
- **pytesseract**: OCR per l'estrazione di testo dalle immagini

## Deployment

L'applicazione è progettata per essere deployata su Hugging Face Spaces, una piattaforma per l'hosting di applicazioni di machine learning.

**File di configurazione:**
- `requirements.txt`: Elenca tutte le dipendenze Python
- `hf-space.yaml`: Configura l'ambiente Hugging Face Spaces
- `README.md`: Contiene metadati per Hugging Face Spaces

## Estensione dell'Applicazione

### Aggiungere Nuove Funzionalità

Per aggiungere nuove funzionalità all'applicazione:

1. Creare un nuovo modulo in `src/` o estendere un modulo esistente
2. Implementare la logica della nuova funzionalità
3. Aggiungere una nuova funzione in `app.py` che utilizza la nuova funzionalità
4. Aggiungere un nuovo tab o elemento UI in `create_interface()` in `app.py`

### Addestrare Nuovi Modelli

Per addestrare nuovi modelli di machine learning:

1. Raccogliere un dataset di firme (autentiche e false per il verificatore, solo autentiche per il rilevatore di anomalie)
2. Utilizzare le classi `AnomalyDetector` o `SignatureVerifier` per addestrare i modelli
3. Salvare i modelli addestrati nella directory `models/`
4. Aggiornare l'applicazione per utilizzare i nuovi modelli

## Considerazioni sulla Sicurezza

- L'applicazione non memorizza le immagini caricate a lungo termine
- I documenti caricati nel sistema RAG sono memorizzati localmente
- Non vengono utilizzate API esterne per l'elaborazione dei dati
- Il sistema RAG funziona in modalità di sola ricerca per evitare la necessità di token API

## Limitazioni Tecniche

- L'OCR potrebbe non funzionare correttamente con testi in lingue non latine
- I modelli di machine learning richiedono un addestramento specifico per casi d'uso particolari
- L'analisi del font e dell'inchiostro ha una precisione limitata
- Il sistema RAG funziona in modalità di sola ricerca, senza generazione di risposte AI

## Risoluzione dei Problemi

- **Errori di memoria**: Ridurre la dimensione delle immagini o utilizzare batch più piccoli
- **Errori di OCR**: Migliorare la qualità delle immagini o utilizzare pre-elaborazione
- **Prestazioni lente**: Ottimizzare i parametri dei modelli o utilizzare hardware più potente

## Riferimenti

- [OpenCV Documentation](https://docs.opencv.org/)
- [Scikit-learn Documentation](https://scikit-learn.org/stable/documentation.html)
- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)
- [Gradio Documentation](https://gradio.app/docs/)
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
