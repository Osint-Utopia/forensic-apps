"""
Utilidades para procesamiento de texto
"""

import re
import unicodedata
from unidecode import unidecode
from utils.config import STOP_WORDS

class TextProcessor:
    """Clase para procesamiento y normalización de texto"""
    
    def __init__(self, language='es'):
        self.language = language
        self.stop_words = set(STOP_WORDS.get(language, STOP_WORDS['es']))
    
    def normalize_text(self, text):
        """
        Normaliza el texto eliminando caracteres especiales y convirtiendo a minúsculas
        """
        if not text:
            return ""
        
        # Convertir a string si no lo es
        text = str(text)
        
        # Convertir a minúsculas
        text = text.lower()
        
        # Normalizar caracteres unicode
        text = unicodedata.normalize('NFKD', text)
        
        # Convertir caracteres especiales a ASCII
        text = unidecode(text)
        
        # Eliminar caracteres no alfanuméricos excepto espacios
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        
        # Eliminar espacios múltiples
        text = re.sub(r'\s+', ' ', text)
        
        # Eliminar espacios al inicio y final
        text = text.strip()
        
        return text
    
    def remove_stop_words(self, text):
        """
        Elimina stop words del texto
        """
        if not text:
            return ""
        
        words = text.split()
        filtered_words = [word for word in words if word not in self.stop_words]
        return ' '.join(filtered_words)
    
    def extract_keywords(self, text, min_length=3):
        """
        Extrae palabras clave del texto
        """
        if not text:
            return []
        
        # Normalizar texto
        normalized = self.normalize_text(text)
        
        # Eliminar stop words
        without_stopwords = self.remove_stop_words(normalized)
        
        # Dividir en palabras y filtrar por longitud
        words = without_stopwords.split()
        keywords = [word for word in words if len(word) >= min_length]
        
        return keywords
    
    def preprocess_for_search(self, text):
        """
        Preprocesa texto para búsqueda semántica
        """
        if not text:
            return ""
        
        # Normalizar
        processed = self.normalize_text(text)
        
        # Eliminar stop words
        processed = self.remove_stop_words(processed)
        
        return processed
    
    def detect_language(self, text):
        """
        Detecta el idioma del texto (simple heurística)
        """
        if not text:
            return 'es'
        
        # Palabras comunes en español
        spanish_indicators = ['que', 'como', 'para', 'con', 'por', 'una', 'del', 'las', 'los', 'está', 'son']
        
        # Palabras comunes en inglés
        english_indicators = ['the', 'and', 'that', 'have', 'for', 'not', 'with', 'you', 'this', 'but', 'are']
        
        text_lower = text.lower()
        
        spanish_count = sum(1 for word in spanish_indicators if word in text_lower)
        english_count = sum(1 for word in english_indicators if word in text_lower)
        
        return 'en' if english_count > spanish_count else 'es'
    
    def clean_response_text(self, text):
        """
        Limpia el texto de respuesta eliminando marcadores de formato
        """
        if not text:
            return ""
        
        # Eliminar marcadores HUMAN/ASSISTANT
        text = re.sub(r'<HUMAN>:', '', text)
        text = re.sub(r'<ASSISTANT>:', '', text)
        text = re.sub(r'\\u003C.*?\\u003E', '', text)
        
        # Eliminar saltos de línea excesivos
        text = re.sub(r'\n+', '\n', text)
        
        # Limpiar espacios
        text = text.strip()
        
        return text

def simple_stemmer(word, language='es'):
    """
    Stemmer simple para reducir palabras a su raíz
    """
    if language == 'es':
        # Sufijos comunes en español
        suffixes = ['ando', 'iendo', 'ado', 'ido', 'ar', 'er', 'ir', 'ción', 'sión', 'dad', 'idad', 'mente']
        
        for suffix in sorted(suffixes, key=len, reverse=True):
            if word.endswith(suffix) and len(word) > len(suffix) + 2:
                return word[:-len(suffix)]
    
    elif language == 'en':
        # Sufijos comunes en inglés
        suffixes = ['ing', 'ed', 'er', 'est', 'ly', 'tion', 'sion', 'ness', 'ment']
        
        for suffix in sorted(suffixes, key=len, reverse=True):
            if word.endswith(suffix) and len(word) > len(suffix) + 2:
                return word[:-len(suffix)]
    
    return word
