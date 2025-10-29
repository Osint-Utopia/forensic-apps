import cv2
import numpy as np
import pytesseract
from .preprocessing import ImagePreprocessor

class FontAnalyzer:
    """
    Classe per l'analisi dei font e il riconoscimento del tipo di inchiostro.
    Implementa funzionalità per identificare i font utilizzati nei documenti
    e analizzare le caratteristiche dell'inchiostro.
    """
    
    def __init__(self):
        """Inizializza l'analizzatore di font."""
        self.preprocessor = ImagePreprocessor()
    
    def detect_text_regions(self, image):
        """
        Rileva le regioni di testo in un'immagine.
        
        Args:
            image (numpy.ndarray): Immagine di input
            
        Returns:
            list: Lista di rettangoli (x, y, w, h) che contengono testo
        """
        # Converti in scala di grigi se necessario
        if len(image.shape) > 2:
            gray = self.preprocessor.convert_to_grayscale(image)
        else:
            gray = image
        
        # Applica soglia per binarizzare l'immagine
        binary = self.preprocessor.threshold_image(gray, method='adaptive')
        
        # Applica operazioni morfologiche per connettere i componenti del testo
        kernel = np.ones((5, 1), np.uint8)  # Kernel rettangolare orizzontale
        dilated = cv2.dilate(binary, kernel, iterations=2)
        
        # Trova i contorni
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filtra i contorni per dimensione
        text_regions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filtra i contorni troppo piccoli
            if w > 20 and h > 8 and w > h:  # Probabilmente testo
                text_regions.append((x, y, w, h))
        
        return text_regions
    
    def extract_text(self, image, text_regions=None):
        """
        Estrae il testo da un'immagine utilizzando OCR.
        
        Args:
            image (numpy.ndarray): Immagine di input
            text_regions (list, optional): Lista di regioni di testo (x, y, w, h)
            
        Returns:
            dict: Dizionario con il testo estratto e le informazioni sulle regioni
        """
        # Se non sono fornite regioni di testo, rileva automaticamente
        if text_regions is None:
            text_regions = self.detect_text_regions(image)
        
        # Converti in scala di grigi se necessario
        if len(image.shape) > 2:
            gray = self.preprocessor.convert_to_grayscale(image)
        else:
            gray = image
        
        # Prepara il risultato
        result = {
            'full_text': '',
            'regions': []
        }
        
        # Estrai il testo da ciascuna regione
        for i, (x, y, w, h) in enumerate(text_regions):
            # Estrai la regione
            roi = gray[y:y+h, x:x+w]
            
            # Applica miglioramenti all'immagine per OCR
            roi = cv2.resize(roi, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            roi = cv2.GaussianBlur(roi, (5, 5), 0)
            roi = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            
            # Esegui OCR
            text = pytesseract.image_to_string(roi, config='--psm 6')
            
            # Aggiungi al risultato
            if text.strip():
                result['full_text'] += text + '\n'
                result['regions'].append({
                    'id': i,
                    'bbox': (x, y, w, h),
                    'text': text.strip()
                })
        
        return result
    
    def analyze_font(self, image, text_regions=None):
        """
        Analizza i font presenti in un'immagine.
        
        Args:
            image (numpy.ndarray): Immagine di input
            text_regions (list, optional): Lista di regioni di testo (x, y, w, h)
            
        Returns:
            dict: Dizionario con le informazioni sui font
        """
        # Se non sono fornite regioni di testo, rileva automaticamente
        if text_regions is None:
            text_regions = self.detect_text_regions(image)
        
        # Converti in scala di grigi se necessario
        if len(image.shape) > 2:
            gray = self.preprocessor.convert_to_grayscale(image)
        else:
            gray = image
        
        # Prepara il risultato
        result = {
            'regions': []
        }
        
        # Analizza ciascuna regione
        for i, (x, y, w, h) in enumerate(text_regions):
            # Estrai la regione
            roi = gray[y:y+h, x:x+w]
            
            # Applica miglioramenti all'immagine per OCR
            roi = cv2.resize(roi, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            roi = cv2.GaussianBlur(roi, (5, 5), 0)
            roi = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            
            # Esegui OCR con output dettagliato
            ocr_data = pytesseract.image_to_data(roi, output_type=pytesseract.Output.DICT)
            
            # Analizza le caratteristiche del font
            font_info = self._analyze_font_characteristics(roi, ocr_data)
            
            # Aggiungi al risultato
            result['regions'].append({
                'id': i,
                'bbox': (x, y, w, h),
                'font_info': font_info
            })
        
        return result
    
    def _analyze_font_characteristics(self, image, ocr_data):
        """
        Analizza le caratteristiche del font in una regione di testo.
        
        Args:
            image (numpy.ndarray): Immagine della regione di testo
            ocr_data (dict): Dati OCR dalla regione
            
        Returns:
            dict: Caratteristiche del font
        """
        # Inizializza le caratteristiche
        font_info = {
            'is_serif': False,
            'is_monospaced': False,
            'is_bold': False,
            'is_italic': False,
            'font_size': 0,
            'confidence': 0,
            'possible_fonts': []
        }
        
        # Estrai le caratteristiche dai dati OCR
        if 'conf' in ocr_data and len(ocr_data['conf']) > 0:
            # Calcola la confidenza media
            valid_conf = [float(conf) for conf in ocr_data['conf'] if conf != '-1']
            if valid_conf:
                font_info['confidence'] = sum(valid_conf) / len(valid_conf)
        
        # Analizza la spaziatura per determinare se è monospaced
        if 'text' in ocr_data and 'left' in ocr_data and len(ocr_data['text']) > 1:
            # Filtra solo le parole valide
            valid_indices = [i for i, text in enumerate(ocr_data['text']) if text.strip()]
            
            if len(valid_indices) > 1:
                # Calcola le distanze tra le parole
                lefts = [ocr_data['left'][i] for i in valid_indices]
                widths = [ocr_data['width'][i] for i in valid_indices]
                
                # Calcola la deviazione standard delle larghezze dei caratteri
                char_widths = []
                for i in valid_indices:
                    if ocr_data['text'][i] and len(ocr_data['text'][i]) > 0:
                        char_width = ocr_data['width'][i] / len(ocr_data['text'][i])
                        char_widths.append(char_width)
                
                if char_widths:
                    std_dev = np.std(char_widths)
                    mean_width = np.mean(char_widths)
                    
                    # Se la deviazione standard è bassa rispetto alla media, è probabilmente monospaced
                    if std_dev / mean_width < 0.1:
                        font_info['is_monospaced'] = True
        
        # Analizza l'immagine per determinare se è serif o sans-serif
        # Questo è un approccio semplificato basato sul conteggio dei pixel
        binary = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        
        # Calcola il numero di pixel bianchi (testo) e neri (sfondo)
        white_pixels = cv2.countNonZero(binary)
        total_pixels = binary.shape[0] * binary.shape[1]
        black_pixels = total_pixels - white_pixels
        
        # Calcola la densità del testo
        text_density = white_pixels / total_pixels if total_pixels > 0 else 0
        
        # Applica operazioni morfologiche per rilevare caratteristiche serif
        kernel = np.ones((2, 2), np.uint8)
        eroded = cv2.erode(binary, kernel, iterations=1)
        
        # Calcola la differenza tra l'immagine originale e quella erosa
        diff = cv2.subtract(binary, eroded)
        
        # Conta i pixel nella differenza
        diff_pixels = cv2.countNonZero(diff)
        
        # Calcola il rapporto tra i pixel di differenza e i pixel bianchi originali
        serif_ratio = diff_pixels / white_pixels if white_pixels > 0 else 0
        
        # Se il rapporto è alto, è probabilmente serif
        if serif_ratio > 0.2:
            font_info['is_serif'] = True
        
        # Stima la dimensione del font
        if 'height' in ocr_data and len(ocr_data['height']) > 0:
            valid_heights = [h for h in ocr_data['height'] if h > 0]
            if valid_heights:
                font_info['font_size'] = sum(valid_heights) / len(valid_heights) / 2  # Approssimazione
        
        # Determina se è grassetto
        if text_density > 0.4:  # Soglia arbitraria
            font_info['is_bold'] = True
        
        # Determina se è corsivo
        # Questo richiederebbe un'analisi più complessa dell'inclinazione dei caratteri
        # Per ora, utilizziamo un'euristica basata sui dati OCR
        if 'text' in ocr_data and 'left' in ocr_data and 'width' in ocr_data:
            # Calcola l'inclinazione media dei caratteri
            # Questo è un approccio semplificato
            font_info['is_italic'] = False  # Implementazione semplificata
        
        # Suggerisci possibili font
        if font_info['is_serif'] and font_info['is_monospaced']:
            font_info['possible_fonts'] = ['Courier', 'Courier New', 'Consolas']
        elif font_info['is_serif'] and not font_info['is_monospaced']:
            if font_info['is_bold']:
                font_info['possible_fonts'] = ['Times New Roman Bold', 'Georgia Bold', 'Garamond Bold']
            else:
                font_info['possible_fonts'] = ['Times New Roman', 'Georgia', 'Garamond']
        elif not font_info['is_serif'] and font_info['is_monospaced']:
            font_info['possible_fonts'] = ['Monaco', 'Menlo', 'Lucida Console']
        else:  # sans-serif, non-monospaced
            if font_info['is_bold']:
                font_info['possible_fonts'] = ['Arial Bold', 'Helvetica Bold', 'Calibri Bold']
            else:
                font_info['possible_fonts'] = ['Arial', 'Helvetica', 'Calibri']
        
        return font_info
    
    def analyze_ink(self, image):
        """
        Analizza il tipo di inchiostro utilizzato in un'immagine.
        
        Args:
            image (numpy.ndarray): Immagine di input
            
        Returns:
            dict: Informazioni sul tipo di inchiostro
        """
        # Verifica che l'immagine sia a colori
        if len(image.shape) < 3:
            # Converti in BGR se è in scala di grigi
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        
        # Converti in HSV per un'analisi migliore del colore
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Estrai i canali HSV
        h, s, v = cv2.split(hsv)
        
        # Crea una maschera per isolare l'inchiostro (pixel scuri)
        _, ink_mask = cv2.threshold(v, 150, 255, cv2.THRESH_BINARY_INV)
        
        # Applica la maschera ai canali HSV
        h_ink = cv2.bitwise_and(h, h, mask=ink_mask)
        s_ink = cv2.bitwise_and(s, s, mask=ink_mask)
        
        # Calcola le statistiche dei canali HSV per l'inchiostro
        h_values = h_ink[ink_mask > 0]
        s_values = s_ink[ink_mask > 0]
        v_values = 255 - v[ink_mask > 0]  # Inverti V per ottenere l'intensità dell'inchiostro
        
        # Se non ci sono pixel di inchiostro, restituisci un risultato predefinito
        if len(h_values) == 0:
            return {
                'ink_type': 'unknown',
                'ink_color': 'unknown',
                'is_printed': False,
                'confidence': 0,
                'details': {
                    'hue_mean': 0,
                    'saturation_mean': 0,
                    'value_mean': 0,
                    'hue_std': 0,
                    'saturation_std': 0,
                    'value_std': 0,
                    'ink_coverage': 0
                }
            }
        
        # Calcola le statistiche
        hue_mean = np.mean(h_values)
        saturation_mean = np.mean(s_values)
        value_mean = np.mean(v_values)
        hue_std = np.std(h_values)
        saturation_std = np.std(s_values)
        value_std = np.std(v_values)
        
        # Calcola la copertura dell'inchiostro
        ink_coverage = np.count_nonzero(ink_mask) / (ink_mask.shape[0] * ink_mask.shape[1])
        
        # Determina il colore dell'inchiostro
        ink_color = self._determine_ink_color(hue_mean, saturation_mean, value_mean)
        
        # Determina se è stampato o scritto a mano
        is_printed = self._is_printed_ink(value_std, saturation_std, ink_coverage)
        
        # Determina il tipo di inchiostro
        ink_type, confidence = self._determine_ink_type(
            hue_mean, saturation_mean, value_mean, 
            hue_std, saturation_std, value_std, 
            ink_coverage, is_printed
        )
        
        return {
            'ink_type': ink_type,
            'ink_color': ink_color,
            'is_printed': is_printed,
            'confidence': confidence,
            'details': {
                'hue_mean': float(hue_mean),
                'saturation_mean': float(saturation_mean),
                'value_mean': float(value_mean),
                'hue_std': float(hue_std),
                'saturation_std': float(saturation_std),
                'value_std': float(value_std),
                'ink_coverage': float(ink_coverage)
            }
        }
    
    def _determine_ink_color(self, hue_mean, saturation_mean, value_mean):
        """
        Determina il colore dell'inchiostro in base ai valori HSV.
        
        Args:
            hue_mean (float): Media del canale H
            saturation_mean (float): Media del canale S
            value_mean (float): Media del canale V
            
        Returns:
            str: Nome del colore dell'inchiostro
        """
        # Se la saturazione è bassa, è probabilmente nero o grigio
        if saturation_mean < 50:
            if value_mean > 200:
                return 'black'
            else:
                return 'gray'
        
        # Altrimenti, determina il colore in base alla tonalità
        if 0 <= hue_mean < 30 or 330 <= hue_mean <= 360:
            return 'red'
        elif 30 <= hue_mean < 90:
            return 'yellow'
        elif 90 <= hue_mean < 150:
            return 'green'
        elif 150 <= hue_mean < 210:
            return 'cyan'
        elif 210 <= hue_mean < 270:
            return 'blue'
        elif 270 <= hue_mean < 330:
            return 'magenta'
        else:
            return 'unknown'
    
    def _is_printed_ink(self, value_std, saturation_std, ink_coverage):
        """
        Determina se l'inchiostro è stampato o scritto a mano.
        
        Args:
            value_std (float): Deviazione standard del canale V
            saturation_std (float): Deviazione standard del canale S
            ink_coverage (float): Percentuale di copertura dell'inchiostro
            
        Returns:
            bool: True se l'inchiostro è probabilmente stampato, False altrimenti
        """
        # L'inchiostro stampato tende ad avere una deviazione standard più bassa
        # e una copertura più uniforme
        if value_std < 30 and saturation_std < 20:
            return True
        
        # Se la copertura è molto alta, è probabilmente stampato
        if ink_coverage > 0.4:
            return True
        
        return False
    
    def _determine_ink_type(self, hue_mean, saturation_mean, value_mean, 
                           hue_std, saturation_std, value_std, 
                           ink_coverage, is_printed):
        """
        Determina il tipo di inchiostro in base alle statistiche HSV.
        
        Args:
            hue_mean (float): Media del canale H
            saturation_mean (float): Media del canale S
            value_mean (float): Media del canale V
            hue_std (float): Deviazione standard del canale H
            saturation_std (float): Deviazione standard del canale S
            value_std (float): Deviazione standard del canale V
            ink_coverage (float): Percentuale di copertura dell'inchiostro
            is_printed (bool): Se l'inchiostro è stampato o scritto a mano
            
        Returns:
            tuple: (tipo_inchiostro, confidenza)
        """
        if is_printed:
            # Inchiostro stampato
            if saturation_mean < 30 and value_mean > 200:
                return 'laser_printer', 0.8
            elif saturation_mean < 50:
                return 'inkjet_printer', 0.7
            else:
                return 'color_printer', 0.6
        else:
            # Inchiostro scritto a mano
            if saturation_mean < 30 and value_mean > 200:
                # Penna a sfera (biro)
                return 'ballpoint_pen', 0.7
            elif saturation_mean > 100 and value_std > 40:
                # Pennarello
                return 'marker', 0.8
            elif value_mean < 150 and value_std < 30:
                # Penna stilografica
                return 'fountain_pen', 0.6
            elif saturation_mean < 50 and value_mean < 180:
                # Matita
                return 'pencil', 0.7
            else:
                return 'unknown_pen', 0.4
