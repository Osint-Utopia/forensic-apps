import cv2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from .preprocessing import ImagePreprocessor

class SignatureAnalyzer:
    """
    Classe per l'analisi e la comparazione di firme.
    Implementa funzionalità per estrarre caratteristiche dalle firme,
    confrontarle e calcolare metriche di similarità.
    """
    
    def __init__(self):
        """Inizializza l'analizzatore di firme."""
        self.preprocessor = ImagePreprocessor()
    
    def extract_contours(self, binary_image):
        """
        Estrae i contorni da un'immagine binaria.
        
        Args:
            binary_image (numpy.ndarray): Immagine binaria
            
        Returns:
            list: Lista di contorni
        """
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours
    
    def extract_features_orb(self, image, n_features=1000):
        """
        Estrae caratteristiche ORB (Oriented FAST and Rotated BRIEF) da un'immagine.
        
        Args:
            image (numpy.ndarray): Immagine di input
            n_features (int): Numero di caratteristiche da estrarre
            
        Returns:
            tuple: (keypoints, descriptors)
        """
        # Converti in scala di grigi se necessario
        if len(image.shape) > 2:
            gray = self.preprocessor.convert_to_grayscale(image)
        else:
            gray = image
        
        # Inizializza il rilevatore ORB
        orb = cv2.ORB_create(nfeatures=n_features)
        
        # Rileva keypoints e calcola i descrittori
        keypoints, descriptors = orb.detectAndCompute(gray, None)
        
        return keypoints, descriptors
    
    def match_features(self, desc1, desc2, method='bf'):
        """
        Confronta i descrittori di due immagini.
        
        Args:
            desc1 (numpy.ndarray): Descrittori della prima immagine
            desc2 (numpy.ndarray): Descrittori della seconda immagine
            method (str): Metodo di matching ('bf' per Brute Force, 'flann' per FLANN)
            
        Returns:
            list: Lista di corrispondenze
        """
        if desc1 is None or desc2 is None:
            return []
        
        if method == 'bf':
            # Brute Force Matcher con norma di Hamming (per descrittori binari come ORB)
            matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = matcher.match(desc1, desc2)
            
            # Ordina le corrispondenze in base alla distanza
            matches = sorted(matches, key=lambda x: x.distance)
            
        elif method == 'flann':
            # FLANN Matcher (più veloce per dataset di grandi dimensioni)
            # Converti i descrittori in float32 se necessario
            if desc1.dtype != np.float32:
                desc1 = np.float32(desc1)
            if desc2.dtype != np.float32:
                desc2 = np.float32(desc2)
                
            FLANN_INDEX_LSH = 6
            index_params = dict(algorithm=FLANN_INDEX_LSH,
                               table_number=6,
                               key_size=12,
                               multi_probe_level=1)
            search_params = dict(checks=50)
            
            flann = cv2.FlannBasedMatcher(index_params, search_params)
            matches = flann.knnMatch(desc1, desc2, k=2)
            
            # Applica il test del rapporto di Lowe
            good_matches = []
            for pair in matches:
                if len(pair) == 2:
                    m, n = pair
                    if m.distance < 0.7 * n.distance:
                        good_matches.append(m)
            matches = good_matches
        else:
            raise ValueError(f"Metodo di matching non supportato: {method}")
        
        return matches
    
    def calculate_similarity_score(self, matches, kp1, kp2):
        """
        Calcola un punteggio di similarità basato sulle corrispondenze.
        
        Args:
            matches (list): Lista di corrispondenze
            kp1 (list): Keypoints della prima immagine
            kp2 (list): Keypoints della seconda immagine
            
        Returns:
            float: Punteggio di similarità (0-100)
        """
        if len(matches) == 0 or len(kp1) == 0 or len(kp2) == 0:
            return 0.0
        
        # Calcola il punteggio come rapporto tra il numero di corrispondenze e il minimo numero di keypoints
        score = 100.0 * len(matches) / min(len(kp1), len(kp2))
        
        return min(score, 100.0)  # Limita il punteggio a 100
    
    def extract_signature_metrics(self, binary_image):
        """
        Estrae metriche grafometriche da una firma.
        
        Args:
            binary_image (numpy.ndarray): Immagine binaria della firma
            
        Returns:
            dict: Dizionario di metriche
        """
        # Estrai i contorni
        contours = self.extract_contours(binary_image)
        
        if not contours:
            return {
                'area': 0,
                'perimeter': 0,
                'width': 0,
                'height': 0,
                'aspect_ratio': 0,
                'density': 0,
                'slant_angle': 0
            }
        
        # Trova il contorno più grande (la firma)
        signature_contour = max(contours, key=cv2.contourArea)
        
        # Calcola l'area
        area = cv2.contourArea(signature_contour)
        
        # Calcola il perimetro
        perimeter = cv2.arcLength(signature_contour, True)
        
        # Calcola il rettangolo delimitatore
        x, y, w, h = cv2.boundingRect(signature_contour)
        
        # Calcola il rapporto d'aspetto
        aspect_ratio = float(w) / h if h > 0 else 0
        
        # Calcola la densità (area / area del rettangolo delimitatore)
        density = area / (w * h) if w * h > 0 else 0
        
        # Calcola l'angolo di inclinazione
        # Utilizziamo l'ellisse che meglio approssima il contorno
        if len(signature_contour) >= 5:  # Servono almeno 5 punti per adattare un'ellisse
            ellipse = cv2.fitEllipse(signature_contour)
            # L'angolo è in gradi, 0-180
            slant_angle = ellipse[2]
            # Normalizziamo l'angolo a -90 - +90 gradi
            if slant_angle > 90:
                slant_angle = slant_angle - 180
        else:
            slant_angle = 0
        
        return {
            'area': area,
            'perimeter': perimeter,
            'width': w,
            'height': h,
            'aspect_ratio': aspect_ratio,
            'density': density,
            'slant_angle': slant_angle
        }
    
    def compare_signatures(self, image_path1, image_path2):
        """
        Confronta due firme e calcola metriche di similarità.
        
        Args:
            image_path1 (str): Percorso della prima immagine
            image_path2 (str): Percorso della seconda immagine
            
        Returns:
            dict: Risultati del confronto
        """
        # Pre-elabora le firme
        sig1_processed = self.preprocessor.preprocess_signature(image_path1)
        sig2_processed = self.preprocessor.preprocess_signature(image_path2)
        
        # Estrai caratteristiche ORB
        kp1, desc1 = self.extract_features_orb(sig1_processed['binary'])
        kp2, desc2 = self.extract_features_orb(sig2_processed['binary'])
        
        # Trova le corrispondenze
        matches = self.match_features(desc1, desc2, method='bf')
        
        # Calcola il punteggio di similarità
        similarity_score = self.calculate_similarity_score(matches, kp1, kp2)
        
        # Estrai metriche grafometriche
        metrics1 = self.extract_signature_metrics(sig1_processed['binary'])
        metrics2 = self.extract_signature_metrics(sig2_processed['binary'])
        
        # Calcola le differenze tra le metriche
        metric_diffs = {
            'area_diff': abs(metrics1['area'] - metrics2['area']) / max(metrics1['area'], metrics2['area'], 1) * 100,
            'perimeter_diff': abs(metrics1['perimeter'] - metrics2['perimeter']) / max(metrics1['perimeter'], metrics2['perimeter'], 1) * 100,
            'aspect_ratio_diff': abs(metrics1['aspect_ratio'] - metrics2['aspect_ratio']) / max(metrics1['aspect_ratio'], metrics2['aspect_ratio'], 1) * 100,
            'density_diff': abs(metrics1['density'] - metrics2['density']) / max(metrics1['density'], metrics2['density'], 1) * 100,
            'slant_angle_diff': abs(metrics1['slant_angle'] - metrics2['slant_angle'])
        }
        
        # Calcola un punteggio di similarità basato sulle metriche
        # Minore è la differenza, maggiore è la similarità
        metric_similarity = 100 - (
            0.2 * metric_diffs['area_diff'] +
            0.2 * metric_diffs['perimeter_diff'] +
            0.2 * metric_diffs['aspect_ratio_diff'] +
            0.2 * metric_diffs['density_diff'] +
            0.2 * min(metric_diffs['slant_angle_diff'] / 90 * 100, 100)  # Normalizza la differenza di angolo
        )
        
        # Combina i punteggi (50% feature matching, 50% metriche)
        combined_score = 0.5 * similarity_score + 0.5 * metric_similarity
        
        return {
            'feature_similarity': similarity_score,
            'metric_similarity': metric_similarity,
            'combined_score': combined_score,
            'metrics1': metrics1,
            'metrics2': metrics2,
            'metric_differences': metric_diffs,
            'keypoints1': len(kp1),
            'keypoints2': len(kp2),
            'matches': len(matches),
            'processed_images': {
                'signature1': sig1_processed,
                'signature2': sig2_processed
            }
        }
    
    def visualize_comparison(self, comparison_result, save_path=None):
        """
        Visualizza il confronto tra due firme.
        
        Args:
            comparison_result (dict): Risultato del confronto
            save_path (str, optional): Percorso dove salvare l'immagine
            
        Returns:
            matplotlib.figure.Figure: Figura con la visualizzazione
        """
        # Crea una figura con più sottografici
        fig, axs = plt.subplots(2, 3, figsize=(15, 10))
        
        # Immagini originali
        axs[0, 0].imshow(cv2.cvtColor(comparison_result['processed_images']['signature1']['original'], cv2.COLOR_BGR2RGB))
        axs[0, 0].set_title('Firma 1 (Originale)')
        axs[0, 0].axis('off')
        
        axs[0, 1].imshow(cv2.cvtColor(comparison_result['processed_images']['signature2']['original'], cv2.COLOR_BGR2RGB))
        axs[0, 1].set_title('Firma 2 (Originale)')
        axs[0, 1].axis('off')
        
        # Immagini binarie
        axs[0, 2].imshow(comparison_result['processed_images']['signature1']['binary'], cmap='gray')
        axs[0, 2].set_title('Firma 1 (Binaria)')
        axs[0, 2].axis('off')
        
        axs[1, 0].imshow(comparison_result['processed_images']['signature2']['binary'], cmap='gray')
        axs[1, 0].set_title('Firma 2 (Binaria)')
        axs[1, 0].axis('off')
        
        # Grafico a barre per i punteggi di similarità
        scores = ['Feature Similarity', 'Metric Similarity', 'Combined Score']
        values = [comparison_result['feature_similarity'], 
                 comparison_result['metric_similarity'], 
                 comparison_result['combined_score']]
        
        axs[1, 1].bar(scores, values, color=['blue', 'green', 'red'])
        axs[1, 1].set_ylim(0, 100)
        axs[1, 1].set_ylabel('Punteggio (%)')
        axs[1, 1].set_title('Punteggi di Similarità')
        
        # Tabella con le metriche
        metrics_table = [
            ['Metrica', 'Firma 1', 'Firma 2', 'Diff (%)'],
            ['Area', f"{comparison_result['metrics1']['area']:.1f}", f"{comparison_result['metrics2']['area']:.1f}", 
             f"{comparison_result['metric_differences']['area_diff']:.1f}"],
            ['Perimetro', f"{comparison_result['metrics1']['perimeter']:.1f}", f"{comparison_result['metrics2']['perimeter']:.1f}", 
             f"{comparison_result['metric_differences']['perimeter_diff']:.1f}"],
            ['Rapporto Aspetto', f"{comparison_result['metrics1']['aspect_ratio']:.2f}", f"{comparison_result['metrics2']['aspect_ratio']:.2f}", 
             f"{comparison_result['metric_differences']['aspect_ratio_diff']:.1f}"],
            ['Densità', f"{comparison_result['metrics1']['density']:.2f}", f"{comparison_result['metrics2']['density']:.2f}", 
             f"{comparison_result['metric_differences']['density_diff']:.1f}"],
            ['Inclinazione (°)', f"{comparison_result['metrics1']['slant_angle']:.1f}", f"{comparison_result['metrics2']['slant_angle']:.1f}", 
             f"{comparison_result['metric_differences']['slant_angle_diff']:.1f}"]
        ]
        
        axs[1, 2].axis('tight')
        axs[1, 2].axis('off')
        table = axs[1, 2].table(cellText=metrics_table, loc='center', cellLoc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 1.5)
        
        # Aggiungi un titolo generale
        plt.suptitle(f"Analisi Comparativa delle Firme - Score: {comparison_result['combined_score']:.1f}%", 
                    fontsize=16)
        
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        
        # Salva l'immagine se richiesto
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def generate_comparison_report(self, comparison_result):
        """
        Genera un report testuale del confronto tra firme.
        
        Args:
            comparison_result (dict): Risultato del confronto
            
        Returns:
            str: Report testuale
        """
        report = []
        report.append("REPORT DI ANALISI COMPARATIVA DELLE FIRME")
        report.append("=" * 50)
        report.append("")
        
        # Punteggi di similarità
        report.append("PUNTEGGI DI SIMILARITÀ:")
        report.append(f"- Similarità delle caratteristiche: {comparison_result['feature_similarity']:.2f}%")
        report.append(f"- Similarità delle metriche: {comparison_result['metric_similarity']:.2f}%")
        report.append(f"- Punteggio combinato: {comparison_result['combined_score']:.2f}%")
        report.append("")
        
        # Interpretazione del punteggio
        if comparison_result['combined_score'] >= 85:
            interpretation = "ALTA probabilità che le firme provengano dalla stessa persona."
        elif comparison_result['combined_score'] >= 70:
            interpretation = "MEDIA-ALTA probabilità che le firme provengano dalla stessa persona."
        elif comparison_result['combined_score'] >= 50:
            interpretation = "MEDIA probabilità che le firme provengano dalla stessa persona."
        elif comparison_result['combined_score'] >= 30:
            interpretation = "BASSA probabilità che le firme provengano dalla stessa persona."
        else:
            interpretation = "MOLTO BASSA probabilità che le firme provengano dalla stessa persona."
        
        report.append(f"INTERPRETAZIONE: {interpretation}")
        report.append("")
        
        # Dettagli tecnici
        report.append("DETTAGLI TECNICI:")
        report.append(f"- Punti chiave rilevati nella Firma 1: {comparison_result['keypoints1']}")
        report.append(f"- Punti chiave rilevati nella Firma 2: {comparison_result['keypoints2']}")
        report.append(f"- Corrispondenze trovate: {comparison_result['matches']}")
        report.append("")
        
        # Metriche grafometriche
        report.append("METRICHE GRAFOMETRICHE:")
        report.append(f"{'Metrica':<20} {'Firma 1':<15} {'Firma 2':<15} {'Differenza (%)':<15}")
        report.append("-" * 65)
        
        metrics = [
            ('Area', comparison_result['metrics1']['area'], comparison_result['metrics2']['area'], 
             comparison_result['metric_differences']['area_diff']),
            ('Perimetro', comparison_result['metrics1']['perimeter'], comparison_result['metrics2']['perimeter'], 
             comparison_result['metric_differences']['perimeter_diff']),
            ('Larghezza', comparison_result['metrics1']['width'], comparison_result['metrics2']['width'], 
             abs(comparison_result['metrics1']['width'] - comparison_result['metrics2']['width']) / 
             max(comparison_result['metrics1']['width'], comparison_result['metrics2']['width'], 1) * 100),
            ('Altezza', comparison_result['metrics1']['height'], comparison_result['metrics2']['height'], 
             abs(comparison_result['metrics1']['height'] - comparison_result['metrics2']['height']) / 
             max(comparison_result['metrics1']['height'], comparison_result['metrics2']['height'], 1) * 100),
            ('Rapporto Aspetto', comparison_result['metrics1']['aspect_ratio'], comparison_result['metrics2']['aspect_ratio'], 
             comparison_result['metric_differences']['aspect_ratio_diff']),
            ('Densità', comparison_result['metrics1']['density'], comparison_result['metrics2']['density'], 
             comparison_result['metric_differences']['density_diff']),
            ('Inclinazione (°)', comparison_result['metrics1']['slant_angle'], comparison_result['metrics2']['slant_angle'], 
             comparison_result['metric_differences']['slant_angle_diff'])
        ]
        
        for name, val1, val2, diff in metrics:
            report.append(f"{name:<20} {val1:<15.2f} {val2:<15.2f} {diff:<15.2f}")
        
        report.append("")
        report.append("NOTA: Questo report è generato automaticamente e deve essere interpretato da un esperto di grafologia forense.")
        
        return "\n".join(report)
