#!/usr/bin/env python3
"""
Script de prueba para el chatbot de salud mental
Prueba la funcionalidad sin interfaz gráfica
"""

import sys
import os

# Añadir el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_dataset_loading():
    """Prueba la carga de datasets"""
    print("=== PRUEBA DE CARGA DE DATASETS ===")
    
    try:
        from core import DatasetProcessor
        
        processor = DatasetProcessor()
        conversations = processor.load_all_datasets()
        
        print(f"✓ Datasets cargados exitosamente")
        print(f"  Total de conversaciones: {len(conversations)}")
        
        stats = processor.get_statistics()
        print(f"  Conversaciones en español: {stats['spanish_conversations']}")
        print(f"  Conversaciones en inglés: {stats['english_conversations']}")
        print(f"  Datasets cargados: {', '.join(stats['loaded_datasets'])}")
        
        return conversations
        
    except Exception as e:
        print(f"✗ Error cargando datasets: {e}")
        return None

def test_search_engine(conversations):
    """Prueba el motor de búsqueda"""
    print("\n=== PRUEBA DEL MOTOR DE BÚSQUEDA ===")
    
    if not conversations:
        print("✗ No hay conversaciones para probar")
        return None
    
    try:
        from core import SemanticSearchEngine
        
        search_engine = SemanticSearchEngine()
        search_engine.train(conversations)
        
        print("✓ Motor de búsqueda entrenado exitosamente")
        
        # Pruebas de búsqueda en español
        test_queries_es = [
            "¿Qué es la ansiedad?",
            "¿Cómo manejar el estrés?",
            "Síntomas de depresión"
        ]
        
        print("\n--- Pruebas en español ---")
        for query in test_queries_es:
            results = search_engine.search(query, language='es', max_results=2)
            print(f"\nConsulta: '{query}'")
            
            if results:
                best_result = results[0]
                print(f"  Mejor resultado (confianza: {best_result['similarity_score']:.2%}):")
                print(f"  Pregunta: {best_result['question'][:100]}...")
                print(f"  Respuesta: {best_result['answer'][:150]}...")
            else:
                print("  No se encontraron resultados")
        
        # Pruebas de búsqueda en inglés
        test_queries_en = [
            "What is anxiety?",
            "How to manage stress?",
            "Depression symptoms"
        ]
        
        print("\n--- Pruebas en inglés ---")
        for query in test_queries_en:
            results = search_engine.search(query, language='en', max_results=2)
            print(f"\nConsulta: '{query}'")
            
            if results:
                best_result = results[0]
                print(f"  Mejor resultado (confianza: {best_result['similarity_score']:.2%}):")
                print(f"  Pregunta: {best_result['question'][:100]}...")
                print(f"  Respuesta: {best_result['answer'][:150]}...")
            else:
                print("  No se encontraron resultados")
        
        return search_engine
        
    except Exception as e:
        print(f"✗ Error en motor de búsqueda: {e}")
        return None

def test_conversation_manager():
    """Prueba el gestor de conversaciones"""
    print("\n=== PRUEBA DEL GESTOR DE CONVERSACIONES ===")
    
    try:
        from core import ConversationManager
        
        manager = ConversationManager()
        
        # Probar mensajes básicos
        manager.add_message("Hola, ¿cómo estás?", "user")
        manager.add_message("¡Hola! Estoy aquí para ayudarte.", "bot")
        
        print("✓ Gestor de conversaciones funcionando")
        print(f"  Mensajes en historial: {len(manager.conversation_history)}")
        print(f"  Idioma actual: {manager.current_language}")
        
        # Probar cambio de idioma
        manager.set_language('en')
        welcome_en = manager.get_welcome_message()
        print(f"  Mensaje de bienvenida en inglés: {welcome_en[:50]}...")
        
        manager.set_language('es')
        welcome_es = manager.get_welcome_message()
        print(f"  Mensaje de bienvenida en español: {welcome_es[:50]}...")
        
        return manager
        
    except Exception as e:
        print(f"✗ Error en gestor de conversaciones: {e}")
        return None

