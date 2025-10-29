
import json

def generate_dorks(target_info: dict, platforms: dict, ai_integration: dict) -> list:
    """
    Genera una lista de dorks de búsqueda basados en la información del objetivo,
    las plataformas seleccionadas y las opciones de integración de IA.
    """
    dorks = []
    name = target_info.get('name', '')
    email = target_info.get('email', '')
    username = target_info.get('username', '')

    # Dorks básicos por nombre/usuario
    if name:
        dorks.append(f'"{name}"')
        dorks.append(f'intitle:"{name}"')
    if username:
        dorks.append(f'"{username}"')
        dorks.append(f'inurl:"{username}"')

    # Dorks por email
    if email:
        dorks.append(f'"{email}"')
        dorks.append(f'intext:"{email}"')

    # Dorks por plataforma
    if platforms.get('social_media', {}).get('enabled'):
        for platform in platforms['social_media'].get('specific_platforms', []):
            if name:
                dorks.append(f'site:{platform}.com "{name}"')
            if username:
                dorks.append(f'site:{platform}.com "{username}"')
            if email:
                dorks.append(f'site:{platform}.com "{email}"')

    if platforms.get('code_repositories', {}).get('enabled'):
        for platform in platforms['code_repositories'].get('specific_platforms', []):
            if name:
                dorks.append(f'site:{platform}.com "{name}"')
            if username:
                dorks.append(f'site:{platform}.com "{username}"')
            if email:
                dorks.append(f'site:{platform}.com "{email}"')

    # Dorks avanzados con IA (simulado por ahora)
    if ai_integration.get('dork_generation'):
        if name:
            dorks.append(f'"{name}" filetype:pdf resume') # Ejemplo de dork avanzado
            dorks.append(f'"{name}" inurl:cv OR inurl:resume')
        if username:
            dorks.append(f'"{username}" password OR credentials') # Ejemplo de dork para credenciales

    return list(set(dorks)) # Eliminar duplicados


# Ejemplo de uso (para pruebas)
if __name__ == "__main__":
    # Cargar una plantilla JSON de ejemplo (simulada)
    example_template = {
      "template_name": "busqueda_juan_perez",
      "description": "Búsqueda de información sobre Juan Pérez",
      "version": "1.0",
      "search_profile": {
        "type": "persona",
        "purpose": "investigación_antecedentes"
      },
      "target_info": {
        "name": "Juan Pérez",
        "email": "juan.perez@example.com",
        "username": "juanperezdev",
        "phone": "",
        "address": "",
        "social_media_handles": []
      },
      "search_parameters": {
        "platforms": {
          "social_media": {
            "enabled": True,
            "specific_platforms": ["linkedin", "twitter"]
          },
          "public_records": {
            "enabled": False
          },
          "dark_web": {
            "enabled": False
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
        "include_raw_data": False,
        "summarize_results": True,
        "visualize_connections": True
      },
      "ai_integration": {
        "dork_generation": True,
        "sentiment_analysis": False,
        "entity_extraction": True
      }
    }

    dorks_generated = generate_dorks(
        example_template['target_info'],
        example_template['search_parameters']['platforms'],
        example_template['ai_integration']
    )

    print("Dorks generados:")
    for dork in dorks_generated:
        print(dork)



