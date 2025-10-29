# pdf_batch_to_json_TUYO.py (versión mejorada)

import json
import re
from pathlib import Path

def extraer_tu_estilo(texto_whatsapp):
    """
    Extrae SOLO tus respuestas y analiza patrones
    """
    tus_respuestas = []
    conversaciones = []
    
    lineas = texto_whatsapp.split('\n')
    contexto = []
    
    for linea in lineas:
        # Detectar tus mensajes (ajusta el nombre)
        if re.search(r'\] (Tú|Tu_Nombre):', linea):
            respuesta = linea.split(': ', 1)[1] if ': ' in linea else linea
            
            conversacion = {
                "contexto_previo": contexto[-3:] if len(contexto) >= 3 else contexto,
                "tu_respuesta": respuesta,
                "longitud": len(respuesta),
                "tiene_humor": detectar_humor(respuesta),
                "es_directo": len(respuesta) < 50,
                "muletillas": extraer_muletillas(respuesta)
            }
            
            conversaciones.append(conversacion)
            contexto = []
        else:
            contexto.append(linea)
    
    return conversaciones

def detectar_humor(texto):
    """Detecta si la respuesta tiene humor/sarcasmo"""
    indicadores = ['jaja', 'pos', 'nel', 'mamada', 'cabrón', 'pendej']
    return any(ind in texto.lower() for ind in indicadores)

def extraer_muletillas(texto):
    """Identifica tus muletillas características"""
    muletillas = ['pos', 'nel', 'órale', 'básicamente', 'pues', 'o sea']
    encontradas = [m for m in muletillas if m in texto.lower()]
    return encontradas

def analizar_patron_respuesta(respuesta):
    """Clasifica el tipo de respuesta"""
    longitud = len(respuesta)
    
    if longitud < 30:
        return "ultra_directo"  # "Pos vete sin despedirte"
    elif longitud < 100:
        return "directo_pragmatico"  # Respuesta + acción
    elif longitud < 300:
        return "explicativo"  # Con fundamento técnico
    else:
        return "detallado"  # Caso complejo

def generar_dataset_entrenamiento(todos_los_whatsapp):
    """
    Convierte TODOS tus chats en dataset de entrenamiento
    """
    dataset = {
        "metadata": {
            "total_conversaciones": 0,
            "respuestas_directas": 0,
            "respuestas_humoristicas": 0,
            "promedio_longitud": 0
        },
        "conversaciones": [],
        "patrones_unicos": {
            "frases_de_apertura": [],
            "frases_de_cierre": [],
            "conectores_caracteristicos": []
        }
    }
    
    for archivo in Path("./whatsapp_exports/").glob("*.txt"):
        with open(archivo, 'r', encoding='utf-8') as f:
            texto = f.read()
            conversaciones = extraer_tu_estilo(texto)
            dataset["conversaciones"].extend(conversaciones)
    
    # Análisis estadístico
    dataset["metadata"]["total_conversaciones"] = len(dataset["conversaciones"])
    dataset["metadata"]["respuestas_directas"] = sum(
        1 for c in dataset["conversaciones"] if c["es_directo"]
    )
    dataset["metadata"]["respuestas_humoristicas"] = sum(
        1 for c in dataset["conversaciones"] if c["tiene_humor"]
    )
    
    return dataset

# Ejecución
if __name__ == "__main__":
    dataset = generar_dataset_entrenamiento("./whatsapp_exports/")
    
    with open("dataset_tu_estilo.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Dataset generado: {dataset['metadata']['total_conversaciones']} conversaciones")
    print(f"📊 Respuestas directas: {dataset['metadata']['respuestas_directas']}")
    print(f"😂 Con humor: {dataset['metadata']['respuestas_humoristicas']}")