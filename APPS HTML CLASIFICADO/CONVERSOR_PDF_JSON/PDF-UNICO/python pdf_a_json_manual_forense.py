# -*- coding: utf-8 -*-
"""
PDF → JSON estructurado
Script universal para manuales técnicos, criminalística, protocolos, etc.
Extrae texto, identifica capítulos, secciones, listas y tablas, y exporta a JSON.
"""

import fitz  # PyMuPDF
import re
import json

# === CONFIGURACIÓN ===
archivo_pdf = "ARCHIVO-MANUALDEBUENASPRACTICASENLAESCENA.pdf"
salida_json = "manual_buenas_practicas.json"

# === FUNCIÓN PRINCIPAL ===
def extraer_texto(pdf_path):
    """Extrae texto de cada página conservando saltos de línea."""
    texto_total = ""
    with fitz.open(pdf_path) as doc:
        for pagina in doc:
            texto_total += pagina.get_text("text") + "\n"
    return texto_total


def limpiar_texto(texto):
    """Limpia espacios y caracteres extraños."""
    texto = re.sub(r'\s+\n', '\n', texto)
    texto = re.sub(r'\n{2,}', '\n', texto)
    texto = texto.replace('', '-').replace('•', '-').replace('', '-')
    return texto.strip()


def segmentar_a_json(texto):
    """
    Detecta capítulos, secciones y procedimientos en el texto del manual.
    Devuelve una lista de diccionarios estructurados.
    """
    data = []
    capitulos = re.split(r'\n(?=CAP[IÍ]TULO\s+\d+)', texto, flags=re.IGNORECASE)

    for c_id, cap in enumerate(capitulos[1:], 1):
        # Nombre del capítulo
        match_cap = re.match(r'(CAP[IÍ]TULO\s+\d+\s*[-–]?\s*(.*))', cap.strip().split('\n')[0], flags=re.IGNORECASE)
        capitulo = match_cap.group(2).strip() if match_cap else f"Capítulo {c_id}"

        # Separar secciones (basado en subtítulos en mayúsculas)
        secciones = re.split(r'\n(?=[A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\s]{3,60}\n)', cap)
        for s_id, sec in enumerate(secciones, 1):
            lineas = sec.strip().split('\n')
            if not lineas:
                continue
            titulo = lineas[0].strip()
            cuerpo = "\n".join(lineas[1:]).strip()

            # Extraer procedimientos (viñetas, guiones, numeraciones)
            procedimientos = re.findall(r'(?:^|\n)[\-–•]\s*(.*)', cuerpo)
            instrumentos = re.findall(r'(instrumento|herramienta|material):\s*(.*)', cuerpo, re.IGNORECASE)

            data.append({
                "id": len(data) + 1,
                "capitulo": capitulo,
                "seccion": f"{s_id}",
                "titulo": titulo,
                "descripcion": cuerpo[:500] + ("..." if len(cuerpo) > 500 else ""),
                "procedimiento": procedimientos,
                "instrumentos": [i[1].strip() for i in instrumentos],
                "observaciones": "",
                "categoria": "Procedimiento de campo" if "procedimiento" in titulo.lower() else "Sección informativa"
            })

    return data


def main():
    texto = extraer_texto(archivo_pdf)
    texto_limpio = limpiar_texto(texto)
    dataset = segmentar_a_json(texto_limpio)

    with open(salida_json, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=4)

    print(f"✅ Dataset generado: {salida_json} ({len(dataset)} registros)")


if __name__ == "__main__":
    main()
