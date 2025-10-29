#!/usr/bin/env python3
"""
Script para convertir el archivo HUMANO.json al formato compatible con el chatbot
"""

import json
import os

def convert_humano_json():
    """Convierte el formato humano/asistente al formato question/answer"""
    
    input_file = 'data/simple_dataset_fixed.json'
    output_file = 'data/simple_dataset_converted.json'
    
    print("🔄 Convirtiendo formato del dataset español...")
    
    try:
        # Leer archivo original
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✓ Archivo original cargado: {len(data)} conversaciones")
        
        # Convertir formato
        converted_conversations = []
        
        for i, item in enumerate(data):
            try:
                question = item.get('humano', '').strip()
                answer = item.get('asistente', '').strip()
                
                if question and answer:
                    converted_conversations.append({
                        'question': question,
                        'answer': answer,
                        'language': 'es',
                        'source': 'humano_dataset',
                        'original_index': i
                    })
                else:
                    print(f"⚠️  Conversación {i} vacía o incompleta")
                    
            except Exception as e:
                print(f"⚠️  Error procesando conversación {i}: {e}")
                continue
        
        # Guardar archivo convertido
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(converted_conversations, f, ensure_ascii=False, indent=2)
        
        print(f"✅ CONVERSIÓN COMPLETADA:")
        print(f"   Conversaciones convertidas: {len(converted_conversations)}")
        print(f"   Archivo guardado: {output_file}")
        
        # Mostrar estadísticas
        avg_question_length = sum(len(c['question'].split()) for c in converted_conversations) / len(converted_conversations)
        avg_answer_length = sum(len(c['answer'].split()) for c in converted_conversations) / len(converted_conversations)
        
        print(f"   Promedio palabras por pregunta: {avg_question_length:.1f}")
        print(f"   Promedio palabras por respuesta: {avg_answer_length:.1f}")
        
        # Mostrar muestra
        print(f"\n📋 MUESTRA DE CONVERSACIÓN CONVERTIDA:")
        sample = converted_conversations[0]
        print(f"   Pregunta: {sample['question'][:100]}...")
        print(f"   Respuesta: {sample['answer'][:100]}...")
        
        return converted_conversations
        
    except Exception as e:
        print(f"❌ Error en conversión: {e}")
        return []

def update_processor_for_converted_dataset():
    """Actualiza el procesador para usar el dataset convertido"""
    
    processor_file = 'core/dataset_processor.py'
    
    # Leer procesador actual
    with open(processor_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Agregar método para cargar dataset convertido
    new_method = '''
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
'''
    
    # Insertar el nuevo método antes del método load_all_datasets
    if 'def load_simple_dataset_converted' not in content:
        insertion_point = content.find('def load_all_datasets(self)')
        if insertion_point != -1:
            content = content[:insertion_point] + new_method + '\n    ' + content[insertion_point:]
            
            # Actualizar load_all_datasets para usar el dataset convertido
            old_load_call = 'simple_fixed_conversations = self.load_simple_dataset_fixed()'
            new_load_call = '''# Intentar cargar dataset convertido primero
        simple_converted_conversations = self.load_simple_dataset_converted()
        all_conversations.extend(simple_converted_conversations)
        
        # Si no hay dataset convertido, intentar el corregido
        if not simple_converted_conversations:
            simple_fixed_conversations = self.load_simple_dataset_fixed()
            all_conversations.extend(simple_fixed_conversations)'''
            
            content = content.replace(old_load_call, new_load_call)
            
            # Escribir archivo actualizado
            with open(processor_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✓ Procesador actualizado para usar dataset convertido")
            return True
    
    print("✓ Procesador ya está actualizado")
    return True

def main():
    """Función principal"""
    print("CONVERTIDOR DE DATASET HUMANO.JSON")
    print("=" * 40)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('core/dataset_processor.py'):
        print("❌ Error: Ejecuta este script desde el directorio del chatbot")
        return
    
    # Verificar que existe el archivo
    if not os.path.exists('data/simple_dataset_fixed.json'):
        print("❌ Error: No se encontró data/simple_dataset_fixed.json")
        return
    
    # Convertir dataset
    conversations = convert_humano_json()
    
    if conversations:
        # Actualizar procesador
        print(f"\n🔄 Actualizando procesador...")
        update_processor_for_converted_dataset()
        
        print(f"\n🎉 ¡CONVERSIÓN COMPLETADA!")
        print(f"\nAhora tienes:")
        print(f"   ✅ {len(conversations)} conversaciones en español")
        print(f"   ✅ Formato compatible con el chatbot")
        print(f"   ✅ Procesador actualizado")
        
        print(f"\nPara probar el chatbot:")
        print(f"   python3 test_chatbot.py")
        print(f"\nPara ejecutar el chatbot:")
        print(f"   python3 main.py")
    else:
        print(f"\n❌ Error en la conversión")

if __name__ == "__main__":
    main()
