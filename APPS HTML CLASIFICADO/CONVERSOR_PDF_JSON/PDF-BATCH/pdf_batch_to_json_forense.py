# -*- coding: utf-8 -*-
"""
Conversión masiva de PDFs a JSON estructurado.
Para manuales técnicos, criminalística, protocolos y guías.
"""

import fitz  # PyMuPDF
import re
import json
import os

# === CONFIGURACIÓN ===
carpeta_pdf = "manuales_pdf"   # carpeta donde guardas los PDFs
carpeta_salida = "datasets_json"  # carpeta donde se guardarán los JSON

os.makedirs(carpeta_salida, exist_ok=True)

def extraer_texto(pdf_path):
    texto_total = ""
    with fitz.open(pdf_path) as doc:
        for pagina in doc:
            texto_total += pagina.get_text("text") + "\n"
    return texto_total

def limpiar_texto(texto):
    texto = re.sub(r'\s+\n', '\n', texto)
    texto = re.sub(r'\n{2,}', '\n', texto)
    texto = texto.replace('', '-').replace('•', '-').replace('', '-')
    return texto.strip()

def segmentar_a_json(texto):
    data = []
    capitulos = re.split(r'\n(?=CAP[IÍ]TULO\s+\d+)', texto, flags=re.IGNORECASE)

    for c_id, cap in enumerate(capitulos[1:], 1):
        match_cap = re.match(r'(CAP[IÍ]TULO\s+\d+\s*[-–]?\s*(.*))', cap.strip().split('\n')[0], flags=re.IGNORECASE)
        capitulo = match_cap.group(2).strip() if match_cap else f"Capítulo {c_id}"

        secciones = re.split(r'\n(?=[A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\s]{3,60}\n)', cap)
        for s_id, sec in enumerate(secciones, 1):
            lineas = sec.strip().split('\n')
            if not lineas:
                continue
            titulo = lineas[0].strip()
            cuerpo = "\n".join(lineas[1:]).strip()
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

def procesar_pdf(pdf_path, carpeta_salida):
    nombre_base = os.path.splitext(os.path.basename(pdf_path))[0]
    salida_json = os.path.join(carpeta_salida, f"{nombre_base}.json")

    texto = extraer_texto(pdf_path)
    texto_limpio = limpiar_texto(texto)
    dataset = segmentar_a_json(texto_limpio)

    with open(salida_json, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=4)

    print(f"✅ {nombre_base}.json generado ({len(dataset)} registros)")

def main():
    pdfs = [f for f in os.listdir(carpeta_pdf) if f.lower().endswith(".pdf")]
    if not pdfs:
        print("⚠️ No se encontraron archivos PDF en la carpeta especificada.")
        return

    for pdf in pdfs:
        procesar_pdf(os.path.join(carpeta_pdf, pdf), carpeta_salida)

    print("\n🚀 Conversión masiva completada. Todos los JSON están en:", carpeta_salida)

if __name__ == "__main__":
    main()
