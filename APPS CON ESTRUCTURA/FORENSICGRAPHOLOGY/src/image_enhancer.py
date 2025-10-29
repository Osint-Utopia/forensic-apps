import cv2
import numpy as np
import matplotlib.pyplot as plt
from .preprocessing import ImagePreprocessor

class ImageEnhancer:
    """
    Classe per l'elaborazione avanzata delle immagini di firme e documenti.
    Implementa funzionalità per migliorare la qualità delle immagini,
    evidenziare dettagli e applicare filtri speciali per l'analisi forense.
    """
    
    def __init__(self):
        """Inizializza l'enhancer di immagini."""
        self.preprocessor = ImagePreprocessor()
    
    def enhance_contrast(self, image, method='clahe'):
        """
        Migliora il contrasto di un'immagine.
        
        Args:
            image (numpy.ndarray): Immagine di input
            method (str): Metodo di miglioramento ('clahe', 'histogram_eq', 'adaptive')
            
        Returns:
            numpy.ndarray: Immagine con contrasto migliorato
        """
        # Converti in scala di grigi se necessario
        if len(image.shape) > 2:
            gray = self.preprocessor.convert_to_grayscale(image)
        else:
            gray = image.copy()
        
        if method == 'clahe':
            # Contrast Limited Adaptive Histogram Equalization
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(gray)
        elif method == 'histogram_eq':
            # Equalizzazione dell'istogramma globale
            enhanced = cv2.equalizeHist(gray)
        elif method == 'adaptive':
            # Miglioramento adattivo del contrasto
            enhanced = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           cv2.THRESH_BINARY, 11, 2)
        else:
            raise ValueError(f"Metodo di miglioramento del contrasto non supportato: {method}")
        
        return enhanced
    
    def sharpen_image(self, image, kernel_size=3, strength=1.0):
        """
        Applica un filtro di sharpening all'immagine.
        
        Args:
            image (numpy.ndarray): Immagine di input
            kernel_size (int): Dimensione del kernel
            strength (float): Intensità dell'effetto di sharpening
            
        Returns:
            numpy.ndarray: Immagine affilata
        """
        # Converti in scala di grigi se necessario
        if len(image.shape) > 2:
            gray = self.preprocessor.convert_to_grayscale(image)
        else:
            gray = image.copy()
        
        # Applica un filtro gaussiano per ridurre il rumore
        blurred = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
        
        # Calcola la maschera di sharpening (immagine originale - immagine sfocata)
        mask = cv2.subtract(gray, blurred)
        
        # Applica la maschera all'immagine originale
        sharpened = cv2.addWeighted(gray, 1.0, mask, strength, 0)
        
        return sharpened
    
    def apply_edge_detection(self, image, method='canny'):
        """
        Applica un rilevatore di bordi all'immagine.
        
        Args:
            image (numpy.ndarray): Immagine di input
            method (str): Metodo di rilevamento bordi ('canny', 'sobel', 'laplacian')
            
        Returns:
            numpy.ndarray: Immagine con bordi rilevati
        """
        # Converti in scala di grigi se necessario
        if len(image.shape) > 2:
            gray = self.preprocessor.convert_to_grayscale(image)
        else:
            gray = image.copy()
        
        # Applica un filtro gaussiano per ridurre il rumore
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        if method == 'canny':
            # Rilevatore di bordi Canny
            edges = cv2.Canny(blurred, 50, 150)
        elif method == 'sobel':
            # Rilevatore di bordi Sobel
            sobelx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
            
            # Calcola il gradiente
            magnitude = cv2.magnitude(sobelx, sobely)
            
            # Normalizza e converti in uint8
            edges = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        elif method == 'laplacian':
            # Rilevatore di bordi Laplaciano
            laplacian = cv2.Laplacian(blurred, cv2.CV_64F)
            
            # Normalizza e converti in uint8
            edges = cv2.normalize(laplacian, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        else:
            raise ValueError(f"Metodo di rilevamento bordi non supportato: {method}")
        
        return edges
    
    def highlight_pressure_points(self, image, threshold=50):
        """
        Evidenzia i punti di pressione in una firma.
        
        Args:
            image (numpy.ndarray): Immagine di input
            threshold (int): Soglia per considerare un punto come punto di pressione
            
        Returns:
            numpy.ndarray: Immagine con punti di pressione evidenziati
        """
        # Converti in scala di grigi se necessario
        if len(image.shape) > 2:
            gray = self.preprocessor.convert_to_grayscale(image)
        else:
            gray = image.copy()
        
        # Inverti l'immagine (testo bianco su sfondo nero)
        gray_inv = cv2.bitwise_not(gray)
        
        # Applica una soglia per isolare il testo
        _, binary = cv2.threshold(gray_inv, threshold, 255, cv2.THRESH_BINARY)
        
        # Crea un'immagine a colori per la visualizzazione
        result = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        
        # Applica una mappa di colori per evidenziare i punti di pressione
        # Più scuro è il pixel, maggiore è la pressione
        for i in range(gray.shape[0]):
            for j in range(gray.shape[1]):
                if binary[i, j] > 0:
                    # Calcola l'intensità normalizzata (0-1)
                    intensity = gray_inv[i, j] / 255.0
                    
                    # Applica una mappa di colori (blu -> verde -> rosso)
                    if intensity < 0.33:
                        # Blu (bassa pressione)
                        result[i, j] = [255, 0, 0]
                    elif intensity < 0.66:
                        # Verde (media pressione)
                        result[i, j] = [0, 255, 0]
                    else:
                        # Rosso (alta pressione)
                        result[i, j] = [0, 0, 255]
        
        return result
    
    def extract_profile(self, image, direction='horizontal'):
        """
        Estrae il profilo di un'immagine in una direzione specifica.
        
        Args:
            image (numpy.ndarray): Immagine di input
            direction (str): Direzione del profilo ('horizontal', 'vertical')
            
        Returns:
            numpy.ndarray: Profilo estratto
        """
        # Converti in scala di grigi se necessario
        if len(image.shape) > 2:
            gray = self.preprocessor.convert_to_grayscale(image)
        else:
            gray = image.copy()
        
        # Inverti l'immagine (testo bianco su sfondo nero)
        gray_inv = cv2.bitwise_not(gray)
        
        if direction == 'horizontal':
            # Somma i pixel per ogni riga
            profile = np.sum(gray_inv, axis=1)
        elif direction == 'vertical':
            # Somma i pixel per ogni colonna
            profile = np.sum(gray_inv, axis=0)
        else:
            raise ValueError(f"Direzione del profilo non supportata: {direction}")
        
        # Normalizza il profilo
        if np.max(profile) > 0:
            profile = profile / np.max(profile)
        
        return profile
    
    def visualize_profile(self, image, save_path=None):
        """
        Visualizza i profili orizzontale e verticale di un'immagine.
        
        Args:
            image (numpy.ndarray): Immagine di input
            save_path (str, optional): Percorso dove salvare l'immagine
            
        Returns:
            matplotlib.figure.Figure: Figura con la visualizzazione
        """
        # Estrai i profili
        h_profile = self.extract_profile(image, direction='horizontal')
        v_profile = self.extract_profile(image, direction='vertical')
        
        # Crea una figura con più sottografici
        fig, axs = plt.subplots(1, 3, figsize=(15, 5))
        
        # Immagine originale
        if len(image.shape) > 2:
            axs[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        else:
            axs[0].imshow(image, cmap='gray')
        axs[0].set_title('Immagine Originale')
        axs[0].axis('off')
        
        # Profilo orizzontale
        axs[1].plot(h_profile, range(len(h_profile)), 'b-')
        axs[1].invert_yaxis()  # Inverti l'asse y per corrispondere all'immagine
        axs[1].set_title('Profilo Orizzontale')
        axs[1].set_xlabel('Intensità Normalizzata')
        axs[1].set_ylabel('Riga')
        
        # Profilo verticale
        axs[2].plot(v_profile, 'r-')
        axs[2].set_title('Profilo Verticale')
        axs[2].set_xlabel('Colonna')
        axs[2].set_ylabel('Intensità Normalizzata')
        
        plt.tight_layout()
        
        # Salva l'immagine se richiesto
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def apply_color_filter(self, image, color_range):
        """
        Applica un filtro di colore all'immagine.
        
        Args:
            image (numpy.ndarray): Immagine di input (BGR)
            color_range (dict): Intervallo di colori in formato HSV
                                {'lower': [h_min, s_min, v_min], 'upper': [h_max, s_max, v_max]}
            
        Returns:
            numpy.ndarray: Immagine filtrata
        """
        # Verifica che l'immagine sia a colori
        if len(image.shape) < 3:
            # Converti in BGR se è in scala di grigi
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        
        # Converti in HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Crea una maschera per il colore specificato
        lower = np.array(color_range['lower'])
        upper = np.array(color_range['upper'])
        mask = cv2.inRange(hsv, lower, upper)
        
        # Applica la maschera all'immagine originale
        filtered = cv2.bitwise_and(image, image, mask=mask)
        
        return filtered
    
    def extract_stamp(self, image):
        """
        Estrae i timbri da un'immagine.
        
        Args:
            image (numpy.ndarray): Immagine di input (BGR)
            
        Returns:
            tuple: (immagine_originale_senza_timbri, timbri_estratti)
        """
        # Verifica che l'immagine sia a colori
        if len(image.shape) < 3:
            # Converti in BGR se è in scala di grigi
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        
        # Definisci intervalli di colore per i timbri comuni
        color_ranges = [
            # Blu (timbri comuni)
            {'lower': [100, 50, 50], 'upper': [140, 255, 255]},
            # Rosso (timbri comuni)
            {'lower': [0, 50, 50], 'upper': [10, 255, 255]},
            # Rosso (parte alta dello spettro HSV)
            {'lower': [170, 50, 50], 'upper': [180, 255, 255]},
            # Viola (alcuni timbri ufficiali)
            {'lower': [140, 50, 50], 'upper': [170, 255, 255]}
        ]
        
        # Converti in HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Crea una maschera combinata per tutti i colori
        combined_mask = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
        
        for color_range in color_ranges:
            lower = np.array(color_range['lower'])
            upper = np.array(color_range['upper'])
            mask = cv2.inRange(hsv, lower, upper)
            combined_mask = cv2.bitwise_or(combined_mask, mask)
        
        # Applica operazioni morfologiche per migliorare la maschera
        kernel = np.ones((5, 5), np.uint8)
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)
        
        # Estrai i timbri
        stamps = cv2.bitwise_and(image, image, mask=combined_mask)
        
        # Crea un'immagine senza timbri
        inv_mask = cv2.bitwise_not(combined_mask)
        image_without_stamps = cv2.bitwise_and(image, image, mask=inv_mask)
        
        return image_without_stamps, stamps
    
    def convert_to_grayscale_enhanced(self, image, method='weighted'):
        """
        Converte un'immagine a colori in scala di grigi con metodi avanzati.
        
        Args:
            image (numpy.ndarray): Immagine di input (BGR)
            method (str): Metodo di conversione ('weighted', 'luminosity', 'desaturation', 'decomposition')
            
        Returns:
            numpy.ndarray: Immagine in scala di grigi
        """
        # Verifica che l'immagine sia a colori
        if len(image.shape) < 3:
            return image.copy()
        
        if method == 'weighted':
            # Metodo standard (ponderato)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        elif method == 'luminosity':
            # Metodo della luminosità (pesi personalizzati)
            b, g, r = cv2.split(image)
            gray = np.uint8(0.07 * b + 0.72 * g + 0.21 * r)
        elif method == 'desaturation':
            # Metodo della desaturazione (media di min e max)
            b, g, r = cv2.split(image)
            min_val = np.minimum(np.minimum(r, g), b)
            max_val = np.maximum(np.maximum(r, g), b)
            gray = np.uint8((min_val + max_val) / 2)
        elif method == 'decomposition':
            # Metodo della decomposizione (massimo dei canali)
            b, g, r = cv2.split(image)
            gray = np.maximum(np.maximum(r, g), b)
        else:
            raise ValueError(f"Metodo di conversione in scala di grigi non supportato: {method}")
        
        return gray
    
    def apply_emboss_effect(self, image, direction='top-left'):
        """
        Applica un effetto di rilievo all'immagine.
        
        Args:
            image (numpy.ndarray): Immagine di input
            direction (str): Direzione della luce ('top-left', 'top-right', 'bottom-left', 'bottom-right')
            
        Returns:
            numpy.ndarray: Immagine con effetto di rilievo
        """
        # Converti in scala di grigi se necessario
        if len(image.shape) > 2:
            gray = self.preprocessor.convert_to_grayscale(image)
        else:
            gray = image.copy()
        
        # Definisci il kernel in base alla direzione
        if direction == 'top-left':
            kernel = np.array([[-1, -1, 0],
                              [-1, 0, 1],
                              [0, 1, 1]])
        elif direction == 'top-right':
            kernel = np.array([[0, -1, -1],
                              [1, 0, -1],
                              [1, 1, 0]])
        elif direction == 'bottom-left':
            kernel = np.array([[0, 1, 1],
                              [-1, 0, 1],
                              [-1, -1, 0]])
        elif direction == 'bottom-right':
            kernel = np.array([[1, 1, 0],
                              [1, 0, -1],
                              [0, -1, -1]])
        else:
            raise ValueError(f"Direzione non supportata: {direction}")
        
        # Applica il filtro
        embossed = cv2.filter2D(gray, -1, kernel)
        
        # Aggiungi 128 per spostare i valori nel range medio
        embossed = cv2.add(embossed, 128)
        
        return embossed
    
    def create_signature_heatmap(self, image, kernel_size=15):
        """
        Crea una mappa di calore della firma per evidenziare le aree di maggiore intensità.
        
        Args:
            image (numpy.ndarray): Immagine di input
            kernel_size (int): Dimensione del kernel per il filtro gaussiano
            
        Returns:
            numpy.ndarray: Mappa di calore della firma
        """
        # Converti in scala di grigi se necessario
        if len(image.shape) > 2:
            gray = self.preprocessor.convert_to_grayscale(image)
        else:
            gray = image.copy()
        
        # Inverti l'immagine (testo bianco su sfondo nero)
        gray_inv = cv2.bitwise_not(gray)
        
        # Applica un filtro gaussiano per creare l'effetto di calore
        heatmap = cv2.GaussianBlur(gray_inv, (kernel_size, kernel_size), 0)
        
        # Normalizza la mappa di calore
        heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        
        # Applica una mappa di colori
        heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
        
        # Crea una maschera per isolare la firma
        _, mask = cv2.threshold(gray_inv, 10, 255, cv2.THRESH_BINARY)
        
        # Dilata la maschera per includere le aree circostanti
        kernel = np.ones((5, 5), np.uint8)
        mask_dilated = cv2.dilate(mask, kernel, iterations=2)
        
        # Applica la maschera alla mappa di calore
        result = cv2.bitwise_and(heatmap_color, heatmap_color, mask=mask_dilated)
        
        # Crea un'immagine di sfondo bianco
        background = np.ones_like(image) * 255
        if len(background.shape) < 3:
            background = cv2.cvtColor(background, cv2.COLOR_GRAY2BGR)
        
        # Combina lo sfondo con la mappa di calore
        mask_dilated_3ch = cv2.cvtColor(mask_dilated, cv2.COLOR_GRAY2BGR) / 255.0
        result = background * (1 - mask_dilated_3ch) + result * mask_dilated_3ch
        
        return result.astype(np.uint8)
    
    def enhance_signature(self, image):
        """
        Applica una serie di miglioramenti a un'immagine di firma.
        
        Args:
            image (numpy.ndarray): Immagine di input
            
        Returns:
            dict: Dizionario con diverse versioni migliorate della firma
        """
        # Carica l'immagine se è un percorso file
        if isinstance(image, str):
            image = self.preprocessor.load_image(image)
        
        # Converti in scala di grigi
        gray = self.preprocessor.convert_to_grayscale(image)
        
        # Migliora il contrasto
        contrast_enhanced = self.enhance_contrast(gray, method='clahe')
        
        # Applica sharpening
        sharpened = self.sharpen_image(gray, kernel_size=3, strength=1.5)
        
        # Rileva i bordi
        edges = self.apply_edge_detection(gray, method='canny')
        
        # Evidenzia i punti di pressione
        pressure_points = self.highlight_pressure_points(gray)
        
        # Applica effetto di rilievo
        embossed = self.apply_emboss_effect(gray)
        
        # Crea una mappa di calore
        heatmap = self.create_signature_heatmap(gray)
        
        return {
            'original': image,
            'grayscale': gray,
            'contrast_enhanced': contrast_enhanced,
            'sharpened': sharpened,
            'edges': edges,
            'pressure_points': pressure_points,
            'embossed': embossed,
            'heatmap': heatmap
        }
