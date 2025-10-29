#!/usr/bin/env python3
"""
Script para procesar archivos .parquet del dataset clonado
"""

import pandas as pd
import json
import os
import sys

def install_required_packages():
    """Instala paquetes necesarios para procesar parquet"""
    try:
        import pyarrow
        print("✓ pyarrow ya está instalado")
    except ImportError:
        print("📦 Instalando pyarrow para procesar archivos .parquet...")
        os.system("pip3 install pyarrow")
        print("✓ pyarrow instalado")

def find_parquet_files(directory="."):
    """Busca archivos .parquet en el directorio"""
    parquet_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.parquet'):
                parquet_files.append(os.path.join(root, file))
    
    return parquet_files

def analyze_parquet_structure(file_path):
    """Analiza la estructura del archivo parquet"""
    try:
        df = pd.read_parquet(file_path)
        
        print(f"\n📊 ANÁLISIS DE {file_path}:")
        print(f"   Filas: {len(df)}")
        print(f"   Columnas: {len(df.columns)}")
        print(f"   Columnas disponibles: {list(df.columns)}")
        
        # Mostrar primeras filas
        print(f"\n📋 PRIMERAS 3 FILAS:")
        for i, row in df.head(3).iterrows():
            print(f"   Fila {i}:")
            for col in df.columns:
                value = str(row[col])[:100] + "..." if len(str(row[col])) > 100 else str(row[col])
                print(f"     {col}: {value}")
            print()
        
        return df
        
    except Exception as e:
        print(f"❌ Error analizando {file_path}: {e}")
        return None

