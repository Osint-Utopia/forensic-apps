import cv2
import numpy as np
import os
from PIL import Image
import fitz  # PyMuPDF

class ImagePreprocessor:
    """
    Classe per l'acquisizione e pre-elaborazione delle immagini di firme e documenti.
    Implementa funzionalità di base come la conversione in scala di grigi,
    normalizzazione, scontorno dei timbri, ecc.
    """
    
    def __init__(self):
        """Inizializza il preprocessore di immagini."""
        pass
    
    def load_image(self, image_path):
        """
        Carica un'immagine da un percorso file.
        
        Args:
            image_path (str): Percorso dell'immagine da caricare
            
        Returns:
            numpy.ndarray: Immagine caricata in formato BGR
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Il file {image_path} non esiste")
        
        # Controlla l'estensione del file
        _, ext = os.path.splitext(image_path)
        ext = ext.lower()
        
        if ext == '.pdf':
            return self.extract_image_from_pdf(image_path)
        else:
            # Carica l'immagine usando OpenCV
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Impossibile caricare l'immagine {image_path}")
            return image
    
    def extract_image_from_pdf(self, pdf_path, page_num=0):
        """
        Estrae un'immagine da un file PDF.
        
        Args:
            pdf_path (str): Percorso del file PDF
            page_num (int): Numero di pagina da cui estrarre l'immagine (default: 0)
            
        Returns:
            numpy.ndarray: Immagine estratta in formato BGR
        """
        # Apri il documento PDF
        doc = fitz.open(pdf_path)
        
        # Controlla se il numero di pagina è valido
        if page_num >= len(doc):
            raise ValueError(f"Il PDF ha {len(doc)} pagine, ma è stata richiesta la pagina {page_num}")
        
        # Ottieni la pagina
        page = doc.load_page(page_num)
        
        # Renderizza la pagina come immagine
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Fattore di scala 2 per migliore qualità
        
        # Converti in formato immagine
        img_data = pix.samples
        
        # Crea un array numpy dall'immagine
        img_array = np.frombuffer(img_data, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
        
        # Se l'immagine è in formato RGB, converti in BGR per OpenCV
        if pix.n == 3:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        return img_array
    
    def convert_to_grayscale(self, image):
        """
        Converte un'immagine in scala di grigi.
        
        Args:
            image (numpy.ndarray): Immagine di input in formato BGR
            
        Returns:
            numpy.ndarray: Immagine in scala di grigi
        """
        if len(image.shape) == 2:
            # L'immagine è già in scala di grigi
            return image
        
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    def normalize_image(self, image):
        """
        Normalizza un'immagine per migliorare contrasto e luminosità.
        
        Args:
            image (numpy.ndarray): Immagine di input (scala di grigi o BGR)
            
        Returns:
            numpy.ndarray: Immagine normalizzata
        """
        # Converti in scala di grigi se necessario
        if len(image.shape) > 2:
            gray = self.convert_to_grayscale(image)
        else:
            gray = image
        
        # Applica equalizzazione dell'istogramma
        return cv2.equalizeHist(gray)
    
    def detect_and_extract_stamps(self, image, lower_color=None, upper_color=None):
        """
        Rileva e estrae i timbri da un'immagine utilizzando il filtraggio del colore.
        
        Args:
            image (numpy.ndarray): Immagine di input in formato BGR
            lower_color (numpy.ndarray, optional): Limite inferiore del colore in formato HSV
            upper_color (numpy.ndarray, optional): Limite superiore del colore in formato HSV
            
        Returns:
            tuple: (immagine_originale_senza_timbri, maschera_timbri, timbri_estratti)
        """
        # Valori predefiniti per rilevare timbri blu (comuni nei documenti)
        if lower_color is None:
            lower_color = np.array([100, 50, 50])  # Blu in HSV
        if upper_color is None:
            upper_color = np.array([140, 255, 255])
        
        # Converti l'immagine in HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Crea una maschera per il colore specificato
        mask = cv2.inRange(hsv, lower_color, upper_color)
        
        # Applica operazioni morfologiche per migliorare la maschera
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Estrai i timbri
        stamps = cv2.bitwise_and(image, image, mask=mask)
        
        # Crea un'immagine senza timbri
        inv_mask = cv2.bitwise_not(mask)
        image_without_stamps = cv2.bitwise_and(image, image, mask=inv_mask)
        
        return image_without_stamps, mask, stamps
    
    def threshold_image(self, image, method='adaptive'):
        """
        Applica una soglia all'immagine per binarizzarla.
        
        Args:
            image (numpy.ndarray): Immagine in scala di grigi
            method (str): Metodo di soglia ('simple', 'adaptive', 'otsu')
            
        Returns:
            numpy.ndarray: Immagine binaria
        """
        if len(image.shape) > 2:
            gray = self.convert_to_grayscale(image)
        else:
            gray = image
        
        if method == 'simple':
            _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
        elif method == 'adaptive':
            binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                          cv2.THRESH_BINARY_INV, 11, 2)
        elif method == 'otsu':
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        else:
            raise ValueError(f"Metodo di soglia non supportato: {method}")
        
        return binary
    
    def resize_image(self, image, width=None, height=None, keep_aspect_ratio=True):
        """
        Ridimensiona un'immagine a una larghezza o altezza specificata.
        
        Args:
            image (numpy.ndarray): Immagine di input
            width (int, optional): Larghezza desiderata
            height (int, optional): Altezza desiderata
            keep_aspect_ratio (bool): Mantiene il rapporto d'aspetto originale
            
        Returns:
            numpy.ndarray: Immagine ridimensionata
        """
        if width is None and height is None:
            return image
        
        h, w = image.shape[:2]
        
        if keep_aspect_ratio:
            if width is None:
                aspect_ratio = height / float(h)
                dim = (int(w * aspect_ratio), height)
            else:
                aspect_ratio = width / float(w)
                dim = (width, int(h * aspect_ratio))
        else:
            dim = (width if width is not None else w, height if height is not None else h)
        
        return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    
    def denoise_image(self, image, method='gaussian'):
        """
        Applica un filtro di riduzione del rumore all'immagine.
        
        Args:
            image (numpy.ndarray): Immagine di input
            method (str): Metodo di denoising ('gaussian', 'median', 'bilateral')
            
        Returns:
            numpy.ndarray: Immagine filtrata
        """
        if method == 'gaussian':
            return cv2.GaussianBlur(image, (5, 5), 0)
        elif method == 'median':
            return cv2.medianBlur(image, 5)
        elif method == 'bilateral':
            if len(image.shape) > 2:
                return cv2.bilateralFilter(image, 9, 75, 75)
            else:
                # Per immagini in scala di grigi, convertiamo temporaneamente in BGR
                temp = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
                temp = cv2.bilateralFilter(temp, 9, 75, 75)
                return cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
        else:
            raise ValueError(f"Metodo di denoising non supportato: {method}")
    
    def preprocess_signature(self, image_path, resize_width=800):
        """
        Pipeline completa di pre-elaborazione per le firme.
        
        Args:
            image_path (str): Percorso dell'immagine della firma
            resize_width (int): Larghezza a cui ridimensionare l'immagine
            
        Returns:
            dict: Dizionario contenente le diverse fasi di pre-elaborazione
        """
        # Carica l'immagine
        original = self.load_image(image_path)
        
        # Ridimensiona l'immagine
        resized = self.resize_image(original, width=resize_width)
        
        # Converti in scala di grigi
        gray = self.convert_to_grayscale(resized)
        
        # Normalizza l'immagine
        normalized = self.normalize_image(gray)
        
        # Applica denoising
        denoised = self.denoise_image(normalized, method='bilateral')
        
        # Applica soglia
        binary = self.threshold_image(denoised, method='adaptive')
        
        # Restituisci tutte le fasi di pre-elaborazione
        return {
            'original': original,
            'resized': resized,
            'grayscale': gray,
            'normalized': normalized,
            'denoised': denoised,
            'binary': binary
        }
