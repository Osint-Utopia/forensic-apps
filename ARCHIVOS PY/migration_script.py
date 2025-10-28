#!/usr/bin/env python3
"""
Script de Migración para Reorganizar Proyecto ForensicWeb
Este script ayuda a migrar de la estructura actual a la nueva estructura propuesta.
"""

import os
import shutil
import json
from pathlib import Path

class ForensicMigrator:
    def __init__(self, source_abogados, source_forensic, target_dir):
        self.source_abogados = Path(source_abogados)
        self.source_forensic = Path(source_forensic)
        self.target_dir = Path(target_dir)
        self.migration_log = []
        
    def log_action(self, action, source, target, status="SUCCESS"):
        """Registrar acciones de migración"""
        self.migration_log.append({
            "action": action,
            "source": str(source),
            "target": str(target),
            "status": status
        })
        print(f"[{status}] {action}: {source} -> {target}")
    
    def create_directory_structure(self):
        """Crear la nueva estructura de directorios"""
        directories = [
            "shared/css",
            "shared/js", 
            "shared/images",
            "shared/webfonts",
            "abogadosforenses_org/main",
            "abogadosforenses_org/assets",
            "forensicweb/templates",
            "forensicweb/components/auth",
            "forensicweb/components/dashboard", 
            "forensicweb/components/legal",
            "forensicweb/components/users",
            "forensicweb/js",
            "forensicweb/css",
            "forensicweb/assets"
        ]
        
        for directory in directories:
            dir_path = self.target_dir / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            self.log_action("CREATE_DIR", "", dir_path)
    
    def migrate_shared_resources(self):
        """Migrar recursos compartidos (CSS, JS, imágenes)"""
        resource_types = ['css', 'js', 'images', 'webfonts']
        
        for resource_type in resource_types:
            # Migrar desde abogados
            source_path = self.source_abogados / resource_type
            if source_path.exists():
                target_path = self.target_dir / "shared" / resource_type
                self.copy_directory_contents(source_path, target_path, f"MIGRATE_SHARED_{resource_type.upper()}")
            
            # Comparar con forensicweb y migrar archivos únicos
            forensic_path = self.source_forensic / resource_type
            if forensic_path.exists():
                target_path = self.target_dir / "shared" / resource_type
                self.merge_directory_contents(forensic_path, target_path, f"MERGE_SHARED_{resource_type.upper()}")
    
    def migrate_abogados_site(self):
        """Migrar sitio de abogados"""
        # Copiar archivos HTML de la raíz
        html_files = ['index.html', 'blog.html']
        for html_file in html_files:
            source_file = self.source_abogados / html_file
            if source_file.exists():
                target_file = self.target_dir / "abogadosforenses_org" / html_file
                shutil.copy2(source_file, target_file)
                self.log_action("MIGRATE_HTML", source_file, target_file)
        
        # Migrar archivos de la carpeta main
        main_source = self.source_abogados / "main"
        if main_source.exists():
            main_target = self.target_dir / "abogadosforenses_org" / "main"
            self.copy_directory_contents(main_source, main_target, "MIGRATE_MAIN")
        
        # Migrar archivos específicos (no compartidos)
        specific_dirs = ['vscode']  # Directorios específicos del proyecto
        for specific_dir in specific_dirs:
            source_path = self.source_abogados / specific_dir
            if source_path.exists():
                target_path = self.target_dir / "abogadosforenses_org" / "assets" / specific_dir
                self.copy_directory_contents(source_path, target_path, f"MIGRATE_SPECIFIC_{specific_dir.upper()}")
    
    def migrate_forensicweb_dashboard(self):
        """Migrar dashboard de ForensicWeb"""
        # Copiar index.html
        index_file = self.source_forensic / "index.html"
        if index_file.exists():
            target_file = self.target_dir / "forensicweb" / "index.html"
            shutil.copy2(index_file, target_file)
            self.log_action("MIGRATE_INDEX", index_file, target_file)
        
        # Migrar archivos específicos
        specific_dirs = ['vscode']
        for specific_dir in specific_dirs:
            source_path = self.source_forensic / specific_dir
            if source_path.exists():
                target_path = self.target_dir / "forensicweb" / "assets" / specific_dir
                self.copy_directory_contents(source_path, target_path, f"MIGRATE_FORENSIC_{specific_dir.upper()}")
        
        # Crear mapeo de archivos HTML del dashboard
        main_source = self.source_forensic / "main"
        if main_source.exists():
            self.create_html_mapping(main_source)
    
    def create_html_mapping(self, main_dir):
        """Crear mapeo de archivos HTML para el nuevo sistema de componentes"""
        html_files = list(main_dir.glob("*.html"))
        
        mapping = {
            "total_files": len(html_files),
            "files": [],
            "suggested_components": {
                "auth": [],
                "dashboard": [],
                "legal": [],
                "users": [],
                "other": []
            }
        }
        
        # Categorizar archivos basándose en nombres comunes
        auth_keywords = ['login', 'register', 'auth', 'signin', 'signup']
        dashboard_keywords = ['dashboard', 'overview', 'stats', 'home', 'main']
        legal_keywords = ['legal', 'case', 'evidence', 'equipment', 'forensic']
        user_keywords = ['user', 'profile', 'admin', 'manage']
        
        for html_file in html_files:
            file_name = html_file.name.lower()
            file_info = {
                "original_name": html_file.name,
                "path": str(html_file),
                "suggested_component": "other"
            }
            
            # Categorizar archivo
            if any(keyword in file_name for keyword in auth_keywords):
                file_info["suggested_component"] = "auth"
                mapping["suggested_components"]["auth"].append(file_info)
            elif any(keyword in file_name for keyword in dashboard_keywords):
                file_info["suggested_component"] = "dashboard"
                mapping["suggested_components"]["dashboard"].append(file_info)
            elif any(keyword in file_name for keyword in legal_keywords):
                file_info["suggested_component"] = "legal"
                mapping["suggested_components"]["legal"].append(file_info)
            elif any(keyword in file_name for keyword in user_keywords):
                file_info["suggested_component"] = "users"
                mapping["suggested_components"]["users"].append(file_info)
            else:
                mapping["suggested_components"]["other"].append(file_info)
            
            mapping["files"].append(file_info)
        
        # Guardar mapeo
        mapping_file = self.target_dir / "html_mapping.json"
        with open(mapping_file, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, indent=2, ensure_ascii=False)
        
        self.log_action("CREATE_MAPPING", main_dir, mapping_file)
        
        return mapping
    
    def copy_directory_contents(self, source, target, action_prefix):
        """Copiar contenido de directorio"""
        if not source.exists():
            return
        
        target.mkdir(parents=True, exist_ok=True)
        
        for item in source.iterdir():
            if item.is_file():
                target_file = target / item.name
                shutil.copy2(item, target_file)
                self.log_action(f"{action_prefix}_FILE", item, target_file)
            elif item.is_dir():
                target_dir = target / item.name
                shutil.copytree(item, target_dir, dirs_exist_ok=True)
                self.log_action(f"{action_prefix}_DIR", item, target_dir)
    
    def merge_directory_contents(self, source, target, action_prefix):
        """Fusionar contenido de directorios, evitando duplicados"""
        if not source.exists():
            return
        
        target.mkdir(parents=True, exist_ok=True)
        
        for item in source.iterdir():
            target_item = target / item.name
            
            if item.is_file():
                if not target_item.exists():
                    shutil.copy2(item, target_item)
                    self.log_action(f"{action_prefix}_NEW_FILE", item, target_item)
                else:
                    # Comparar archivos y decidir si sobrescribir
                    if item.stat().st_size != target_item.stat().st_size:
                        backup_name = f"{item.name}.backup"
                        backup_path = target / backup_name
                        shutil.copy2(target_item, backup_path)
                        shutil.copy2(item, target_item)
                        self.log_action(f"{action_prefix}_REPLACE_FILE", item, target_item)
                        self.log_action(f"{action_prefix}_BACKUP", target_item, backup_path)
            elif item.is_dir():
                if not target_item.exists():
                    shutil.copytree(item, target_item)
                    self.log_action(f"{action_prefix}_NEW_DIR", item, target_item)
                else:
                    self.merge_directory_contents(item, target_item, action_prefix)
    
    def update_html_references(self):
        """Actualizar referencias en archivos HTML para usar recursos compartidos"""
        html_files = []
        
        # Encontrar todos los archivos HTML
        for root, dirs, files in os.walk(self.target_dir):
            for file in files:
                if file.endswith('.html'):
                    html_files.append(Path(root) / file)
        
        # Patrones de reemplazo para recursos compartidos
        replacements = {
            'css/': '../shared/css/',
            'js/': '../shared/js/',
            'images/': '../shared/images/',
            'webfonts/': '../shared/webfonts/',
            './css/': '../shared/css/',
            './js/': '../shared/js/',
            './images/': '../shared/images/',
            './webfonts/': '../shared/webfonts/'
        }
        
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Aplicar reemplazos
                for old_path, new_path in replacements.items():
                    content = content.replace(f'"{old_path}', f'"{new_path}')
                    content = content.replace(f"'{old_path}", f"'{new_path}")
                
                # Guardar si hubo cambios
                if content != original_content:
                    with open(html_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.log_action("UPDATE_REFERENCES", html_file, html_file)
                    
            except Exception as e:
                self.log_action("UPDATE_REFERENCES", html_file, html_file, f"ERROR: {str(e)}")
    
    def generate_migration_report(self):
        """Generar reporte de migración"""
        report_file = self.target_dir / "migration_report.json"
        
        report = {
            "migration_date": str(Path().cwd()),
            "source_directories": {
                "abogados": str(self.source_abogados),
                "forensicweb": str(self.source_forensic)
            },
            "target_directory": str(self.target_dir),
            "total_actions": len(self.migration_log),
            "actions": self.migration_log,
            "summary": {
                "successful_actions": len([a for a in self.migration_log if a["status"] == "SUCCESS"]),
                "failed_actions": len([a for a in self.migration_log if a["status"].startswith("ERROR")])
            }
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n=== REPORTE DE MIGRACIÓN ===")
        print(f"Acciones totales: {report['total_actions']}")
        print(f"Exitosas: {report['summary']['successful_actions']}")
        print(f"Fallidas: {report['summary']['failed_actions']}")
        print(f"Reporte guardado en: {report_file}")
        
        return report
    
    def run_migration(self):
        """Ejecutar migración completa"""
        print("Iniciando migración de proyecto ForensicWeb...")
        
        # Crear estructura de directorios
        print("\n1. Creando estructura de directorios...")
        self.create_directory_structure()
        
        # Migrar recursos compartidos
        print("\n2. Migrando recursos compartidos...")
        self.migrate_shared_resources()
        
        # Migrar sitio de abogados
        print("\n3. Migrando sitio de abogados...")
        self.migrate_abogados_site()
        
        # Migrar dashboard ForensicWeb
        print("\n4. Migrando dashboard ForensicWeb...")
        self.migrate_forensicweb_dashboard()
        
        # Actualizar referencias
        print("\n5. Actualizando referencias en archivos HTML...")
        self.update_html_references()
        
        # Generar reporte
        print("\n6. Generando reporte de migración...")
        report = self.generate_migration_report()
        
        print("\n¡Migración completada!")
        return report

def main():
    """Función principal"""
    print("=== SCRIPT DE MIGRACIÓN FORENSICWEB ===")
    print("Este script migra tu proyecto actual a la nueva estructura propuesta.")
    print()
    
    # Solicitar rutas (en un caso real, estas serían argumentos o configuración)
    source_abogados = input("Ruta de abogadosforenses_org: ").strip()
    source_forensic = input("Ruta de forensicweb: ").strip()
    target_dir = input("Directorio destino (por defecto: ./FORENSIC_REORGANIZED): ").strip()
    
    if not target_dir:
        target_dir = "./FORENSIC_REORGANIZED"
    
    # Validar rutas
    if not os.path.exists(source_abogados):
        print(f"Error: No se encuentra el directorio {source_abogados}")
        return
    
    if not os.path.exists(source_forensic):
        print(f"Error: No se encuentra el directorio {source_forensic}")
        return
    
    # Confirmar migración
    print(f"\nConfiguración de migración:")
    print(f"  Origen abogados: {source_abogados}")
    print(f"  Origen forensic: {source_forensic}")
    print(f"  Destino: {target_dir}")
    
    confirm = input("\n¿Continuar con la migración? (s/N): ").strip().lower()
    if confirm not in ['s', 'si', 'sí', 'y', 'yes']:
        print("Migración cancelada.")
        return
    
    # Ejecutar migración
    migrator = ForensicMigrator(source_abogados, source_forensic, target_dir)
    migrator.run_migration()

if __name__ == "__main__":
    main()
