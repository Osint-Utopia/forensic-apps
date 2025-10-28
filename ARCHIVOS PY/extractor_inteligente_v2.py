# extractor_inteligente_v2.py
# Procesa directorio completo, extrae por <title>, nomenclatura automática

import os
import re
import hashlib
from datetime import datetime
from pathlib import Path
import json

class ExtractorInteligente:
    """
    Extrae y organiza archivos HTML por <title>
    Mantiene metadata forense (hashes, fechas, etc)
    """
    
    def __init__(self, directorio_origen):
        self.dir_origen = Path(directorio_origen)
        self.dir_destino = Path("CARPETA DE ARCHIVOS EN GENERAL")
        self.registro = []
        self.setup_estructura()
    
    def setup_estructura(self):
        """Crea carpetas organizadas por tipo"""
        carpetas = {
            "apps": "01_APPS_COMPLETAS",
            "fragmentos": "02_FRAGMENTOS_CODIGO",
            "ideas": "03_IDEAS_TEXTO",
            "plantillas": "04_PLANTILLAS_JSON",
            "imagenes": "05_CAPTURAS_PANTALLA",
            "emails": "06_CORREOS_HISTORICOS",
            "notas": "07_NOTAS_SUELTAS",
            "sin_clasificar": "99_SIN_CLASIFICAR"
        }
        
        for carpeta in carpetas.values():
            (self.dir_destino / carpeta).mkdir(parents=True, exist_ok=True)
        
        # Carpeta especial para metadata
        (self.dir_destino / "00_METADATA").mkdir(exist_ok=True)
    
    def extraer_title_html(self, archivo):
        """
        Extrae <title> de archivos HTML
        """
        try:
            with open(archivo, 'r', encoding='utf-8', errors='ignore') as f:
                contenido = f.read()
            
            # Buscar <title>...</title>
            match = re.search(r'<title>(.*?)</title>', contenido, re.IGNORECASE | re.DOTALL)
            
            if match:
                title = match.group(1).strip()
                # Limpiar caracteres no permitidos en nombres de archivo
                title_limpio = re.sub(r'[<>:"/\\|?*]', '_', title)
                return title_limpio
            else:
                return None
        
        except Exception as e:
            print(f"⚠️ Error leyendo {archivo}: {e}")
            return None
    
    def detectar_tipo_archivo(self, archivo):
        """
        Clasifica archivo según contenido y extensión
        """
        extension = archivo.suffix.lower()
        
        # Leer primeras líneas para análisis
        try:
            with open(archivo, 'r', encoding='utf-8', errors='ignore') as f:
                primeras_lineas = f.read(2000)  # Primeros 2KB
        except:
            primeras_lineas = ""
        
        # Reglas de clasificación
        if extension == '.html':
            if '<script' in primeras_lineas or 'function' in primeras_lineas:
                return 'apps'
            elif 'artifact' in primeras_lineas.lower():
                return 'apps'
            else:
                return 'fragmentos'
        
        elif extension == '.py':
            if 'class ' in primeras_lineas and 'def ' in primeras_lineas:
                return 'apps'  # App completa
            else:
                return 'fragmentos'  # Script suelto
        
        elif extension in ['.json', '.yaml', '.yml']:
            return 'plantillas'
        
        elif extension in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
            return 'imagenes'
        
        elif extension in ['.txt', '.md']:
            if '@' in primeras_lineas and ('From:' in primeras_lineas or 'Subject:' in primeras_lineas):
                return 'emails'
            else:
                return 'notas'
        
        else:
            return 'sin_clasificar'
    
    def generar_nombre_inteligente(self, archivo, title=None):
        """
        Genera nombre siguiendo convención:
        [fecha_archivo]_[title_o_nombre_original]_[hash_corto].[ext]
        """
        
        # 1. Fecha de creación del archivo
        timestamp = os.path.getctime(archivo)
        fecha = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
        
        # 2. Título o nombre original
        if title:
            nombre_base = title[:50]  # Limitar a 50 caracteres
        else:
            nombre_base = archivo.stem[:50]
        
        # Limpiar nombre
        nombre_limpio = re.sub(r'[^\w\-_]', '_', nombre_base)
        
        # 3. Hash corto (primeros 8 caracteres) para unicidad
        with open(archivo, 'rb') as f:
            contenido = f.read()
            hash_completo = hashlib.sha256(contenido).hexdigest()
            hash_corto = hash_completo[:8]
        
        # 4. Extensión original
        extension = archivo.suffix
        
        # Construir nombre final
        nombre_final = f"{fecha}_{nombre_limpio}_{hash_corto}{extension}"
        
        return nombre_final
    
    def extraer_metadata_completa(self, archivo):
        """
        Extrae TODA la metadata posible (modo forense)
        """
        stat = os.stat(archivo)
        
        # Hash para integridad
        with open(archivo, 'rb') as f:
            contenido = f.read()
            hash_sha256 = hashlib.sha256(contenido).hexdigest()
            hash_md5 = hashlib.md5(contenido).hexdigest()
        
        metadata = {
            "nombre_original": archivo.name,
            "ruta_original": str(archivo.absolute()),
            "tamaño_bytes": stat.st_size,
            "creado": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modificado": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "accedido": datetime.fromtimestamp(stat.st_atime).isoformat(),
            "hash_sha256": hash_sha256,
            "hash_md5": hash_md5,
            "extension": archivo.suffix,
            "procesado": datetime.now().isoformat()
        }
        
        # Si es HTML, agregar title
        if archivo.suffix.lower() == '.html':
            title = self.extraer_title_html(archivo)
            metadata["title_html"] = title
        
        return metadata
    
    def procesar_archivo(self, archivo):
        """
        Proceso completo para UN archivo
        """
        print(f"📄 Procesando: {archivo.name}")
        
        # 1. Detectar tipo
        tipo = self.detectar_tipo_archivo(archivo)
        
        # 2. Extraer título si es HTML
        title = None
        if archivo.suffix.lower() == '.html':
            title = self.extraer_title_html(archivo)
        
        # 3. Generar nombre inteligente
        nombre_nuevo = self.generar_nombre_inteligente(archivo, title)
        
        # 4. Extraer metadata completa
        metadata = self.extraer_metadata_completa(archivo)
        metadata["tipo_clasificado"] = tipo
        metadata["nombre_nuevo"] = nombre_nuevo
        
        # 5. Determinar carpeta destino
        carpetas_map = {
            "apps": "01_APPS_COMPLETAS",
            "fragmentos": "02_FRAGMENTOS_CODIGO",
            "ideas": "03_IDEAS_TEXTO",
            "plantillas": "04_PLANTILLAS_JSON",
            "imagenes": "05_CAPTURAS_PANTALLA",
            "emails": "06_CORREOS_HISTORICOS",
            "notas": "07_NOTAS_SUELTAS",
            "sin_clasificar": "99_SIN_CLASIFICAR"
        }
        carpeta_destino = self.dir_destino / carpetas_map[tipo]
        
        # 6. Copiar archivo con nuevo nombre
        ruta_destino = carpeta_destino / nombre_nuevo
        
        # Evitar sobrescribir si ya existe
        contador = 1
        while ruta_destino.exists():
            nombre_base = ruta_destino.stem
            nombre_nuevo_unico = f"{nombre_base}_v{contador}{ruta_destino.suffix}"
            ruta_destino = carpeta_destino / nombre_nuevo_unico
            contador += 1
        
        # Copiar
        import shutil
        shutil.copy2(archivo, ruta_destino)
        
        metadata["ruta_destino"] = str(ruta_destino)
        
        # 7. Registrar en log
        self.registro.append(metadata)
        
        print(f"   ✅ → {tipo}/{nombre_nuevo}")
        
        return metadata
    
    def procesar_directorio_recursivo(self, directorio=None):
        """
        Procesa TODO un directorio y subdirectorios
        """
        if directorio is None:
            directorio = self.dir_origen
        
        print(f"\n🔍 Escaneando: {directorio}\n")
        
        archivos_procesados = 0
        errores = 0
        
        for archivo in Path(directorio).rglob('*'):
            if archivo.is_file():
                try:
                    self.procesar_archivo(archivo)
                    archivos_procesados += 1
                except Exception as e:
                    print(f"❌ Error con {archivo.name}: {e}")
                    errores += 1
        
        print(f"\n✅ Procesados: {archivos_procesados}")
        print(f"❌ Errores: {errores}")
        
        return archivos_procesados, errores
    
    def generar_indice(self):
        """
        Genera índice JSON con toda la metadata
        """
        archivo_indice = self.dir_destino / "00_METADATA" / "indice_completo.json"
        
        with open(archivo_indice, 'w', encoding='utf-8') as f:
            json.dump(self.registro, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 Índice generado: {archivo_indice}")
        
        # También generar versión Markdown legible
        self.generar_indice_markdown()
    
    def generar_indice_markdown(self):
        """
        Genera índice en Markdown para lectura humana
        """
        archivo_md = self.dir_destino / "00_METADATA" / "INDICE_LEGIBLE.md"
        
        with open(archivo_md, 'w', encoding='utf-8') as f:
            f.write("# 📚 ÍNDICE COMPLETO - ARCHIVO AL (1999-2025)\n\n")
            f.write(f"**Generado:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Total archivos:** {len(self.registro)}\n\n")
            f.write("---\n\n")
            
            # Agrupar por tipo
            por_tipo = {}
            for item in self.registro:
                tipo = item['tipo_clasificado']
                if tipo not in por_tipo:
                    por_tipo[tipo] = []
                por_tipo[tipo].append(item)
            
            # Escribir por tipo
            for tipo, items in por_tipo.items():
                f.write(f"## 📁 {tipo.upper()} ({len(items)} archivos)\n\n")
                
                for item in items:
                    f.write(f"### {item['nombre_nuevo']}\n\n")
                    f.write(f"- **Original:** `{item['nombre_original']}`\n")
                    if 'title_html' in item and item['title_html']:
                        f.write(f"- **Título:** {item['title_html']}\n")
                    f.write(f"- **Creado:** {item['creado'][:10]}\n")
                    f.write(f"- **Tamaño:** {item['tamaño_bytes']:,} bytes\n")
                    f.write(f"- **Hash:** `{item['hash_sha256'][:16]}...`\n")
                    f.write(f"- **Ubicación:** `{item['ruta_destino']}`\n")
                    f.write("\n---\n\n")
        
        print(f"📄 Índice Markdown: {archivo_md}")
    
    def generar_estadisticas(self):
        """
        Genera estadísticas del procesamiento
        """
        total = len(self.registro)
        
        # Por tipo
        por_tipo = {}
        for item in self.registro:
            tipo = item['tipo_clasificado']
            por_tipo[tipo] = por_tipo.get(tipo, 0) + 1
        
        # Por año
        por_año = {}
        for item in self.registro:
            año = item['creado'][:4]
            por_año[año] = por_año.get(año, 0) + 1
        
        # Tamaño total
        tamaño_total = sum(item['tamaño_bytes'] for item in self.registro)
        
        print("\n" + "="*50)
        print("📊 ESTADÍSTICAS")
        print("="*50)
        print(f"\n📂 Total archivos procesados: {total}")
        print(f"💾 Tamaño total: {tamaño_total / (1024**2):.2f} MB")
        
        print("\n📁 Por tipo:")
        for tipo, cantidad in sorted(por_tipo.items()):
            print(f"   {tipo}: {cantidad}")
        
        print("\n📅 Por año:")
        for año, cantidad in sorted(por_año.items()):
            print(f"   {año}: {cantidad}")
        
        print("\n" + "="*50)


# =============================================================================
# MODO DE USO
# =============================================================================

def main():
    """
    Función principal - ejecutar esto
    """
    
    print("""
╔════════════════════════════════════════════════════════╗
║                                                        ║
║     EXTRACTOR INTELIGENTE AL v2.0                      ║
║     Organiza 24 años de conocimiento (1999-2025)       ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
    """)
    
    # PASO 1: Pedir directorio de origen
    print("\n📂 Directorio a procesar:")
    print("   (Arrastra la carpeta aquí o escribe la ruta)")
    
    dir_origen = input("\nRuta: ").strip().strip('"')
    
    if not os.path.exists(dir_origen):
        print("❌ Directorio no existe")
        return
    
    # PASO 2: Confirmar
    print(f"\n🔍 Se procesarán TODOS los archivos en:")
    print(f"   {dir_origen}")
    print(f"\n📁 Se organizarán en:")
    print(f"   {os.path.join(os.getcwd(), 'CARPETA DE ARCHIVOS EN GENERAL')}")
    
    confirmar = input("\n¿Continuar? (s/n): ").lower()
    
    if confirmar != 's':
        print("❌ Cancelado")
        return
    
    # PASO 3: Procesar
    print("\n🚀 Iniciando procesamiento...\n")
    
    extractor = ExtractorInteligente(dir_origen)
    extractor.procesar_directorio_recursivo()
    
    # PASO 4: Generar índices
    print("\n📊 Generando índices...")
    extractor.generar_indice()
    extractor.generar_estadisticas()
    
    print("\n✅ ¡PROCESO COMPLETADO!")
    print(f"\n📂 Revisa la carpeta: {extractor.dir_destino}")

if __name__ == "__main__":
    main()