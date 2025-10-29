"""
Motor de búsqueda semántica para el chatbot de salud mental
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
from utils.text_processing import TextProcessor
from utils.config import SEARCH_CONFIG

class SemanticSearchEngine:
    """Motor de búsqueda semántica usando TF-IDF y similitud coseno"""
    
    def __init__(self):
        self.vectorizers = {}  # Vectorizadores por idioma
        self.question_vectors = {}  # Vectores de preguntas por idioma
        self.answer_vectors = {}  # Vectores de respuestas por idioma
        self.conversations = {}  # Conversaciones por idioma
        self.text_processors = {
            'es': TextProcessor('es'),
            'en': TextProcessor('en')
        }
        self.is_trained = False
    
    def train(self, conversations: List[Dict]):
        """
        Entrena el motor de búsqueda con las conversaciones proporcionadas
        """
        print("Entrenando motor de búsqueda semántica...")
        
        # Separar conversaciones por idioma
        conversations_by_lang = {}
        for conv in conversations:
            lang = conv['language']
            if lang not in conversations_by_lang:
                conversations_by_lang[lang] = []
            conversations_by_lang[lang].append(conv)
        
        # Entrenar vectorizadores para cada idioma
        for lang, lang_conversations in conversations_by_lang.items():
            print(f"Entrenando para idioma: {lang} ({len(lang_conversations)} conversaciones)")
            
            # Extraer textos procesados
            questions = [conv['processed_question'] for conv in lang_conversations]
            answers = [conv['processed_answer'] for conv in lang_conversations]
            
            # Combinar preguntas y respuestas para el vocabulario
            all_texts = questions + answers
            
            # Crear y entrenar vectorizador TF-IDF
            vectorizer = TfidfVectorizer(
                max_features=5000,
                ngram_range=(1, 2),  # Unigramas y bigramas
                min_df=1,
                max_df=0.95,
                stop_words=None  # Ya removimos stop words en el preprocesamiento
            )
            
            try:
                vectorizer.fit(all_texts)
                
                # Vectorizar preguntas y respuestas
                question_vectors = vectorizer.transform(questions)
                answer_vectors = vectorizer.transform(answers)
                
                # Guardar en el motor
                self.vectorizers[lang] = vectorizer
                self.question_vectors[lang] = question_vectors
                self.answer_vectors[lang] = answer_vectors
                self.conversations[lang] = lang_conversations
                
                print(f"Vocabulario para {lang}: {len(vectorizer.vocabulary_)} términos")
                
            except Exception as e:
                print(f"Error entrenando para idioma {lang}: {e}")
        
        self.is_trained = True
        print("Entrenamiento completado")
    
    def search(self, query: str, language: str = None, max_results: int = None) -> List[Dict]:
        """
        Busca respuestas relevantes para una consulta
        """
        if not self.is_trained:
            return []
        
        if max_results is None:
            max_results = SEARCH_CONFIG['max_results']
        
        # Detectar idioma si no se especifica
        if language is None:
            language = self.text_processors['es'].detect_language(query)
        
        # Verificar si tenemos datos para este idioma
        if language not in self.vectorizers:
            # Intentar con el otro idioma disponible
            available_langs = list(self.vectorizers.keys())
            if available_langs:
                language = available_langs[0]
            else:
                return []
        
        # Preprocesar consulta
        processor = self.text_processors[language]
        processed_query = processor.preprocess_for_search(query)
        
        if not processed_query.strip():
            return []
        
        try:
            # Vectorizar consulta
            vectorizer = self.vectorizers[language]
            query_vector = vectorizer.transform([processed_query])
            
            # Calcular similitudes con preguntas
            question_similarities = cosine_similarity(query_vector, self.question_vectors[language]).flatten()
            
            # Calcular similitudes con respuestas (peso menor)
            answer_similarities = cosine_similarity(query_vector, self.answer_vectors[language]).flatten()
            
            # Combinar similitudes (más peso a preguntas)
            combined_similarities = 0.7 * question_similarities + 0.3 * answer_similarities
            
            # Obtener índices ordenados por similitud
            sorted_indices = np.argsort(combined_similarities)[::-1]
            
            # Filtrar por umbral mínimo y límite de resultados
            results = []
            threshold = SEARCH_CONFIG['min_similarity_threshold']
            
            for idx in sorted_indices[:max_results * 2]:  # Obtener más para filtrar
                similarity = combined_similarities[idx]
                
                if similarity >= threshold:
                    conversation = self.conversations[language][idx].copy()
                    conversation['similarity_score'] = float(similarity)
                    conversation['question_similarity'] = float(question_similarities[idx])
                    conversation['answer_similarity'] = float(answer_similarities[idx])
                    results.append(conversation)
                
                if len(results) >= max_results:
                    break
            
            return results
            
        except Exception as e:
            print(f"Error en búsqueda: {e}")
            return []
    
    def search_multimodal(self, query: str, max_results: int = None) -> List[Dict]:
        """
        Busca en todos los idiomas disponibles y combina resultados
        """
        if max_results is None:
            max_results = SEARCH_CONFIG['max_results']
        
        all_results = []
        
        # Buscar en cada idioma
        for lang in self.vectorizers.keys():
            lang_results = self.search(query, language=lang, max_results=max_results)
            all_results.extend(lang_results)
        
        # Ordenar por similitud y limitar resultados
        all_results.sort(key=lambda x: x['similarity_score'], reverse=True)
        return all_results[:max_results]
    
    def get_similar_questions(self, query: str, language: str = None, max_results: int = 5) -> List[str]:
        """
        Obtiene preguntas similares a la consulta
        """
        results = self.search(query, language, max_results)
        return [result['question'] for result in results]
    
    def get_vocabulary_stats(self, language: str) -> Dict:
        """
        Obtiene estadísticas del vocabulario para un idioma
        """
        if language not in self.vectorizers:
            return {}
        
        vectorizer = self.vectorizers[language]
        vocabulary = vectorizer.vocabulary_
        
        return {
            'vocabulary_size': len(vocabulary),
            'feature_names': list(vocabulary.keys())[:20],  # Primeras 20 características
            'max_features': vectorizer.max_features,
            'ngram_range': vectorizer.ngram_range
        }
    
    def explain_search(self, query: str, language: str = None) -> Dict:
        """
        Explica cómo se procesó una búsqueda (para debugging)
        """
        if language is None:
            language = self.text_processors['es'].detect_language(query)
        
        processor = self.text_processors[language]
        
        explanation = {
            'original_query': query,
            'detected_language': language,
            'normalized_query': processor.normalize_text(query),
            'processed_query': processor.preprocess_for_search(query),
            'keywords': processor.extract_keywords(query),
            'available_languages': list(self.vectorizers.keys()),
            'is_trained': self.is_trained
        }
        
        if language in self.vectorizers:
            explanation['vocabulary_size'] = len(self.vectorizers[language].vocabulary_)
            explanation['num_conversations'] = len(self.conversations[language])
        
        return explanation
