import cv2
import numpy as np
import matplotlib.pyplot as plt
from .preprocessing import ImagePreprocessor

class MeasurementTool:
    """
    Classe per la misurazione e profilazione di documenti e firme.
    Implementa funzionalità per misurare interlinea, spazi, margini,
    e generare profili di analisi.
    """
    
    def __init__(self):
        """Inizializza lo strumento di misurazione."""
        self.preprocessor = ImagePreprocessor()
    
    def detect_lines(self, image, method='projection'):
        """
        Rileva le linee di testo in un'immagine.
        
        Args:
            image (numpy.ndarray): Immagine di input
            method (str): Metodo di rilevamento ('projection', 'hough')
            
        Returns:
            list: Lista di coordinate y delle linee di testo
        """
        # Converti in scala di grigi se necessario
        if len(image.shape) > 2:
            gray = self.preprocessor.convert_to_grayscale(image)
        else:
            gray = image
        
        # Binarizza l'immagine
        binary = self.preprocessor.threshold_image(gray, method='adaptive')
        
        if method == 'projection':
            # Metodo della proiezione orizzontale
            # Somma i pixel bianchi per ogni riga
            projection = np.sum(binary, axis=1)
            
            # Normalizza la proiezione
            projection = projection / np.max(projection)
            
            # Trova i picchi nella proiezione (linee di testo)
            lines = []
            threshold = 0.3  # Soglia per considerare un picco
            in_line = False
            start_line = 0
            
            for i in range(len(projection)):
                if projection[i] > threshold and not in_line:
                    in_line = True
                    start_line = i
                elif projection[i] <= threshold and in_line:
                    in_line = False
                    mid_line = (start_line + i) // 2
                    lines.append(mid_line)
            
            # Se l'ultima linea non è stata chiusa
            if in_line:
                mid_line = (start_line + len(projection) - 1) // 2
                lines.append(mid_line)
            
        elif method == 'hough':
            # Metodo delle trasformate di Hough
            edges = cv2.Canny(binary, 50, 150, apertureSize=3)
            
            # Rileva le linee
            lines_hough = cv2.HoughLines(edges, 1, np.pi/180, threshold=100)
            
            # Filtra le linee orizzontali
            lines = []
            if lines_hough is not None:
                for line in lines_hough:
                    rho, theta = line[0]
                    # Considera solo le linee orizzontali (theta vicino a 0 o pi)
                    if (theta < 0.1 or abs(theta - np.pi) < 0.1):
                        a = np.cos(theta)
                        b = np.sin(theta)
                        x0 = a * rho
                        y0 = b * rho
                        # y = (rho - x * cos(theta)) / sin(theta)
                        # Per linee orizzontali, y è costante
                        y = int(y0)
                        lines.append(y)
            
            # Ordina le linee per posizione y
            lines.sort()
        else:
            raise ValueError(f"Metodo di rilevamento linee non supportato: {method}")
        
        return lines
    
    def measure_line_spacing(self, image):
        """
        Misura lo spazio tra le linee di testo.
        
        Args:
            image (numpy.ndarray): Immagine di input
            
        Returns:
            dict: Informazioni sullo spazio tra le linee
        """
        # Rileva le linee
        lines = self.detect_lines(image)
        
        if len(lines) < 2:
            return {
                'line_count': len(lines),
                'average_spacing': 0,
                'spacing_std': 0,
                'line_positions': lines,
                'spacing_values': []
            }
        
        # Calcola lo spazio tra le linee consecutive
        spacing = [lines[i+1] - lines[i] for i in range(len(lines)-1)]
        
        return {
            'line_count': len(lines),
            'average_spacing': np.mean(spacing),
            'spacing_std': np.std(spacing),
            'line_positions': lines,
            'spacing_values': spacing
        }
    
    def detect_word_boundaries(self, image, line_positions=None):
        """
        Rileva i confini delle parole in un'immagine.
        
        Args:
            image (numpy.ndarray): Immagine di input
            line_positions (list, optional): Posizioni y delle linee di testo
            
        Returns:
            list: Lista di tuple (linea, x_inizio, x_fine) per ogni parola
        """
        # Converti in scala di grigi se necessario
        if len(image.shape) > 2:
            gray = self.preprocessor.convert_to_grayscale(image)
        else:
            gray = image
        
        # Binarizza l'immagine
        binary = self.preprocessor.threshold_image(gray, method='adaptive')
        
        # Se non sono fornite le posizioni delle linee, rilevale
        if line_positions is None:
            line_positions = self.detect_lines(binary)
        
        # Se non ci sono linee, restituisci una lista vuota
        if not line_positions:
            return []
        
        # Calcola l'altezza media delle linee
        line_height = 30  # Valore predefinito
        if len(line_positions) > 1:
            line_height = int(np.mean([line_positions[i+1] - line_positions[i] 
                                      for i in range(len(line_positions)-1)]))
        
        # Rileva le parole per ogni linea
        words = []
        for i, y in enumerate(line_positions):
            # Estrai una regione intorno alla linea
            y_start = max(0, y - line_height // 2)
            y_end = min(binary.shape[0], y + line_height // 2)
            line_region = binary[y_start:y_end, :]
            
            # Proiezione verticale (somma i pixel bianchi per ogni colonna)
            projection = np.sum(line_region, axis=0)
            
            # Normalizza la proiezione
            if np.max(projection) > 0:
                projection = projection / np.max(projection)
            
            # Trova i confini delle parole
            threshold = 0.1  # Soglia per considerare uno spazio
            in_word = False
            start_word = 0
            
            for j in range(len(projection)):
                if projection[j] > threshold and not in_word:
                    in_word = True
                    start_word = j
                elif projection[j] <= threshold and in_word:
                    in_word = False
                    words.append((i, start_word, j))
            
            # Se l'ultima parola non è stata chiusa
            if in_word:
                words.append((i, start_word, len(projection) - 1))
        
        return words
    
    def measure_word_spacing(self, image):
        """
        Misura lo spazio tra le parole.
        
        Args:
            image (numpy.ndarray): Immagine di input
            
        Returns:
            dict: Informazioni sullo spazio tra le parole
        """
        # Rileva le linee
        lines = self.detect_lines(image)
        
        # Rileva i confini delle parole
        words = self.detect_word_boundaries(image, lines)
        
        # Calcola lo spazio tra le parole consecutive sulla stessa linea
        spacing = []
        for i in range(len(words)-1):
            line1, _, end1 = words[i]
            line2, start2, _ = words[i+1]
            
            # Considera solo le parole sulla stessa linea
            if line1 == line2:
                space = start2 - end1
                if space > 0:  # Ignora sovrapposizioni
                    spacing.append(space)
        
        if not spacing:
            return {
                'word_count': len(words),
                'average_spacing': 0,
                'spacing_std': 0,
                'spacing_values': []
            }
        
        return {
            'word_count': len(words),
            'average_spacing': np.mean(spacing),
            'spacing_std': np.std(spacing),
            'spacing_values': spacing
        }
    
    def detect_margins(self, image):
        """
        Rileva i margini del documento.
        
        Args:
            image (numpy.ndarray): Immagine di input
            
        Returns:
            dict: Informazioni sui margini (sinistra, destra, superiore, inferiore)
        """
        # Converti in scala di grigi se necessario
        if len(image.shape) > 2:
            gray = self.preprocessor.convert_to_grayscale(image)
        else:
            gray = image
        
        # Binarizza l'immagine
        binary = self.preprocessor.threshold_image(gray, method='adaptive')
        
        # Inverti l'immagine (testo bianco su sfondo nero)
        binary_inv = cv2.bitwise_not(binary)
        
        # Proiezione orizzontale (somma i pixel bianchi per ogni riga)
        h_projection = np.sum(binary_inv, axis=1)
        
        # Proiezione verticale (somma i pixel bianchi per ogni colonna)
        v_projection = np.sum(binary_inv, axis=0)
        
        # Normalizza le proiezioni
        if np.max(h_projection) > 0:
            h_projection = h_projection / np.max(h_projection)
        if np.max(v_projection) > 0:
            v_projection = v_projection / np.max(v_projection)
        
        # Trova i margini
        threshold = 0.05  # Soglia per considerare un margine
        
        # Margine superiore
        top_margin = 0
        while top_margin < len(h_projection) and h_projection[top_margin] <= threshold:
            top_margin += 1
        
        # Margine inferiore
        bottom_margin = len(h_projection) - 1
        while bottom_margin >= 0 and h_projection[bottom_margin] <= threshold:
            bottom_margin -= 1
        bottom_margin = len(h_projection) - 1 - bottom_margin
        
        # Margine sinistro
        left_margin = 0
        while left_margin < len(v_projection) and v_projection[left_margin] <= threshold:
            left_margin += 1
        
        # Margine destro
        right_margin = len(v_projection) - 1
        while right_margin >= 0 and v_projection[right_margin] <= threshold:
            right_margin -= 1
        right_margin = len(v_projection) - 1 - right_margin
        
        return {
            'top': top_margin,
            'bottom': bottom_margin,
            'left': left_margin,
            'right': right_margin
        }
    
    def measure_character_slant(self, image):
        """
        Misura l'inclinazione dei caratteri.
        
        Args:
            image (numpy.ndarray): Immagine di input
            
        Returns:
            dict: Informazioni sull'inclinazione dei caratteri
        """
        # Converti in scala di grigi se necessario
        if len(image.shape) > 2:
            gray = self.preprocessor.convert_to_grayscale(image)
        else:
            gray = image
        
        # Binarizza l'immagine
        binary = self.preprocessor.threshold_image(gray, method='adaptive')
        
        # Applica la trasformata di Hough probabilistica
        edges = cv2.Canny(binary, 50, 150, apertureSize=3)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=15, maxLineGap=10)
        
        if lines is None:
            return {
                'average_slant': 0,
                'slant_std': 0,
                'slant_values': []
            }
        
        # Calcola l'angolo di inclinazione per ogni linea
        angles = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            
            # Ignora le linee orizzontali
            if abs(x2 - x1) > 5:
                # Calcola l'angolo in gradi
                angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
                
                # Considera solo gli angoli tra -45 e 45 gradi (caratteri inclinati)
                if -45 <= angle <= 45:
                    angles.append(angle)
        
        if not angles:
            return {
                'average_slant': 0,
                'slant_std': 0,
                'slant_values': []
            }
        
        return {
            'average_slant': np.mean(angles),
            'slant_std': np.std(angles),
            'slant_values': angles
        }
    
    def analyze_pressure_profile(self, image):
        """
        Analizza il profilo di pressione in un'immagine.
        
        Args:
            image (numpy.ndarray): Immagine di input
            
        Returns:
            dict: Informazioni sul profilo di pressione
        """
        # Converti in scala di grigi se necessario
        if len(image.shape) > 2:
            gray = self.preprocessor.convert_to_grayscale(image)
        else:
            gray = image
        
        # Inverti l'immagine (testo bianco su sfondo nero)
        gray_inv = cv2.bitwise_not(gray)
        
        # Applica una soglia per isolare il testo
        _, binary = cv2.threshold(gray_inv, 50, 255, cv2.THRESH_BINARY)
        
        # Calcola l'intensità media dei pixel di testo
        text_pixels = gray_inv[binary > 0]
        
        if len(text_pixels) == 0:
            return {
                'average_pressure': 0,
                'pressure_std': 0,
                'pressure_histogram': None
            }
        
        # Calcola l'istogramma dell'intensità
        hist, bins = np.histogram(text_pixels, bins=50, range=(0, 255))
        
        # Normalizza l'istogramma
        hist = hist / np.sum(hist)
        
        # Calcola la pressione media (intensità media)
        average_pressure = np.mean(text_pixels)
        
        # Calcola la deviazione standard della pressione
        pressure_std = np.std(text_pixels)
        
        return {
            'average_pressure': float(average_pressure),
            'pressure_std': float(pressure_std),
            'pressure_histogram': {
                'hist': hist.tolist(),
                'bins': bins.tolist()
            }
        }
    
    def generate_measurement_report(self, image):
        """
        Genera un report completo di misurazione per un'immagine.
        
        Args:
            image (numpy.ndarray): Immagine di input
            
        Returns:
            dict: Report completo di misurazione
        """
        # Carica l'immagine se è un percorso file
        if isinstance(image, str):
            image = self.preprocessor.load_image(image)
        
        # Misura lo spazio tra le linee
        line_spacing = self.measure_line_spacing(image)
        
        # Misura lo spazio tra le parole
        word_spacing = self.measure_word_spacing(image)
        
        # Rileva i margini
        margins = self.detect_margins(image)
        
        # Misura l'inclinazione dei caratteri
        slant = self.measure_character_slant(image)
        
        # Analizza il profilo di pressione
        pressure = self.analyze_pressure_profile(image)
        
        return {
            'line_spacing': line_spacing,
            'word_spacing': word_spacing,
            'margins': margins,
            'character_slant': slant,
            'pressure_profile': pressure
        }
    
    def visualize_measurements(self, image, measurements, save_path=None):
        """
        Visualizza le misurazioni su un'immagine.
        
        Args:
            image (numpy.ndarray): Immagine di input
            measurements (dict): Risultato di generate_measurement_report
            save_path (str, optional): Percorso dove salvare l'immagine
            
        Returns:
            matplotlib.figure.Figure: Figura con la visualizzazione
        """
        # Crea una copia dell'immagine per la visualizzazione
        if len(image.shape) == 2:
            # Converti in BGR se è in scala di grigi
            vis_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        else:
            vis_image = image.copy()
        
        # Converti in RGB per matplotlib
        vis_image_rgb = cv2.cvtColor(vis_image, cv2.COLOR_BGR2RGB)
        
        # Crea una figura con più sottografici
        fig, axs = plt.subplots(2, 2, figsize=(15, 12))
        
        # Immagine con linee di testo
        axs[0, 0].imshow(vis_image_rgb)
        axs[0, 0].set_title('Linee di Testo e Margini')
        
        # Disegna le linee di testo
        for y in measurements['line_spacing']['line_positions']:
            axs[0, 0].axhline(y=y, color='r', linestyle='-', alpha=0.5)
        
        # Disegna i margini
        margins = measurements['margins']
        h, w = image.shape[:2]
        
        # Margine superiore
        axs[0, 0].axhline(y=margins['top'], color='g', linestyle='--')
        # Margine inferiore
        axs[0, 0].axhline(y=h - margins['bottom'], color='g', linestyle='--')
        # Margine sinistro
        axs[0, 0].axvline(x=margins['left'], color='g', linestyle='--')
        # Margine destro
        axs[0, 0].axvline(x=w - margins['right'], color='g', linestyle='--')
        
        axs[0, 0].axis('off')
        
        # Grafico dell'inclinazione dei caratteri
        if measurements['character_slant']['slant_values']:
            axs[0, 1].hist(measurements['character_slant']['slant_values'], bins=20, 
                          range=(-45, 45), color='blue', alpha=0.7)
            axs[0, 1].axvline(x=measurements['character_slant']['average_slant'], 
                             color='r', linestyle='-', linewidth=2)
            axs[0, 1].set_title(f"Inclinazione dei Caratteri: {measurements['character_slant']['average_slant']:.1f}°")
            axs[0, 1].set_xlabel('Angolo (gradi)')
            axs[0, 1].set_ylabel('Frequenza')
        else:
            axs[0, 1].text(0.5, 0.5, 'Dati di inclinazione non disponibili', 
                          horizontalalignment='center', verticalalignment='center')
            axs[0, 1].set_title('Inclinazione dei Caratteri')
        
        # Grafico del profilo di pressione
        if measurements['pressure_profile']['pressure_histogram'] is not None:
            hist = measurements['pressure_profile']['pressure_histogram']['hist']
            bins = measurements['pressure_profile']['pressure_histogram']['bins']
            bin_centers = 0.5 * (bins[:-1] + bins[1:])
            
            axs[1, 0].bar(bin_centers, hist, width=bins[1] - bins[0], color='green', alpha=0.7)
            axs[1, 0].axvline(x=measurements['pressure_profile']['average_pressure'], 
                             color='r', linestyle='-', linewidth=2)
            axs[1, 0].set_title(f"Profilo di Pressione: {measurements['pressure_profile']['average_pressure']:.1f}")
            axs[1, 0].set_xlabel('Intensità')
            axs[1, 0].set_ylabel('Frequenza Normalizzata')
        else:
            axs[1, 0].text(0.5, 0.5, 'Dati di pressione non disponibili', 
                          horizontalalignment='center', verticalalignment='center')
            axs[1, 0].set_title('Profilo di Pressione')
        
        # Tabella con le misurazioni
        axs[1, 1].axis('tight')
        axs[1, 1].axis('off')
        
        table_data = [
            ['Metrica', 'Valore'],
            ['Numero di Linee', f"{measurements['line_spacing']['line_count']}"],
            ['Spazio Medio tra Linee', f"{measurements['line_spacing']['average_spacing']:.1f} px"],
            ['Numero di Parole', f"{measurements['word_spacing']['word_count']}"],
            ['Spazio Medio tra Parole', f"{measurements['word_spacing']['average_spacing']:.1f} px"],
            ['Margine Superiore', f"{margins['top']} px"],
            ['Margine Inferiore', f"{margins['bottom']} px"],
            ['Margine Sinistro', f"{margins['left']} px"],
            ['Margine Destro', f"{margins['right']} px"],
            ['Inclinazione Media', f"{measurements['character_slant']['average_slant']:.1f}°"],
            ['Pressione Media', f"{measurements['pressure_profile']['average_pressure']:.1f}"]
        ]
        
        table = axs[1, 1].table(cellText=table_data, loc='center', cellLoc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)
        axs[1, 1].set_title('Riepilogo Misurazioni')
        
        plt.tight_layout()
        
        # Salva l'immagine se richiesto
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def create_digital_ruler(self, image, dpi=96, save_path=None):
        """
        Crea un righello digitale sovrapposto all'immagine.
        
        Args:
            image (numpy.ndarray): Immagine di input
            dpi (int): Punti per pollice (per la conversione in unità fisiche)
            save_path (str, optional): Percorso dove salvare l'immagine
            
        Returns:
            numpy.ndarray: Immagine con righello sovrapposto
        """
        # Crea una copia dell'immagine per la visualizzazione
        if len(image.shape) == 2:
            # Converti in BGR se è in scala di grigi
            vis_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        else:
            vis_image = image.copy()
        
        # Dimensioni dell'immagine
        h, w = image.shape[:2]
        
        # Calcola la scala (pixel per millimetro)
        pixels_per_mm = dpi / 25.4  # 25.4 mm = 1 pollice
        
        # Disegna il righello orizzontale
        y_ruler = 30  # Posizione y del righello orizzontale
        
        # Disegna la linea principale
        cv2.line(vis_image, (0, y_ruler), (w, y_ruler), (0, 0, 255), 2)
        
        # Disegna le tacche principali (ogni 10 mm)
        for x in range(0, w, int(10 * pixels_per_mm)):
            cv2.line(vis_image, (x, y_ruler - 10), (x, y_ruler + 10), (0, 0, 255), 2)
            # Aggiungi l'etichetta (in mm)
            label = f"{int(x / pixels_per_mm)}"
            cv2.putText(vis_image, label, (x - 10, y_ruler - 15), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
        # Disegna le tacche secondarie (ogni 1 mm)
        for x in range(0, w, int(1 * pixels_per_mm)):
            cv2.line(vis_image, (x, y_ruler - 5), (x, y_ruler + 5), (0, 0, 255), 1)
        
        # Disegna il righello verticale
        x_ruler = 30  # Posizione x del righello verticale
        
        # Disegna la linea principale
        cv2.line(vis_image, (x_ruler, 0), (x_ruler, h), (0, 0, 255), 2)
        
        # Disegna le tacche principali (ogni 10 mm)
        for y in range(0, h, int(10 * pixels_per_mm)):
            cv2.line(vis_image, (x_ruler - 10, y), (x_ruler + 10, y), (0, 0, 255), 2)
            # Aggiungi l'etichetta (in mm)
            label = f"{int(y / pixels_per_mm)}"
            cv2.putText(vis_image, label, (x_ruler - 30, y + 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
        # Disegna le tacche secondarie (ogni 1 mm)
        for y in range(0, h, int(1 * pixels_per_mm)):
            cv2.line(vis_image, (x_ruler - 5, y), (x_ruler + 5, y), (0, 0, 255), 1)
        
        # Aggiungi informazioni sulla scala
        scale_info = f"Scala: 1 pixel = {1/pixels_per_mm:.3f} mm (DPI: {dpi})"
        cv2.putText(vis_image, scale_info, (w - 300, h - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
        
        # Salva l'immagine se richiesto
        if save_path:
            cv2.imwrite(save_path, vis_image)
        
        return vis_image
