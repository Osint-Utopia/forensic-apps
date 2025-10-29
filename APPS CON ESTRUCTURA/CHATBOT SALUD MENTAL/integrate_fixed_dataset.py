#!/usr/bin/env python3
"""
Script para integrar el dataset corregido al chatbot actual
"""

import os
import sys
import json
import shutil

def backup_current_processor():
    """Crear backup del procesador actual"""
    source = 'core/dataset_processor.py'
    backup = 'core/dataset_processor_backup.py'
    
    if os.path.exists(source):
        shutil.copy2(source, backup)
        print(f"✓ Backup creado: {backup}")
        return True
    return False

def update_dataset_processor():
    """Actualizar el procesador para incluir el dataset corregido"""
    
    enhanced_processor = '''"""
Procesador de datasets JSON para el chatbot de salud mental - VERSIÓN MEJORADA
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
    
    def load_simple_dataset_fixed(self, file_path: str = None) -> List[Dict]:
        """
        Carga el dataset simple corregido en español
        """
        if file_path is None:
            file_path = 'data/simple_dataset_fixed.json'
        
        try:
            if not os.path.exists(file_path):
                print(f"⚠️  Dataset corregido no encontrado: {file_path}")
                return []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            conversations = []
            
            for item in data:
                try:
                    question = item.get('question', '').strip()
                    answer = item.get('answer', '').strip()
                    
                    if question and answer:
                        # Limpiar y procesar
                        question = self.text_processor_es.clean_response_text(question)
                        answer = self.text_processor_es.clean_response_text(answer)
                        
                        if len(question) > 5 and len(answer) > 10:
                            conversations.append({
                                'question': question,
                                'answer': answer,
                                'language': 'es',
                                'source': 'simple_dataset_fixed',
                                'processed_question': self.text_processor_es.preprocess_for_search(question),
                                'processed_answer': self.text_processor_es.preprocess_for_search(answer)
                            })
                except Exception as e:
                    continue
            
            print(f"✓ Dataset simple corregido cargado: {len(conversations)} conversaciones")
            self.loaded_datasets.append('simple_fixed')
            return conversations
            
        except Exception as e:
            print(f"✗ Error cargando dataset simple corregido: {e}")
            return []
    
    def load_simple_dataset(self, file_path: str = None) -> List[Dict]:
        """
        Intenta cargar el dataset simple original (fallback)
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
                    parts = text.split('\\\\u003CASSISTANT\\\\u003E:')
                    if len(parts) == 2:
                        question = parts[0].replace('\\\\u003CHUMAN\\\\u003E:', '').strip()
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
            
            print(f"✓ Dataset simple original cargado: {len(conversations)} conversaciones")
            self.loaded_datasets.append('simple')
            return conversations
            
        except Exception as e:
            print(f"⚠️  No se pudo cargar dataset simple original: {e}")
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
            
            print(f"✓ Dataset combinado cargado: {len(conversations)} conversaciones")
            self.loaded_datasets.append('combined')
            return conversations
            
        except Exception as e:
            print(f"✗ Error cargando dataset combinado: {e}")
            return []
    
    def load_additional_datasets(self) -> List[Dict]:
        """
        Busca y carga datasets adicionales en la carpeta data/
        """
        additional_conversations = []
        data_dir = 'data'
        
        if not os.path.exists(data_dir):
            return additional_conversations
        
        # Archivos a ignorar (ya procesados)
        ignore_files = {
            'simple_dataset.json',
            'combined_dataset.json', 
            'simple_dataset_fixed.json'
        }
        
        for filename in os.listdir(data_dir):
            if filename.endswith('.json') and filename not in ignore_files:
                filepath = os.path.join(data_dir, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Detectar formato del dataset
                    if isinstance(data, list):
                        # Formato array directo
                        for item in data:
                            if isinstance(item, dict) and 'question' in item and 'answer' in item:
                                lang = item.get('language', 'es')
                                processor = self.text_processor_es if lang == 'es' else self.text_processor_en
                                
                                additional_conversations.append({
                                    'question': item['question'],
                                    'answer': item['answer'],
                                    'language': lang,
                                    'source': f'additional_{filename}',
                                    'processed_question': processor.preprocess_for_search(item['question']),
                                    'processed_answer': processor.preprocess_for_search(item['answer'])
                                })
                    
                    elif isinstance(data, dict):
                        # Otros formatos posibles
                        if 'conversations' in data:
                            for conv in data['conversations']:
                                # Procesar según estructura
                                pass
                    
                    if additional_conversations:
                        print(f"✓ Dataset adicional {filename}: {len(additional_conversations)} conversaciones")
                        self.loaded_datasets.append(f'additional_{filename}')
                
                except Exception as e:
                    print(f"⚠️  Error cargando {filename}: {e}")
                    continue
        
        return additional_conversations
    
    def load_all_datasets(self) -> List[Dict]:
        """
        Carga todos los datasets disponibles con prioridad al corregido
        """
        all_conversations = []
        
        print("🔄 Cargando todos los datasets disponibles...")
        
        # 1. Intentar cargar dataset simple corregido PRIMERO
        simple_fixed_conversations = self.load_simple_dataset_fixed()
        all_conversations.extend(simple_fixed_conversations)
        
        # 2. Si no hay dataset corregido, intentar el original
        if not simple_fixed_conversations:
            print("⚠️  Dataset corregido no disponible, intentando original...")
            simple_conversations = self.load_simple_dataset()
            all_conversations.extend(simple_conversations)
        
        # 3. Cargar dataset combinado (inglés)
        combined_conversations = self.load_combined_dataset()
        all_conversations.extend(combined_conversations)
        
        # 4. Buscar datasets adicionales
        additional_conversations = self.load_additional_datasets()
        all_conversations.extend(additional_conversations)
        
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
            'avg_answer_length': 0,
            'sources': {}
        }
        
        if self.conversations:
            question_lengths = [len(conv['question'].split()) for conv in self.conversations]
            answer_lengths = [len(conv['answer'].split()) for conv in self.conversations]
            
            stats['avg_question_length'] = sum(question_lengths) / len(question_lengths)
            stats['avg_answer_length'] = sum(answer_lengths) / len(answer_lengths)
            
            # Estadísticas por fuente
            for conv in self.conversations:
                source = conv['source']
                if source not in stats['sources']:
                    stats['sources'][source] = 0
                stats['sources'][source] += 1
        
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
        print(f"✓ Conversaciones exportadas a {file_path}")
'''
    
    # Escribir el procesador mejorado
    with open('core/dataset_processor.py', 'w', encoding='utf-8') as f:
        f.write(enhanced_processor)
    
    print("✓ Procesador de datasets actualizado")