def test_text_processing():
    """Prueba las utilidades de procesamiento de texto"""
    print("\n=== PRUEBA DE PROCESAMIENTO DE TEXTO ===")
    
    try:
        from utils import TextProcessor
        
        processor_es = TextProcessor('es')
        processor_en = TextProcessor('en')
        
        # Texto de prueba en español
        text_es = "¿Cómo puedo manejar la ansiedad y el estrés en mi vida diaria?"
        normalized_es = processor_es.normalize_text(text_es)
        processed_es = processor_es.preprocess_for_search(text_es)
        keywords_es = processor_es.extract_keywords(text_es)
        
        print("✓ Procesamiento de texto en español:")
        print(f"  Original: {text_es}")
        print(f"  Normalizado: {normalized_es}")
        print(f"  Procesado: {processed_es}")
        print(f"  Palabras clave: {keywords_es}")
        
        # Texto de prueba en inglés
        text_en = "How can I manage anxiety and stress in my daily life?"
        normalized_en = processor_en.normalize_text(text_en)
        processed_en = processor_en.preprocess_for_search(text_en)
        keywords_en = processor_en.extract_keywords(text_en)
        
        print("\n✓ Procesamiento de texto en inglés:")
        print(f"  Original: {text_en}")
        print(f"  Normalizado: {normalized_en}")
        print(f"  Procesado: {processed_en}")
        print(f"  Palabras clave: {keywords_en}")
        
        # Prueba de detección de idioma
        detected_es = processor_es.detect_language(text_es)
        detected_en = processor_es.detect_language(text_en)
        
        print(f"\n✓ Detección de idioma:")
        print(f"  Texto español detectado como: {detected_es}")
        print(f"  Texto inglés detectado como: {detected_en}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error en procesamiento de texto: {e}")
        return False

def interactive_test(search_engine):
    """Prueba interactiva del chatbot"""
    print("\n=== PRUEBA INTERACTIVA ===")
    print("Escribe preguntas para probar el chatbot (escribe 'salir' para terminar)")
    
    if not search_engine:
        print("✗ Motor de búsqueda no disponible")
        return
    
    while True:
        try:
            query = input("\nTu pregunta: ").strip()
            
            if query.lower() in ['salir', 'exit', 'quit']:
                break
            
            if not query:
                continue
            
            # Buscar respuesta
            results = search_engine.search(query, max_results=1)
            
            if results:
                result = results[0]
                print(f"\nUli responde (confianza: {result['similarity_score']:.1%}):")
                print(f"{result['answer']}")
                print(f"\n[Fuente: {result['source']}, Idioma: {result['language']}]")
            else:
                print("\nUli: Lo siento, no encontré información específica sobre tu consulta.")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\nError: {e}")
    
    print("\n¡Gracias por probar el chatbot!")

def main():
    """Función principal de prueba"""
    print("CHATBOT DE SALUD MENTAL - PRUEBAS")
    print("=" * 50)
    
    # Verificar dependencias básicas
    try:
        import sklearn
        import pandas
        import numpy
        from unidecode import unidecode
        print("✓ Todas las dependencias están instaladas")
    except ImportError as e:
        print(f"✗ Dependencia faltante: {e}")
        return
    
    # Ejecutar pruebas
    conversations = test_dataset_loading()
    search_engine = test_search_engine(conversations)
    conversation_manager = test_conversation_manager()
    text_processing_ok = test_text_processing()
    
    # Resumen de pruebas
    print("\n" + "=" * 50)
    print("RESUMEN DE PRUEBAS:")
    print(f"  Carga de datasets: {'✓' if conversations else '✗'}")
    print(f"  Motor de búsqueda: {'✓' if search_engine else '✗'}")
    print(f"  Gestor de conversaciones: {'✓' if conversation_manager else '✗'}")
    print(f"  Procesamiento de texto: {'✓' if text_processing_ok else '✗'}")
    
    if all([conversations, search_engine, conversation_manager, text_processing_ok]):
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        
        # Ofrecer prueba interactiva
        response = input("\n¿Quieres probar el chatbot interactivamente? (s/n): ")
        if response.lower() in ['s', 'si', 'sí', 'y', 'yes']:
            interactive_test(search_engine)
    else:
        print("\n❌ Algunas pruebas fallaron. Revisa los errores arriba.")

if __name__ == "__main__":
    main()
