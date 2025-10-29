
import json
from dork_generator import generate_dorks

def simulate_osint_tool_adapter(template_path: str):
    """
    Simula un adaptador que toma una plantilla JSON, genera dorks y simula
    la ejecución de una herramienta OSINT y la recolección de resultados.
    """
    try:
        with open(template_path, 'r') as f:
            template = json.load(f)
    except FileNotFoundError:
        print(f"Error: La plantilla JSON no se encontró en {template_path}")
        return
    except json.JSONDecodeError:
        print(f"Error: El archivo {template_path} no es un JSON válido")
        return

    print(f"\n--- Simulando integración para la plantilla: {template.get('template_name', 'Desconocida')} ---")

    target_info = template.get('target_info', {})
    search_parameters = template.get('search_parameters', {})
    ai_integration = template.get('ai_integration', {})

    # 1. Generación de Dorks
    if ai_integration.get('dork_generation'):
        print("Generando dorks...")
        dorks = generate_dorks(
            target_info,
            search_parameters.get('platforms', {}),
            ai_integration
        )
        print(f"Dorks generados ({len(dorks)}):\n{json.dumps(dorks, indent=2)}")
    else:
        dorks = []
        print("Generación de dorks deshabilitada.")

    # 2. Simulación de ejecución de herramienta OSINT (ej. NUCLEI/OTE/SPIDERSUITE)
    print("\nSimulando ejecución de herramienta OSINT con los dorks...")
    # En un escenario real, aquí se invocaría la herramienta real con los dorks
    # y se procesaría su salida.
    simulated_raw_results = [
        {"source": "simulated_nuclei", "data": f"Found mention of {target_info.get('name', 'target')} on a blog post using dork: {dorks[0] if dorks else 'N/A'}"},
        {"source": "simulated_ote", "data": f"Email {target_info.get('email', 'N/A')} found in a pastebin link."},
        {"source": "simulated_spidersuite", "data": f"Profile for {target_info.get('username', 'N/A')} found on social media."}
    ]
    print(f"Resultados brutos simulados: {json.dumps(simulated_raw_results, indent=2)}")

    # 3. Simulación de procesamiento de resultados a la estructura de grafo
    print("\nProcesando resultados a la estructura de grafo...")
    # Esto simula el 'result_parser.py' mencionado en el plan de integración
    result_entities = []
    result_relationships = []
    raw_data_sources = []

    # Añadir la entidad principal (persona)
    if target_info.get('name'):
        person_id = f"person_{target_info['name'].replace(' ', '_').lower()}"
        result_entities.append({
            "id": person_id,
            "type": "person",
            "value": target_info['name'],
            "attributes": {}
        })

        if target_info.get('email'):
            email_id = f"email_{target_info['email']}"
            result_entities.append({"id": email_id, "type": "email", "value": target_info['email'], "attributes": {}})
            result_relationships.append({"source": person_id, "target": email_id, "type": "has_email", "attributes": {}})

        if target_info.get('username'):
            username_id = f"username_{target_info['username']}"
            result_entities.append({"id": username_id, "type": "username", "value": target_info['username'], "attributes": {}})
            result_relationships.append({"source": person_id, "target": username_id, "type": "has_username", "attributes": {}})

    for res in simulated_raw_results:
        raw_data_sources.append({
            "source_name": res['source'],
            "url": "simulated_url",
            "timestamp_collected": "2025-09-04T12:00:00Z"
        })

    final_result = {
        "query_details": template,
        "timestamp": "2025-09-04T12:00:00Z",
        "summary": "Resumen simulado de los hallazgos.",
        "entities": result_entities,
        "relationships": result_relationships,
        "raw_data_sources": raw_data_sources
    }

    print(f"Resultado final en formato de grafo:\n{json.dumps(final_result, indent=2)}")

    # Guardar el resultado simulado para posterior visualización
    output_filename = f"simulated_result_{template.get('template_name', 'unknown').replace(' ', '_')}.json"
    with open(output_filename, 'w') as f:
        json.dump(final_result, f, indent=2)
    print(f"Resultado simulado guardado en {output_filename}")

# Ejemplo de uso
if __name__ == "__main__":
    # Crear una plantilla de ejemplo para la simulación
    example_template_content = {
      "template_name": "busqueda_persona_ejemplo",
      "description": "Plantilla de ejemplo para simulación de búsqueda de persona",
      "version": "1.0",
      "search_profile": {
        "type": "persona",
        "purpose": "investigación_antecedentes"
      },
      "target_info": {
        "name": "Maria Garcia",
        "email": "maria.garcia@example.com",
        "username": "mariag_dev",
        "phone": "+34600123456",
        "address": "Calle Falsa 123",
        "social_media_handles": ["@mariag_tw", "/in/mariagarcia"]
      },
      "search_parameters": {
        "platforms": {
          "social_media": {
            "enabled": True,
            "specific_platforms": ["linkedin", "twitter", "facebook"]
          },
          "public_records": {
            "enabled": True,
            "types": ["birth_records"]
          },
          "code_repositories": {
            "enabled": True,
            "specific_platforms": ["github"]
          },
          "news_media": {
            "enabled": True
          }
        },
        "data_to_collect": {
          "emails": True,
          "phone_numbers": True,
          "addresses": True,
          "associated_names": True,
          "employment_history": True,
          "education_history": True,
          "online_mentions": True,
          "images": False,
          "videos": False
        },
        "depth": "medium",
        "time_frame": "all_time"
      },
      "output_format": {
        "type": "json",
        "include_raw_data": True,
        "summarize_results": True,
        "visualize_connections": True
      },
      "ai_integration": {
        "dork_generation": True,
        "sentiment_analysis": False,
        "entity_extraction": True
      }
    }

    template_filename = "example_person_template.json"
    with open(template_filename, 'w') as f:
        json.dump(example_template_content, f, indent=2)

    simulate_osint_tool_adapter(template_filename)



