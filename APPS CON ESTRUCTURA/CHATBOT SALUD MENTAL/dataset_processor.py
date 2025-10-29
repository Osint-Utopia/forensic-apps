"""
Procesador de datasets JSON para el chatbot de salud mental
"""

import json
import pandas as pd
import os
from typing import List, Dict, Tuple
from utils.text_processing import TextProcessor
from utils.config import DATASET_CONFIG

class DatasetProcessor:
    """Clase para procesar y gestionar los datasets de conversaciones"""
    
    def __init__(self):
        self.conversations = []
        self.text_processor_es = TextProcessor('es')
        self.text_processor_en = TextProcessor('en')
        self.loaded_datasets = []
    
    def load_simple_dataset(self, file_path: str = None) -> List[Dict]:
        """
        Carga el dataset simple en español
        """
        if file_path is None:
            file_path = DATASET_CONFIG['simple_dataset_path']
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            conversations = []
            
            # Procesar las filas del dataset
            for row in data.get('filas', []):
                text = row.get('fila', {}).get('text', '')
                if text:
                    # Dividir en HUMAN y ASSISTANT
                    parts = text.split('\\u003CASSISTANT\\u003E:')
                    if len(parts) == 2:
                        question = parts[0].replace('\\u003CHUMAN\\u003E:', '').strip()
                        answer = parts[1].strip()
                        
                        # Limpiar texto
                        question = self.text_processor_es.clean_response_text(question)
                        answer = self.text_processor_es.clean_response_text(answer)
                        
                        if question and answer:
                            conversations.append({
                                'question': question,
                                'answer': answer,
                                'language': 'es',
                                'source': 'simple_dataset',
                                'processed_question': self.text_processor_es.preprocess_for_search(question),
                                'processed_answer': self.text_processor_es.preprocess_for_search(answer)
                            })
            
            print(f"Cargadas {len(conversations)} conversaciones del dataset simple")

            
            self.loaded_datasets.append('simple')
            return conversations
            
        except Exception as e:
            print(f"Error cargando dataset simple: {e}")
            return []
    
    def load_combined_dataset(self, file_path: str = None) -> List[Dict]:
        """
        Carga el dataset combinado en inglés
        """
        if file_path is None:
            file_path = DATASET_CONFIG['combined_dataset_path']
        
        try:
            conversations = []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            data = json.loads(line)
                            context = data.get('Context', '').strip()
                            response = data.get('Response', '').strip()
                            
                            if context and response:
                                # Limpiar texto
                                context = self.text_processor_en.clean_response_text(context)
                                response = self.text_processor_en.clean_response_text(response)
                                
                                conversations.append({
                                    'question': context,
                                    'answer': response,
                                    'language': 'en',
                                    'source': 'combined_dataset',
                                    'processed_question': self.text_processor_en.preprocess_for_search(context),
                                    'processed_answer': self.text_processor_en.preprocess_for_search(response)
                                })
                        except json.JSONDecodeError:
                            continue
            
            print(f"Cargadas {len(conversations)} conversaciones del dataset combinado")
            self.loaded_datasets.append('combined')
            return conversations
            
        except Exception as e:
            print(f"Error cargando dataset combinado: {e}")
            return []
    
    
    def load_simple_dataset_converted(self, file_path: str = None) -> List[Dict]:
        """
        Carga el dataset simple convertido (formato question/answer)
        """
        if file_path is None:
            file_path = 'data/simple_dataset_converted.json'
        
        try:
            if not os.path.exists(file_path):
                print(f"⚠️  Dataset convertido no encontrado: {file_path}")
                return []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                conversations = json.load(f)
            
            # Procesar para búsqueda
            for conv in conversations:
                conv['processed_question'] = self.text_processor_es.preprocess_for_search(conv['question'])
                conv['processed_answer'] = self.text_processor_es.preprocess_for_search(conv['answer'])
            
            print(f"✓ Dataset convertido cargado: {len(conversations)} conversaciones")
            self.loaded_datasets.append('simple_converted')
            return conversations
            
        except Exception as e:
            print(f"✗ Error cargando dataset convertido: {e}")
            return []

    def load_all_datasets(self) -> List[Dict]:
        """
        Carga todos los datasets disponibles con prioridad al convertido
        """
        all_conversations = []
        
        print("🔄 Cargando todos los datasets disponibles...")
        
        # 1. Intentar cargar dataset convertido primero (español)
        simple_converted_conversations = self.load_simple_dataset_converted()
        all_conversations.extend(simple_converted_conversations)
        
        # 2. Si no hay dataset convertido, intentar el original
        if not simple_converted_conversations:
            simple_conversations = self.load_simple_dataset()
            all_conversations.extend(simple_conversations)
        
        # 3. Cargar dataset combinado (inglés)
        combined_conversations = self.load_combined_dataset()
        all_conversations.extend(combined_conversations)
        
        self.conversations = all_conversations
        
        print(f"📊 RESUMEN DE CARGA:")
        print(f"   Total conversaciones: {len(all_conversations)}")
        print(f"   Datasets cargados: {', '.join(self.loaded_datasets)}")
        
        # Estadísticas por idioma
        es_count = len([c for c in all_conversations if c['language'] == 'es'])
        en_count = len([c for c in all_conversations if c['language'] == 'en'])
        print(f"   Español: {es_count} conversaciones")
        print(f"   Inglés: {en_count} conversaciones")
        
        return all_conversations
    
    def get_conversations_by_language(self, language: str) -> List[Dict]:
        """
        Obtiene conversaciones filtradas por idioma
        """
        return [conv for conv in self.conversations if conv['language'] == language]
    
    def get_all_questions(self, language: str = None) -> List[str]:
        """
        Obtiene todas las preguntas, opcionalmente filtradas por idioma
        """
        conversations = self.conversations
        if language:
            conversations = self.get_conversations_by_language(language)
        
        return [conv['processed_question'] for conv in conversations if conv['processed_question']]
    
    def get_all_answers(self, language: str = None) -> List[str]:
        """
        Obtiene todas las respuestas, opcionalmente filtradas por idioma
        """
        conversations = self.conversations
        if language:
            conversations = self.get_conversations_by_language(language)
        
        return [conv['processed_answer'] for conv in conversations if conv['processed_answer']]
    
    def search_by_keywords(self, keywords: List[str], language: str = None) -> List[Dict]:
        """
        Busca conversaciones que contengan las palabras clave especificadas
        """
        conversations = self.conversations
        if language:
            conversations = self.get_conversations_by_language(language)
        
        results = []
        keywords_lower = [kw.lower() for kw in keywords]
        
        for conv in conversations:
            question_text = conv['processed_question'].lower()
            answer_text = conv['processed_answer'].lower()
            
            # Verificar si alguna palabra clave está presente
            found_keywords = 0
            for keyword in keywords_lower:
                if keyword in question_text or keyword in answer_text:
                    found_keywords += 1
            
            if found_keywords > 0:
                conv_copy = conv.copy()
                conv_copy['keyword_matches'] = found_keywords
                conv_copy['relevance_score'] = found_keywords / len(keywords)
                results.append(conv_copy)
        
        # Ordenar por relevancia
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        return results
    
    def get_statistics(self) -> Dict:
        """
        Obtiene estadísticas de los datasets cargados
        """
        stats = {
            'total_conversations': len(self.conversations),
            'spanish_conversations': len(self.get_conversations_by_language('es')),
            'english_conversations': len(self.get_conversations_by_language('en')),
            'loaded_datasets': self.loaded_datasets,
            'avg_question_length': 0,
            'avg_answer_length': 0
        }
        
        if self.conversations:
            question_lengths = [len(conv['question'].split()) for conv in self.conversations]
            answer_lengths = [len(conv['answer'].split()) for conv in self.conversations]
            
            stats['avg_question_length'] = sum(question_lengths) / len(question_lengths)
            stats['avg_answer_length'] = sum(answer_lengths) / len(answer_lengths)
        
        return stats
    
    def export_to_csv(self, file_path: str, language: str = None):
        """
        Exporta las conversaciones a un archivo CSV
        """
        conversations = self.conversations
        if language:
            conversations = self.get_conversations_by_language(language)
        
        df = pd.DataFrame(conversations)
        df.to_csv(file_path, index=False, encoding='utf-8')
        print(f"Conversaciones exportadas a {file_path}")
