import cv2
import numpy as np
from PIL import Image

def process_signature(image):
    # Se `image` è numpy, convertilo a PIL.
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)
    
    """Effettua preprocessing della firma per migliorare l'analisi"""
    img = np.array(image.convert("L"))  # Converti in scala di grigi
    img = cv2.GaussianBlur(img, (5, 5), 0)  # Applica un leggero smoothing
    _, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)  # Binarizzazione
    return img
