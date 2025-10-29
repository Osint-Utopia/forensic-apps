import os
import gradio as gr
import numpy as np
import cv2
import matplotlib.pyplot as plt
import tempfile
from PIL import Image
import torch
import time
import json

# Importa i moduli dell'applicazione
from src.preprocessing import ImagePreprocessor
from src.signature_analysis import SignatureAnalyzer
from src.font_analysis import FontAnalyzer
from src.measurement import MeasurementTool
from src.image_enhancer import ImageEnhancer
from src.ml_models import SignatureFeatureExtractor, AnomalyDetector, SignatureVerifier
from src.rag_system import DocumentProcessor, VectorStore, RAGSystem

# Definisci le directory di lavoro
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
MODELS_DIR = os.path.join(BASE_DIR, "models")
VECTOR_STORE_DIR = os.path.join(BASE_DIR, "vector_store")

# Crea le directory se non esistono
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

# Inizializza i componenti dell'applicazione
preprocessor = ImagePreprocessor()
signature_analyzer = SignatureAnalyzer()
font_analyzer = FontAnalyzer()
measurement_tool = MeasurementTool()
image_enhancer = ImageEnhancer()

# Inizializza il sistema RAG
rag_system = RAGSystem(
    upload_dir=UPLOAD_DIR,
    vector_store_dir=VECTOR_STORE_DIR,
    use_local_model=True,
    model_name="google/flan-t5-small"
)

# Inizializza i modelli di machine learning
# Nota: questi verranno caricati solo quando necessario
anomaly_detector = None
signature_verifier = None

# Funzione per salvare un'immagine temporanea
def save_temp_image(image):
    if image is None:
        return None
    
    # Crea un file temporaneo
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png", dir=UPLOAD_DIR)
    temp_path = temp_file.name
    temp_file.close()
    
    # Salva l'immagine
    if isinstance(image, np.ndarray):
        cv2.imwrite(temp_path, image)
    elif isinstance(image, Image.Image):
        image.save(temp_path)
    
    return temp_path