def convert_parquet_to_json(df, output_path, format_type="auto"):
    """Convierte DataFrame a formato JSON para el chatbot"""
    
    conversations = []
    
    # Detectar formato automáticamente
    columns = [col.lower() for col in df.columns]
    
    print(f"🔍 Detectando formato del dataset...")
    print(f"   Columnas encontradas: {df.columns.tolist()}")
    
    # Patrones comunes para datasets de salud mental
    question_patterns = ['question', 'input', 'prompt', 'user', 'human', 'context', 'query']
    answer_patterns = ['answer', 'response', 'output', 'assistant', 'reply', 'completion']
    
    question_col = None
    answer_col = None
    
    # Buscar columnas de pregunta
    for pattern in question_patterns:
        for col in df.columns:
            if pattern in col.lower():
                question_col = col
                break
        if question_col:
            break
    
    # Buscar columnas de respuesta
    for pattern in answer_patterns:
        for col in df.columns:
            if pattern in col.lower():
                answer_col = col
                break
        if answer_col:
            break
    
    print(f"   Columna de pregunta detectada: {question_col}")
    print(f"   Columna de respuesta detectada: {answer_col}")
    
    if not question_col or not answer_col:
        print("⚠️  No se pudieron detectar columnas automáticamente")
        print("📋 Columnas disponibles:")
        for i, col in enumerate(df.columns):
            print(f"   {i}: {col}")
        
        try:
            q_idx = int(input("Selecciona el índice de la columna de PREGUNTAS: "))
            a_idx = int(input("Selecciona el índice de la columna de RESPUESTAS: "))
            
            question_col = df.columns[q_idx]
            answer_col = df.columns[a_idx]
            
            print(f"✓ Usando {question_col} como preguntas")
            print(f"✓ Usando {answer_col} como respuestas")
            
        except (ValueError, IndexError):
            print("❌ Selección inválida")
            return []
    
    # Procesar conversaciones
    processed_count = 0
    error_count = 0
    
    for idx, row in df.iterrows():
        try:
            question = str(row[question_col]).strip()
            answer = str(row[answer_col]).strip()
            
            # Filtrar entradas válidas
            if (question and answer and 
                question != 'nan' and answer != 'nan' and
                len(question) > 5 and len(answer) > 10):
                
                # Detectar idioma (simple heurística)
                spanish_words = ['qué', 'cómo', 'por', 'para', 'con', 'una', 'del', 'las', 'los', 'que', 'es', 'la', 'el']
                english_words = ['what', 'how', 'why', 'when', 'where', 'the', 'and', 'for', 'with', 'you', 'are', 'is']
                
                question_lower = question.lower()
                spanish_count = sum(1 for word in spanish_words if word in question_lower)
                english_count = sum(1 for word in english_words if word in question_lower)
                
                language = 'es' if spanish_count > english_count else 'en'
                
                conversations.append({
                    'question': question,
                    'answer': answer,
                    'language': language,
                    'source': 'parquet_dataset',
                    'original_index': idx
                })
                
                processed_count += 1
            else:
                error_count += 1
                
        except Exception as e:
            error_count += 1
            continue
    
    # Guardar resultado
    if conversations:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(conversations, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ CONVERSIÓN COMPLETADA:")
        print(f"   Conversaciones procesadas: {processed_count}")
        print(f"   Errores encontrados: {error_count}")
        print(f"   Archivo guardado: {output_path}")
        
        # Estadísticas por idioma
        es_count = len([c for c in conversations if c['language'] == 'es'])
        en_count = len([c for c in conversations if c['language'] == 'en'])
        print(f"   Conversaciones en español: {es_count}")
        print(f"   Conversaciones en inglés: {en_count}")
        
        return conversations
    else:
        print("❌ No se pudieron procesar conversaciones")
        return []

def merge_with_existing_datasets(new_conversations, output_dir="data"):
    """Fusiona las nuevas conversaciones con datasets existentes"""
    
    # Crear dataset combinado mejorado
    all_conversations = new_conversations.copy()
    
    # Cargar datasets existentes
    existing_files = [
        'simple_dataset_fixed.json',
        'combined_dataset.json'
    ]
    
    for filename in existing_files:
        filepath = os.path.join(output_dir, filename)
        if os.path.exists(filepath):
            try:
                if filename == 'combined_dataset.json':
                    # Formato JSONL
                    with open(filepath, 'r', encoding='utf-8') as f:
                        for line in f:
                            if line.strip():
                                data = json.loads(line)
                                all_conversations.append({
                                    'question': data.get('Context', ''),
                                    'answer': data.get('Response', ''),
                                    'language': 'en',
                                    'source': 'combined_dataset'
                                })
                else:
                    # Formato JSON array
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            all_conversations.extend(data)
                
                print(f"✓ Fusionado con {filename}")
                
            except Exception as e:
                print(f"⚠️  Error fusionando {filename}: {e}")
    
    # Guardar dataset mega-combinado
    mega_output = os.path.join(output_dir, 'mega_combined_dataset.json')
    with open(mega_output, 'w', encoding='utf-8') as f:
        json.dump(all_conversations, f, ensure_ascii=False, indent=2)
    
    print(f"\n🎉 DATASET MEGA-COMBINADO CREADO:")
    print(f"   Total conversaciones: {len(all_conversations)}")
    print(f"   Archivo: {mega_output}")
    
    return all_conversations

def main():
    """Función principal"""
    print("PROCESADOR DE DATASETS .PARQUET")
    print("=" * 40)
    
    # Instalar dependencias
    install_required_packages()
    
    # Buscar archivos parquet
    print("\n🔍 Buscando archivos .parquet...")
    parquet_files = find_parquet_files()
    
    if not parquet_files:
        print("❌ No se encontraron archivos .parquet")
        print("   Asegúrate de estar en el directorio correcto")
        print("   O especifica la ruta: python3 process_parquet_dataset.py /ruta/al/dataset")
        return
    
    print(f"✓ Encontrados {len(parquet_files)} archivos .parquet:")
    for i, file in enumerate(parquet_files):
        print(f"   {i}: {file}")
    
    # Procesar cada archivo
    all_new_conversations = []
    
    for file_path in parquet_files:
        print(f"\n{'='*50}")
        print(f"PROCESANDO: {file_path}")
        print(f"{'='*50}")
        
        # Analizar estructura
        df = analyze_parquet_structure(file_path)
        
        if df is not None:
            # Convertir a JSON
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            output_path = f"data/{base_name}_converted.json"
            
            # Crear directorio data si no existe
            os.makedirs("data", exist_ok=True)
            
            conversations = convert_parquet_to_json(df, output_path)
            all_new_conversations.extend(conversations)
    
    # Fusionar con datasets existentes
    if all_new_conversations:
        print(f"\n{'='*50}")
        print("FUSIONANDO CON DATASETS EXISTENTES")
        print(f"{'='*50}")
        
        mega_conversations = merge_with_existing_datasets(all_new_conversations)
        
        print(f"\n🎉 PROCESAMIENTO COMPLETADO:")
        print(f"   Nuevas conversaciones del .parquet: {len(all_new_conversations)}")
        print(f"   Total en mega-dataset: {len(mega_conversations)}")
        print(f"\nPara usar en el chatbot:")
        print(f"   1. Ejecuta: python3 integrate_fixed_dataset.py")
        print(f"   2. O modifica dataset_processor.py para cargar mega_combined_dataset.json")
    
    else:
        print("\n❌ No se procesaron conversaciones")

if __name__ == "__main__":
    # Permitir especificar directorio como argumento
    if len(sys.argv) > 1:
        os.chdir(sys.argv[1])
    
    main()
