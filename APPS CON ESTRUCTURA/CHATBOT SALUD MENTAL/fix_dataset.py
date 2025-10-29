#!/usr/bin/env python3
"""
Script para corregir y optimizar los datasets JSON
"""

import json
import re
import sys
import os

def fix_simple_dataset(input_path, output_path):
    """
    Corrige el dataset simple eliminando caracteres de control problemáticos
    """
    print(f"Corrigiendo dataset: {input_path}")
    
    try:
        # Leer archivo con manejo de errores
        with open(input_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        # Limpiar caracteres de control problemáticos
        # Mantener solo caracteres imprimibles y espacios en blanco básicos
        cleaned_content = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', content)
        
        # Intentar parsear JSON
        data = json.loads(cleaned_content)
        
        conversations = []
        processed_count = 0
        error_count = 0
        
        for row in data.get('filas', []):
            try:
                text = row.get('fila', {}).get('text', '')
                if text:
                    # Limpiar marcadores HTML-like
                    text = text.replace('\\u003CHUMAN\\u003E:', '<HUMAN>:')
                    text = text.replace('\\u003CASSISTANT\\u003E:', '<ASSISTANT>:')
                    text = text.replace('\u003CHUMAN\u003E:', '<HUMAN>:')
                    text = text.replace('\u003CASSISTANT\u003E:', '<ASSISTANT>:')
                    
                    # Dividir en pregunta y respuesta
                    if '<ASSISTANT>:' in text:
                        parts = text.split('<ASSISTANT>:', 1)
                        if len(parts) == 2:
                            question = parts[0].replace('<HUMAN>:', '').strip()
                            answer = parts[1].strip()
                            
                            if question and answer and len(question) > 10 and len(answer) > 10:
                                conversations.append({
                                    'question': question,
                                    'answer': answer,
                                    'language': 'es',
                                    'source': 'simple_dataset_fixed',
                                    'row_idx': row.get('fila_idx', processed_count)
                                })
                                processed_count += 1
                            else:
                                error_count += 1
                        else:
                            error_count += 1
                    else:
                        error_count += 1
                else:
                    error_count += 1
                    
            except Exception as e:
                error_count += 1
                continue
        
        # Guardar dataset corregido
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(conversations, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Dataset corregido guardado en: {output_path}")
        print(f"  Conversaciones procesadas: {processed_count}")
        print(f"  Errores encontrados: {error_count}")
        print(f"  Tasa de éxito: {processed_count/(processed_count+error_count)*100:.1f}%")
        
        return conversations
        
    except Exception as e:
        print(f"✗ Error procesando dataset: {e}")
        return []

def analyze_dataset_usage():
    """
    Analiza el uso actual de los datasets
    """
    print("\n=== ANÁLISIS DE USO DE DATASETS ===")
    
    # Verificar archivos existentes
    data_dir = 'data'
    files = {
        'simple_dataset.json': 'Dataset simple (español)',
        'combined_dataset.json': 'Dataset combinado (inglés)',
        'simple_dataset_fixed.json': 'Dataset simple corregido'
    }
    
    total_conversations = 0
    
    for filename, description in files.items():
        filepath = os.path.join(data_dir, filename)
        
        if os.path.exists(filepath):
            try:
                file_size = os.path.getsize(filepath) / (1024 * 1024)  # MB
                print(f"\n📁 {description}")
                print(f"   Archivo: {filename}")
                print(f"   Tamaño: {file_size:.2f} MB")
                
                # Contar conversaciones según el formato
                if filename == 'simple_dataset.json':
                    # Formato original con estructura compleja
                    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                        try:
                            data = json.loads(f.read())
                            count = len(data.get('filas', []))
                            print(f"   Entradas: {count}")
                            print(f"   Estado: ⚠️ Problemas de formato detectados")
                        except:
                            print(f"   Estado: ❌ Error de formato JSON")
                            count = 0
                
                elif filename == 'combined_dataset.json':
                    # Formato JSONL
                    count = 0
                    with open(filepath, 'r', encoding='utf-8') as f:
                        for line in f:
                            if line.strip():
                                count += 1
                    print(f"   Conversaciones: {count}")
                    print(f"   Estado: ✅ Funcionando correctamente")
                    total_conversations += count
                
                elif filename == 'simple_dataset_fixed.json':
                    # Formato JSON array
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        count = len(data)
                        print(f"   Conversaciones: {count}")
                        print(f"   Estado: ✅ Corregido y funcionando")
                        total_conversations += count
                        
            except Exception as e:
                print(f"   Estado: ❌ Error: {e}")
        else:
            print(f"\n📁 {description}")
            print(f"   Archivo: {filename}")
            print(f"   Estado: ❌ No encontrado")
    
    print(f"\n📊 RESUMEN:")
    print(f"   Total conversaciones utilizables: {total_conversations}")
    print(f"   Potencial total si se corrige dataset simple: {total_conversations} + dataset simple")

def create_enhanced_loader():
    """
    Crea un cargador mejorado que use todos los datasets disponibles
    """
    enhanced_loader = '''
def load_all_datasets_enhanced(self):
    """
    Versión mejorada que carga todos los datasets disponibles
    """
    all_conversations = []
    
    # 1. Cargar dataset simple corregido (si existe)
    simple_fixed_path = 'data/simple_dataset_fixed.json'
    if os.path.exists(simple_fixed_path):
        try:
            with open(simple_fixed_path, 'r', encoding='utf-8') as f:
                simple_data = json.load(f)
                all_conversations.extend(simple_data)
                print(f"✓ Dataset simple corregido: {len(simple_data)} conversaciones")
        except Exception as e:
            print(f"✗ Error cargando dataset simple corregido: {e}")
    
    # 2. Cargar dataset combinado (inglés)
    combined_conversations = self.load_combined_dataset()
    all_conversations.extend(combined_conversations)
    
    # 3. Buscar datasets adicionales
    data_dir = 'data'
    for filename in os.listdir(data_dir):
        if filename.endswith('.json') and filename not in ['simple_dataset.json', 'combined_dataset.json', 'simple_dataset_fixed.json']:
            filepath = os.path.join(data_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    additional_data = json.load(f)
                    if isinstance(additional_data, list):
                        all_conversations.extend(additional_data)
                        print(f"✓ Dataset adicional {filename}: {len(additional_data)} conversaciones")
            except Exception as e:
                print(f"✗ Error cargando {filename}: {e}")
    
    self.conversations = all_conversations
    print(f"📊 Total conversaciones cargadas: {len(all_conversations)}")
    
    return all_conversations
'''
    
    print("\n=== CARGADOR MEJORADO ===")
    print("Para maximizar el uso de datos, agrega este método a dataset_processor.py:")
    print(enhanced_loader)

def suggest_improvements():
    """
    Sugiere mejoras para incrementar los datasets
    """
    print("\n=== SUGERENCIAS PARA INCREMENTAR DATASETS ===")
    
    suggestions = [
        {
            "título": "🔧 Corregir Dataset Simple",
            "descripción": "Ejecutar fix_dataset.py para recuperar conversaciones en español",
            "comando": "python3 fix_dataset.py"
        },
        {
            "título": "📥 Descargar Datasets Adicionales",
            "descripción": "Usar Hugging Face datasets para más conversaciones",
            "ejemplo": """
from datasets import load_dataset

# Ejemplos de datasets de salud mental
datasets = [
    "Amod/mental_health_counseling_conversations",
    "heliosbrahma/mental_health_chatbot_dataset",
    "alexandreteles/mental-health-conversational-data"
]

for dataset_name in datasets:
    try:
        dataset = load_dataset(dataset_name)
        # Convertir a formato compatible
        # Guardar en data/
    except:
        print(f"Dataset {dataset_name} no disponible")
"""
        },
        {
            "título": "🌐 Crear Dataset Personalizado",
            "descripción": "Agregar conversaciones específicas para tu dominio",
            "formato": """
[
  {
    "question": "Tu pregunta específica",
    "answer": "Tu respuesta específica", 
    "language": "es",
    "source": "custom_domain"
  }
]
"""
        },
        {
            "título": "🔄 Traducir Datasets",
            "descripción": "Usar Google Translate API para duplicar contenido en ambos idiomas",
            "beneficio": "Duplicar efectivamente el tamaño del dataset"
        }
    ]
    
    for i, suggestion in enumerate(suggestions, 1):
        print(f"\n{i}. {suggestion['título']}")
        print(f"   {suggestion['descripción']}")
        if 'comando' in suggestion:
            print(f"   Comando: {suggestion['comando']}")
        if 'ejemplo' in suggestion:
            print(f"   Ejemplo:{suggestion['ejemplo']}")
        if 'formato' in suggestion:
            print(f"   Formato:{suggestion['formato']}")
        if 'beneficio' in suggestion:
            print(f"   Beneficio: {suggestion['beneficio']}")

def main():
    """Función principal"""
    print("OPTIMIZADOR DE DATASETS - CHATBOT SALUD MENTAL")
    print("=" * 55)
    
    # Analizar uso actual
    analyze_dataset_usage()
    
    # Preguntar si corregir dataset simple
    print("\n" + "=" * 55)
    response = input("¿Quieres corregir el dataset simple ahora? (s/n): ")
    
    if response.lower() in ['s', 'si', 'sí', 'y', 'yes']:
        input_path = 'data/simple_dataset.json'
        output_path = 'data/simple_dataset_fixed.json'
        
        if os.path.exists(input_path):
            conversations = fix_simple_dataset(input_path, output_path)
            if conversations:
                print(f"\n🎉 ¡Dataset corregido! Ahora tienes {len(conversations)} conversaciones adicionales en español.")
        else:
            print(f"❌ No se encontró {input_path}")
    
    # Mostrar sugerencias
    suggest_improvements()
    
    # Mostrar cargador mejorado
    create_enhanced_loader()
    
    print("\n" + "=" * 55)
    print("Para aplicar las mejoras:")
    print("1. Ejecuta las correcciones sugeridas")
    print("2. Agrega el cargador mejorado a dataset_processor.py") 
    print("3. Reinicia el chatbot para cargar todos los datos")

if __name__ == "__main__":
    main()