def test_integration():
    """Probar la integración del dataset corregido"""
    print("\n🧪 PROBANDO INTEGRACIÓN...")
    
    try:
        # Importar el procesador actualizado
        sys.path.insert(0, '.')
        from core.dataset_processor import DatasetProcessor
        
        processor = DatasetProcessor()
        conversations = processor.load_all_datasets()
        
        if conversations:
            stats = processor.get_statistics()
            print(f"\n✅ INTEGRACIÓN EXITOSA:")
            print(f"   Total conversaciones: {stats['total_conversations']}")
            print(f"   Conversaciones en español: {stats['spanish_conversations']}")
            print(f"   Conversaciones en inglés: {stats['english_conversations']}")
            print(f"   Fuentes: {list(stats['sources'].keys())}")
            
            return True
        else:
            print("❌ No se cargaron conversaciones")
            return False
            
    except Exception as e:
        print(f"❌ Error en integración: {e}")
        return False

def main():
    """Función principal"""
    print("INTEGRADOR DE DATASET CORREGIDO")
    print("=" * 40)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('core/dataset_processor.py'):
        print("❌ Error: Ejecuta este script desde el directorio del chatbot")
        return
    
    # Verificar si existe el dataset corregido
    if os.path.exists('data/simple_dataset_fixed.json'):
        print("✓ Dataset corregido encontrado")
        
        # Mostrar información del dataset corregido
        try:
            with open('data/simple_dataset_fixed.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"  Conversaciones en dataset corregido: {len(data)}")
        except:
            print("  ⚠️ Error leyendo dataset corregido")
    else:
        print("⚠️ Dataset corregido no encontrado")
        print("   Asegúrate de haber ejecutado la corrección primero")
        return
    
    # Crear backup y actualizar
    print("\n🔄 Actualizando procesador...")
    backup_current_processor()
    update_dataset_processor()
    
    # Probar integración
    success = test_integration()
    
    if success:
        print("\n🎉 ¡INTEGRACIÓN COMPLETADA!")
        print("\nPara usar el chatbot con el dataset corregido:")
        print("  python3 main.py")
        print("\nPara ejecutar pruebas:")
        print("  python3 test_chatbot.py")
    else:
        print("\n❌ Integración falló")
        print("Restaurando backup...")
        if os.path.exists('core/dataset_processor_backup.py'):
            shutil.copy2('core/dataset_processor_backup.py', 'core/dataset_processor.py')
            print("✓ Backup restaurado")

if __name__ == "__main__":
    main()