# Funzione per convertire una figura matplotlib in un'immagine
def fig_to_image(fig):
    # Salva la figura in un file temporaneo
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png", dir=RESULTS_DIR)
    temp_path = temp_file.name
    temp_file.close()
    
    # Salva la figura
    fig.savefig(temp_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    
    # Carica l'immagine
    image = cv2.imread(temp_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    return image, temp_path

# Funzione per pre-elaborare un'immagine
def preprocess_image(image):
    if image is None:
        return None, "Nessuna immagine fornita."
    
    try:
        # Salva l'immagine temporaneamente
        temp_path = save_temp_image(image)
        
        # Pre-elabora l'immagine
        processed = preprocessor.preprocess_signature(temp_path)
        
        # Crea un'immagine di output con tutte le fasi di pre-elaborazione
        h, w = processed['original'].shape[:2]
        output = np.zeros((h * 2, w * 3, 3), dtype=np.uint8)
        
        # Converti le immagini in RGB se necessario
        original_rgb = cv2.cvtColor(processed['original'], cv2.COLOR_BGR2RGB)
        
        # Converti le immagini in scala di grigi in RGB
        grayscale_rgb = cv2.cvtColor(processed['grayscale'], cv2.COLOR_GRAY2RGB)
        normalized_rgb = cv2.cvtColor(processed['normalized'], cv2.COLOR_GRAY2RGB)
        denoised_rgb = cv2.cvtColor(processed['denoised'], cv2.COLOR_GRAY2RGB)
        binary_rgb = cv2.cvtColor(processed['binary'], cv2.COLOR_GRAY2RGB)
        
        # Ridimensiona le immagini se necessario
        original_resized = cv2.resize(original_rgb, (w, h))
        grayscale_resized = cv2.resize(grayscale_rgb, (w, h))
        normalized_resized = cv2.resize(normalized_rgb, (w, h))
        denoised_resized = cv2.resize(denoised_rgb, (w, h))
        binary_resized = cv2.resize(binary_rgb, (w, h))
        
        # Inserisci le immagini nell'output
        output[0:h, 0:w] = original_resized
        output[0:h, w:2*w] = grayscale_resized
        output[0:h, 2*w:3*w] = normalized_resized
        output[h:2*h, 0:w] = denoised_resized
        output[h:2*h, w:2*w] = binary_resized
        
        # Aggiungi etichette
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(output, "Originale", (10, 30), font, 1, (255, 255, 255), 2)
        cv2.putText(output, "Scala di Grigi", (w + 10, 30), font, 1, (255, 255, 255), 2)
        cv2.putText(output, "Normalizzata", (2*w + 10, 30), font, 1, (255, 255, 255), 2)
        cv2.putText(output, "Denoised", (10, h + 30), font, 1, (255, 255, 255), 2)
        cv2.putText(output, "Binaria", (w + 10, h + 30), font, 1, (255, 255, 255), 2)
        
        # Salva l'immagine di output
        output_path = os.path.join(RESULTS_DIR, f"preprocessed_{os.path.basename(temp_path)}")
        cv2.imwrite(output_path, cv2.cvtColor(output, cv2.COLOR_RGB2BGR))
        
        return output, f"Pre-elaborazione completata. Risultati salvati in {output_path}"
    except Exception as e:
        return None, f"Errore durante la pre-elaborazione: {str(e)}"

# Funzione per confrontare due firme
def compare_signatures(image1, image2):
    if image1 is None or image2 is None:
        return None, "Fornire entrambe le immagini delle firme."
    
    try:
        # Salva le immagini temporaneamente
        temp_path1 = save_temp_image(image1)
        temp_path2 = save_temp_image(image2)
        
        # Confronta le firme
        comparison_result = signature_analyzer.compare_signatures(temp_path1, temp_path2)
        
        # Visualizza il confronto
        fig = signature_analyzer.visualize_comparison(comparison_result)
        
        # Converti la figura in un'immagine
        output_image, output_path = fig_to_image(fig)
        
        # Genera un report testuale
        report = signature_analyzer.generate_comparison_report(comparison_result)
        
        # Salva il report
        report_path = os.path.join(RESULTS_DIR, f"comparison_report_{int(time.time())}.txt")
        with open(report_path, 'w') as f:
            f.write(report)
        
        return output_image, f"Confronto completato. Punteggio di similarità: {comparison_result['combined_score']:.2f}%\n\n{report}"
    except Exception as e:
        return None, f"Errore durante il confronto delle firme: {str(e)}"

# Funzione per analizzare il font e l'inchiostro
def analyze_font_and_ink(image):
    if image is None:
        return None, "Nessuna immagine fornita."
    
    try:
        # Salva l'immagine temporaneamente
        temp_path = save_temp_image(image)
        
        # Carica l'immagine
        img = preprocessor.load_image(temp_path)
        
        # Rileva le regioni di testo
        text_regions = font_analyzer.detect_text_regions(img)
        
        # Estrai il testo
        text_result = font_analyzer.extract_text(img, text_regions)
        
        # Analizza il font
        font_result = font_analyzer.analyze_font(img, text_regions)
        
        # Analizza l'inchiostro
        ink_result = font_analyzer.analyze_ink(img)
        
        # Crea un'immagine di output
        output = img.copy()
        
        # Disegna i rettangoli delle regioni di testo
        for i, (x, y, w, h) in enumerate(text_regions):
            cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(output, f"Testo {i+1}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Converti in RGB per la visualizzazione
        output_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        
        # Prepara il report
        report = "ANALISI DEL FONT E DELL'INCHIOSTRO\n"
        report += "=" * 50 + "\n\n"
        
        # Aggiungi il testo estratto
        report += "TESTO ESTRATTO:\n"
        report += text_result['full_text'] + "\n\n"
        
        # Aggiungi l'analisi del font
        report += "ANALISI DEL FONT:\n"
        for i, region in enumerate(font_result['regions']):
            font_info = region['font_info']
            report += f"Regione {i+1}:\n"
            report += f"- Tipo: {'Serif' if font_info['is_serif'] else 'Sans-serif'}\n"
            report += f"- Monospaced: {'Sì' if font_info['is_monospaced'] else 'No'}\n"
            report += f"- Grassetto: {'Sì' if font_info['is_bold'] else 'No'}\n"
            report += f"- Corsivo: {'Sì' if font_info['is_italic'] else 'No'}\n"
            report += f"- Dimensione stimata: {font_info['font_size']:.1f} pt\n"
            report += f"- Confidenza: {font_info['confidence']:.1f}%\n"
            report += f"- Font possibili: {', '.join(font_info['possible_fonts'])}\n\n"
        
        # Aggiungi l'analisi dell'inchiostro
        report += "ANALISI DELL'INCHIOSTRO:\n"
        report += f"- Tipo: {ink_result['ink_type']}\n"
        report += f"- Colore: {ink_result['ink_color']}\n"
        report += f"- Stampato: {'Sì' if ink_result['is_printed'] else 'No'}\n"
        report += f"- Confidenza: {ink_result['confidence']:.1f}%\n\n"
        
        report += "DETTAGLI TECNICI:\n"
        report += f"- Tonalità media (H): {ink_result['details']['hue_mean']:.1f}\n"
        report += f"- Saturazione media (S): {ink_result['details']['saturation_mean']:.1f}\n"
        report += f"- Valore medio (V): {ink_result['details']['value_mean']:.1f}\n"
        report += f"- Deviazione standard tonalità: {ink_result['details']['hue_std']:.1f}\n"
        report += f"- Deviazione standard saturazione: {ink_result['details']['saturation_std']:.1f}\n"
        report += f"- Deviazione standard valore: {ink_result['details']['value_std']:.1f}\n"
        report += f"- Copertura inchiostro: {ink_result['details']['ink_coverage']*100:.1f}%\n"
        
        # Salva il report
        report_path = os.path.join(RESULTS_DIR, f"font_ink_analysis_{int(time.time())}.txt")
        with open(report_path, 'w') as f:
            f.write(report)
        
        return output_rgb, report
    except Exception as e:
        return None, f"Errore durante l'analisi del font e dell'inchiostro: {str(e)}"

# Funzione per misurare e profilare un documento
def measure_document(image):
    if image is None:
        return None, "Nessuna immagine fornita."
    
    try:
        # Salva l'immagine temporaneamente
        temp_path = save_temp_image(image)
        
        # Carica l'immagine
        img = preprocessor.load_image(temp_path)
        
        # Genera il report di misurazione
        measurements = measurement_tool.generate_measurement_report(img)
        
        # Visualizza le misurazioni
        fig = measurement_tool.visualize_measurements(img, measurements)
        
        # Converti la figura in un'immagine
        output_image, output_path = fig_to_image(fig)
        
        # Crea un righello digitale
        ruler_image = measurement_tool.create_digital_ruler(img)
        ruler_path = os.path.join(RESULTS_DIR, f"ruler_{os.path.basename(temp_path)}")
        cv2.imwrite(ruler_path, ruler_image)
        
        # Prepara il report
        report = "REPORT DI MISURAZIONE DEL DOCUMENTO\n"
        report += "=" * 50 + "\n\n"
        
        # Aggiungi le misurazioni delle linee
        report += "SPAZIO TRA LE LINEE:\n"
        report += f"- Numero di linee: {measurements['line_spacing']['line_count']}\n"
        report += f"- Spazio medio: {measurements['line_spacing']['average_spacing']:.1f} pixel\n"
        report += f"- Deviazione standard: {measurements['line_spacing']['spacing_std']:.1f} pixel\n\n"
        
        # Aggiungi le misurazioni delle parole
        report += "SPAZIO TRA LE PAROLE:\n"
        report += f"- Numero di parole: {measurements['word_spacing']['word_count']}\n"
        report += f"- Spazio medio: {measurements['word_spacing']['average_spacing']:.1f} pixel\n"
        report += f"- Deviazione standard: {measurements['word_spacing']['spacing_std']:.1f} pixel\n\n"
        
        # Aggiungi i margini
        report += "MARGINI:\n"
        report += f"- Superiore: {measurements['margins']['top']} pixel\n"
        report += f"- Inferiore: {measurements['margins']['bottom']} pixel\n"
        report += f"- Sinistro: {measurements['margins']['left']} pixel\n"
        report += f"- Destro: {measurements['margins']['right']} pixel\n\n"
        
        # Aggiungi l'inclinazione dei caratteri
        report += "INCLINAZIONE DEI CARATTERI:\n"
        report += f"- Inclinazione media: {measurements['character_slant']['average_slant']:.1f} gradi\n"
        report += f"- Deviazione standard: {measurements['character_slant']['slant_std']:.1f} gradi\n\n"
        
        # Aggiungi il profilo di pressione
        report += "PROFILO DI PRESSIONE:\n"
        report += f"- Pressione media: {measurements['pressure_profile']['average_pressure']:.1f}\n"
        report += f"- Deviazione standard: {measurements['pressure_profile']['pressure_std']:.1f}\n"
        
        # Salva il report
        report_path = os.path.join(RESULTS_DIR, f"measurement_report_{int(time.time())}.txt")
        with open(report_path, 'w') as f:
            f.write(report)
        
        return output_image, report
    except Exception as e:
        return None, f"Errore durante la misurazione del documento: {str(e)}"

# Funzione per migliorare un'immagine
def enhance_image(image, enhancement_type):
    if image is None:
        return None, "Nessuna immagine fornita."
    
    try:
        # Salva l'immagine temporaneamente
        temp_path = save_temp_image(image)
        
        # Carica l'immagine
        img = preprocessor.load_image(temp_path)
        
        # Applica il miglioramento selezionato
        if enhancement_type == "contrast":
            enhanced = image_enhancer.enhance_contrast(img, method='clahe')
            title = "Miglioramento del Contrasto"
        elif enhancement_type == "sharpen":
            enhanced = image_enhancer.sharpen_image(img, strength=1.5)
            title = "Sharpening dell'Immagine"
        elif enhancement_type == "edges":
            enhanced = image_enhancer.apply_edge_detection(img, method='canny')
            title = "Rilevamento dei Bordi"
        elif enhancement_type == "pressure":
            enhanced = image_enhancer.highlight_pressure_points(img)
            title = "Evidenziazione Punti di Pressione"
        elif enhancement_type == "emboss":
            enhanced = image_enhancer.apply_emboss_effect(img)
            title = "Effetto Rilievo"
        elif enhancement_type == "heatmap":
            enhanced = image_enhancer.create_signature_heatmap(img)
            title = "Mappa di Calore della Firma"
        elif enhancement_type == "all":
            # Applica tutti i miglioramenti
            enhancements = image_enhancer.enhance_signature(img)
            
            # Crea un'immagine di output con tutti i miglioramenti
            h, w = enhancements['original'].shape[:2]
            output = np.zeros((h * 2, w * 4, 3), dtype=np.uint8)
            
            # Converti le immagini in RGB se necessario
            original_rgb = cv2.cvtColor(enhancements['original'], cv2.COLOR_BGR2RGB)
            
            # Converti le immagini in scala di grigi in RGB
            grayscale_rgb = cv2.cvtColor(enhancements['grayscale'], cv2.COLOR_GRAY2RGB)
            contrast_rgb = cv2.cvtColor(enhancements['contrast_enhanced'], cv2.COLOR_GRAY2RGB)
            sharpened_rgb = cv2.cvtColor(enhancements['sharpened'], cv2.COLOR_GRAY2RGB)
            edges_rgb = cv2.cvtColor(enhancements['edges'], cv2.COLOR_GRAY2RGB)
            embossed_rgb = cv2.cvtColor(enhancements['embossed'], cv2.COLOR_GRAY2RGB)
            
            # Inserisci le immagini nell'output
            output[0:h, 0:w] = original_rgb
            output[0:h, w:2*w] = grayscale_rgb
            output[0:h, 2*w:3*w] = contrast_rgb
            output[0:h, 3*w:4*w] = sharpened_rgb
            output[h:2*h, 0:w] = edges_rgb
            output[h:2*h, w:2*w] = embossed_rgb
            output[h:2*h, 2*w:3*w] = enhancements['pressure_points']
            output[h:2*h, 3*w:4*w] = enhancements['heatmap']
            
            # Aggiungi etichette
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(output, "Originale", (10, 30), font, 1, (255, 255, 255), 2)
            cv2.putText(output, "Scala di Grigi", (w + 10, 30), font, 1, (255, 255, 255), 2)
            cv2.putText(output, "Contrasto", (2*w + 10, 30), font, 1, (255, 255, 255), 2)
            cv2.putText(output, "Sharpening", (3*w + 10, 30), font, 1, (255, 255, 255), 2)
            cv2.putText(output, "Bordi", (10, h + 30), font, 1, (255, 255, 255), 2)
            cv2.putText(output, "Rilievo", (w + 10, h + 30), font, 1, (255, 255, 255), 2)
            cv2.putText(output, "Punti di Pressione", (2*w + 10, h + 30), font, 1, (255, 255, 255), 2)
            cv2.putText(output, "Mappa di Calore", (3*w + 10, h + 30), font, 1, (255, 255, 255), 2)
            
            enhanced = output
            title = "Tutti i Miglioramenti"
        else:
            return None, f"Tipo di miglioramento non supportato: {enhancement_type}"
        
        # Salva l'immagine migliorata
        output_path = os.path.join(RESULTS_DIR, f"{enhancement_type}_{os.path.basename(temp_path)}")
        
        # Converti in BGR per il salvataggio se necessario
        if len(enhanced.shape) == 3 and enhanced.shape[2] == 3:
            cv2.imwrite(output_path, cv2.cvtColor(enhanced, cv2.COLOR_RGB2BGR))
        else:
            cv2.imwrite(output_path, enhanced)
        
        # Converti in RGB per la visualizzazione se necessario
        if len(enhanced.shape) == 2:
            enhanced_rgb = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2RGB)
        elif enhanced.shape[2] == 3:
            enhanced_rgb = enhanced
        else:
            enhanced_rgb = enhanced
        
        return enhanced_rgb, f"{title} completato. Risultato salvato in {output_path}"
    except Exception as e:
        return None, f"Errore durante il miglioramento dell'immagine: {str(e)}"

# Funzione per rilevare anomalie in una firma
def detect_anomalies(image, model_path=None):
    global anomaly_detector
    
    if image is None:
        return "Nessuna immagine fornita."
    
    try:
        # Salva l'immagine temporaneamente
        temp_path = save_temp_image(image)
        
        # Inizializza il rilevatore di anomalie se non è già stato fatto
        if anomaly_detector is None:
            anomaly_detector = AnomalyDetector()
            
            # Carica il modello se specificato
            if model_path and os.path.exists(model_path):
                anomaly_detector.load_model(model_path)
            else:
                # Cerca un modello nella directory dei modelli
                model_files = [f for f in os.listdir(MODELS_DIR) if f.endswith('.joblib') and 'anomaly' in f]
                if model_files:
                    model_path = os.path.join(MODELS_DIR, model_files[0])
                    anomaly_detector.load_model(model_path)
                else:
                    return "Nessun modello di rilevamento anomalie trovato. Addestrare un modello prima di utilizzare questa funzione."
        
        # Estrai caratteristiche dalla firma
        feature_extractor = SignatureFeatureExtractor()
        features = feature_extractor.extract_features(temp_path)
        
        # Rileva anomalie
        result = anomaly_detector.predict(features=features)
        
        # Prepara il report
        report = "RILEVAMENTO ANOMALIE NELLA FIRMA\n"
        report += "=" * 50 + "\n\n"
        
        report += f"RISULTATO: {'ANOMALIA RILEVATA' if result['is_anomaly'] else 'FIRMA NORMALE'}\n\n"
        
        report += f"Punteggio di anomalia: {result['anomaly_score']:.4f}\n"
        report += f"Confidenza: {result['confidence']:.2f}%\n\n"
        
        report += "INTERPRETAZIONE:\n"
        if result['is_anomaly']:
            report += "La firma presenta caratteristiche anomale rispetto al modello di riferimento.\n"
            report += "Potrebbe trattarsi di una firma falsa o di una variazione significativa rispetto alle firme autentiche.\n"
        else:
            report += "La firma presenta caratteristiche coerenti con il modello di riferimento.\n"
            report += "È probabile che si tratti di una firma autentica.\n"
        
        report += "\nNOTA: Questo risultato è basato su un modello statistico e deve essere interpretato da un esperto di grafologia forense."
        
        return report
    except Exception as e:
        return f"Errore durante il rilevamento delle anomalie: {str(e)}"

# Funzione per verificare due firme
def verify_signatures(image1, image2, model_path=None):
    global signature_verifier
    
    if image1 is None or image2 is None:
        return "Fornire entrambe le immagini delle firme."
    
    try:
        # Salva le immagini temporaneamente
        temp_path1 = save_temp_image(image1)
        temp_path2 = save_temp_image(image2)
        
        # Inizializza il verificatore di firme se non è già stato fatto
        if signature_verifier is None:
            signature_verifier = SignatureVerifier()
            
            # Carica il modello se specificato
            if model_path and os.path.exists(model_path):
                signature_verifier.load_model(model_path)
            else:
                # Cerca un modello nella directory dei modelli
                model_files = [f for f in os.listdir(MODELS_DIR) if f.endswith('.pth') and 'verifier' in f]
                if model_files:
                    model_path = os.path.join(MODELS_DIR, model_files[0])
                    signature_verifier.load_model(model_path)
                else:
                    return "Nessun modello di verifica firme trovato. Addestrare un modello prima di utilizzare questa funzione."
        
        # Verifica le firme
        result = signature_verifier.verify(temp_path1, temp_path2)
        
        # Prepara il report
        report = "VERIFICA DELLE FIRME\n"
        report += "=" * 50 + "\n\n"
        
        report += f"RISULTATO: {'STESSA PERSONA' if result['is_same_person'] else 'PERSONE DIVERSE'}\n\n"
        
        report += f"Probabilità: {result['probability']:.4f}\n"
        report += f"Confidenza: {result['confidence']:.2f}%\n\n"
        
        report += "INTERPRETAZIONE:\n"
        if result['is_same_person']:
            report += "Le due firme sono probabilmente della stessa persona.\n"
            report += f"Il modello ha una confidenza del {result['confidence']:.2f}% in questa valutazione.\n"
        else:
            report += "Le due firme sono probabilmente di persone diverse.\n"
            report += f"Il modello ha una confidenza del {result['confidence']:.2f}% in questa valutazione.\n"
        
        report += "\nNOTA: Questo risultato è basato su un modello di deep learning e deve essere interpretato da un esperto di grafologia forense."
        
        return report
    except Exception as e:
        return f"Errore durante la verifica delle firme: {str(e)}"

# Funzione per caricare un documento nel sistema RAG
def upload_document(file):
    if file is None:
        return "Nessun file fornito."
    
    try:
        # Elabora e memorizza il documento
        result = rag_system.process_and_store_document(file)
        
        if result['success']:
            return f"Documento '{result['filename']}' caricato e indicizzato con successo.\n\n" + \
                   f"ID documento: {result['document_id']}\n" + \
                   f"Numero di chunk: {result['chunk_count']}"
        else:
            return f"Errore durante il caricamento del documento: {result['error']}"
    except Exception as e:
        return f"Errore durante il caricamento del documento: {str(e)}"

# Funzione per eseguire una query sul sistema RAG
def query_rag(query_text):
    if not query_text:
        return "Nessuna query fornita."
    
    try:
        # Esegui la query
        result = rag_system.query(query_text)
        
        if result['success']:
            # Prepara la risposta
            response = f"RISPOSTA:\n{result['response']}\n\n"
            
            # Aggiungi i riferimenti
            response += "RIFERIMENTI:\n"
            for ref in result['references']:
                response += f"[{ref['id']}] {ref['filename']} (chunk {ref['chunk_id']+1}/{ref['chunk_total']})\n"
                response += f"    Snippet: {ref['snippet']}\n\n"
            
            return response
        else:
            return f"Errore durante l'esecuzione della query: {result['error']}"
    except Exception as e:
        return f"Errore durante l'esecuzione della query: {str(e)}"

# Funzione per ottenere la lista dei documenti nel sistema RAG
def get_document_list():
    try:
        # Ottieni la lista dei documenti
        documents = rag_system.get_document_list()
        
        if not documents:
            return "Nessun documento trovato nel sistema."
        
        # Prepara la risposta
        response = "DOCUMENTI NEL SISTEMA:\n"
        response += "=" * 50 + "\n\n"
        
        for i, doc in enumerate(documents):
            response += f"[{i+1}] {doc['filename']}\n"
            response += f"    ID: {doc['document_id']}\n"
            response += f"    Numero di chunk: {doc['chunk_total']}\n"
            response += f"    Data di elaborazione: {doc['processing_date']}\n\n"
        
        return response
    except Exception as e:
        return f"Errore durante il recupero della lista dei documenti: {str(e)}"

# Funzione per eliminare un documento dal sistema RAG
def delete_document(document_id):
    if not document_id:
        return "Nessun ID documento fornito."
    
    try:
        # Elimina il documento
        result = rag_system.vector_store.delete_document(document_id)
        
        if result['success']:
            return f"Documento con ID '{document_id}' eliminato con successo."
        else:
            return f"Errore durante l'eliminazione del documento: {result['error']}"
    except Exception as e:
        return f"Errore durante l'eliminazione del documento: {str(e)}"

# Crea l'interfaccia Gradio
def create_interface():
    # Crea i tab per le diverse funzionalità
    with gr.Blocks(title="Grafologia Forense") as app:
        gr.Markdown("# Applicazione di Grafologia Forense")
        gr.Markdown("Questa applicazione fornisce strumenti per l'analisi forense di firme e documenti.")
        
        with gr.Tabs():
            # Tab per la pre-elaborazione delle immagini
            with gr.Tab("Pre-elaborazione"):
                with gr.Row():
                    with gr.Column():
                        preprocess_input = gr.Image(label="Immagine da pre-elaborare", type="numpy")
                        preprocess_button = gr.Button("Pre-elabora")
                    with gr.Column():
                        preprocess_output = gr.Image(label="Risultato della pre-elaborazione")
                        preprocess_text = gr.Textbox(label="Output", lines=5)
                
                preprocess_button.click(
                    fn=preprocess_image,
                    inputs=[preprocess_input],
                    outputs=[preprocess_output, preprocess_text]
                )
            
            # Tab per la comparazione di firme
            with gr.Tab("Comparazione Firme"):
                with gr.Row():
                    with gr.Column():
                        compare_input1 = gr.Image(label="Firma 1", type="numpy")
                        compare_input2 = gr.Image(label="Firma 2", type="numpy")
                        compare_button = gr.Button("Confronta")
                    with gr.Column():
                        compare_output = gr.Image(label="Risultato del confronto")
                        compare_text = gr.Textbox(label="Report", lines=10)
                
                compare_button.click(
                    fn=compare_signatures,
                    inputs=[compare_input1, compare_input2],
                    outputs=[compare_output, compare_text]
                )
            
            # Tab per l'analisi di font e inchiostro
            with gr.Tab("Analisi Font e Inchiostro"):
                with gr.Row():
                    with gr.Column():
                        font_input = gr.Image(label="Immagine da analizzare", type="numpy")
                        font_button = gr.Button("Analizza")
                    with gr.Column():
                        font_output = gr.Image(label="Regioni di testo rilevate")
                        font_text = gr.Textbox(label="Report", lines=15)
                
                font_button.click(
                    fn=analyze_font_and_ink,
                    inputs=[font_input],
                    outputs=[font_output, font_text]
                )
            
            # Tab per la misurazione e profilazione
            with gr.Tab("Misurazione e Profilazione"):
                with gr.Row():
                    with gr.Column():
                        measure_input = gr.Image(label="Documento da misurare", type="numpy")
                        measure_button = gr.Button("Misura")
                    with gr.Column():
                        measure_output = gr.Image(label="Risultato della misurazione")
                        measure_text = gr.Textbox(label="Report", lines=15)
                
                measure_button.click(
                    fn=measure_document,
                    inputs=[measure_input],
                    outputs=[measure_output, measure_text]
                )
            
            # Tab per il miglioramento delle immagini
            with gr.Tab("Miglioramento Immagini"):
                with gr.Row():
                    with gr.Column():
                        enhance_input = gr.Image(label="Immagine da migliorare", type="numpy")
                        enhance_type = gr.Radio(
                            label="Tipo di miglioramento",
                            choices=["contrast", "sharpen", "edges", "pressure", "emboss", "heatmap", "all"],
                            value="contrast"
                        )
                        enhance_button = gr.Button("Migliora")
                    with gr.Column():
                        enhance_output = gr.Image(label="Risultato del miglioramento")
                        enhance_text = gr.Textbox(label="Output", lines=5)
                
                enhance_button.click(
                    fn=enhance_image,
                    inputs=[enhance_input, enhance_type],
                    outputs=[enhance_output, enhance_text]
                )
            
            # Tab per il machine learning
            with gr.Tab("Machine Learning"):
                with gr.Tabs():
                    # Subtab per il rilevamento di anomalie
                    with gr.Tab("Rilevamento Anomalie"):
                        with gr.Row():
                            with gr.Column():
                                anomaly_input = gr.Image(label="Firma da analizzare", type="numpy")
                                anomaly_button = gr.Button("Rileva Anomalie")
                            with gr.Column():
                                anomaly_text = gr.Textbox(label="Report", lines=15)
                        
                        anomaly_button.click(
                            fn=detect_anomalies,
                            inputs=[anomaly_input],
                            outputs=[anomaly_text]
                        )
                    
                    # Subtab per la verifica delle firme
                    with gr.Tab("Verifica Firme"):
                        with gr.Row():
                            with gr.Column():
                                verify_input1 = gr.Image(label="Firma 1", type="numpy")
                                verify_input2 = gr.Image(label="Firma 2", type="numpy")
                                verify_button = gr.Button("Verifica")
                            with gr.Column():
                                verify_text = gr.Textbox(label="Report", lines=15)
                        
                        verify_button.click(
                            fn=verify_signatures,
                            inputs=[verify_input1, verify_input2],
                            outputs=[verify_text]
                        )
            
            # Tab per il sistema RAG
            with gr.Tab("Sistema RAG"):
                with gr.Tabs():
                    # Subtab per il caricamento dei documenti
                    with gr.Tab("Caricamento Documenti"):
                        with gr.Row():
                            with gr.Column():
                                upload_input = gr.File(label="Documento da caricare")
                                upload_button = gr.Button("Carica")
                            with gr.Column():
                                upload_text = gr.Textbox(label="Output", lines=5)
                        
                        upload_button.click(
                            fn=upload_document,
                            inputs=[upload_input],
                            outputs=[upload_text]
                        )
                    
                    # Subtab per le query
                    with gr.Tab("Query"):
                        with gr.Row():
                            with gr.Column():
                                query_input = gr.Textbox(label="Query", lines=3)
                                query_button = gr.Button("Esegui Query")
                            with gr.Column():
                                query_text = gr.Textbox(label="Risposta", lines=15)
                        
                        query_button.click(
                            fn=query_rag,
                            inputs=[query_input],
                            outputs=[query_text]
                        )
                    
                    # Subtab per la gestione dei documenti
                    with gr.Tab("Gestione Documenti"):
                        with gr.Row():
                            with gr.Column():
                                list_button = gr.Button("Lista Documenti")
                                delete_input = gr.Textbox(label="ID Documento da eliminare")
                                delete_button = gr.Button("Elimina Documento")
                            with gr.Column():
                                doc_text = gr.Textbox(label="Output", lines=15)
                        
                        list_button.click(
                            fn=get_document_list,
                            inputs=[],
                            outputs=[doc_text]
                        )
                        
                        delete_button.click(
                            fn=delete_document,
                            inputs=[delete_input],
                            outputs=[doc_text]
                        )
    
    return app

# Funzione principale
def main():
    # Crea l'interfaccia
    app = create_interface()
    
    # Avvia l'applicazione
    app.launch(share=True)

if __name__ == "__main__":
    main()
