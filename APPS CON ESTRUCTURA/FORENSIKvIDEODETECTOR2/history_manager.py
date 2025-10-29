import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path
import shutil
import uuid
import base64
import zipfile
import io
import numpy as np

class HistoryManager:
    """
    Versi optimal untuk Hugging Face Spaces dengan penyimpanan persisten
    """
    
    def __init__(self, history_file="analysis_history.json", history_folder="analysis_artifacts"):
        # Gunakan direktori persisten Hugging Face Spaces
        self.base_path = Path("/data") if Path("/data").exists() else Path("./data")
        self.base_path.mkdir(exist_ok=True, parents=True)
        
        # Path untuk file dan folder
        self.history_file = self.base_path / history_file
        self.history_folder = self.base_path / history_folder
        self.history_folder.mkdir(exist_ok=True)
        
        # Path database SQLite
        self.db_path = self.base_path / "analysis_settings.db"
        
        # Inisialisasi database
        self._init_db()
        
        # Buat file riwayat jika belum ada
        if not self.history_file.exists():
            with open(self.history_file, 'w') as f:
                json.dump([], f)
    
    def _init_db(self):
        """Inisialisasi database SQLite dengan error handling"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute(
                "CREATE TABLE IF NOT EXISTS settings (id TEXT PRIMARY KEY, video_name TEXT, timestamp TEXT, fps_awal REAL, fps_baru REAL, ssim_thresh REAL, z_thresh REAL)"
            )
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
    
    def convert_numpy_types(self, data):
        """Recursively convert numpy types and other non-serializable types to JSON-serializable types."""
        if data is None:
            return None
        elif isinstance(data, dict):
            return {k: self.convert_numpy_types(v) for k, v in data.items()}
        elif isinstance(data, (list, tuple)):
            return [self.convert_numpy_types(element) for element in data]
        elif isinstance(data, (np.floating, float)):
            if np.isnan(data) or np.isinf(data):
                return None  # Convert NaN/Inf to None for JSON compatibility
            return float(data)
        elif isinstance(data, (np.integer, int)):
            return int(data)
        elif isinstance(data, np.ndarray):
            try:
                return data.tolist()
            except:
                return str(data)  # Fallback to string representation
        elif isinstance(data, (np.bool_, bool)):
            return bool(data)
        elif isinstance(data, (Path, str)):
            return str(data)
        elif isinstance(data, bytes):
            try:
                return data.decode('utf-8')
            except:
                return base64.b64encode(data).decode('utf-8')
        elif hasattr(data, 'isoformat'):  # datetime objects
            return data.isoformat()
        elif hasattr(data, '__dict__'):
            # Handle objects with attributes
            try:
                converted_dict = {}
                for attr_name in dir(data):
                    if not attr_name.startswith('_') and not attr_name.startswith('__'):
                        try:
                            attr_value = getattr(data, attr_name)
                            if not callable(attr_value):
                                converted_dict[attr_name] = self.convert_numpy_types(attr_value)
                        except:
                            continue
                return converted_dict
            except:
                return str(data)  # Fallback to string representation
        elif hasattr(data, '__iter__') and not isinstance(data, (str, bytes)):
            # Handle other iterable types
            try:
                return [self.convert_numpy_types(item) for item in data]
            except:
                return str(data)
        else:
            # Try to convert to basic types, fallback to string
            try:
                if isinstance(data, (int, float, str, bool)):
                    return data
                else:
                    return str(data)
            except:
                return "<non-serializable object>"
    
    def save_analysis(self, result, video_name, additional_info=None):
        """Simpan analisis dengan penanganan error yang lebih baik"""
        try:
            # Convert the result object to handle all numpy types
            if isinstance(result, dict):
                result = self.convert_numpy_types(result)
            else:
                # Handle object with attributes
                result = self.convert_numpy_types(result)
            
            # Also convert additional_info if it exists
            if additional_info:
                additional_info = self.convert_numpy_types(additional_info)
                
            analysis_id = str(uuid.uuid4())
            
            # Buat folder artefak di direktori persisten
            artifact_folder = self.history_folder / analysis_id
            artifact_folder.mkdir(exist_ok=True)
            
            # Salin artefak visual penting ke folder riwayat.
            saved_artifacts = self._save_artifacts(result, artifact_folder)
            
            # Periksa tipe data input dan akses atribut dengan aman
            if isinstance(result, dict):
                # Jika input adalah dictionary, akses dengan bracket notation
                preservation_hash = result.get('preservation_hash', 'unknown')
                summary = result.get('summary', {})
                metadata = result.get('metadata', {})
                forensic_evidence_matrix = result.get('forensic_evidence_matrix')
                localization_details = result.get('localization_details')
                pipeline_assessment = result.get('pipeline_assessment')
                localizations = result.get('localizations', [])
                markdown_report_path = result.get('markdown_report_path')
            else:
                # Jika input adalah objek AnalysisResult, akses dengan dot notation
                preservation_hash = getattr(result, 'preservation_hash', 'unknown')
                summary = getattr(result, 'summary', {})
                metadata = getattr(result, 'metadata', {})
                forensic_evidence_matrix = getattr(result, 'forensic_evidence_matrix', None)
                localization_details = getattr(result, 'localization_details', None)
                pipeline_assessment = getattr(result, 'pipeline_assessment', None)
                localizations = getattr(result, 'localizations', [])
                markdown_report_path = getattr(result, 'markdown_report_path', None)
            
            # Struktur data riwayat yang akan disimpan ke JSON.
            history_entry = {
                "id": analysis_id,
                "timestamp": datetime.now().isoformat(),
                "video_name": video_name,
                "artifacts_folder": str(artifact_folder),
                "preservation_hash": preservation_hash,
                "summary": summary,
                "metadata": metadata,
                "forensic_evidence_matrix": forensic_evidence_matrix,
                "localization_details": localization_details,
                "pipeline_assessment": pipeline_assessment,
                "localizations": localizations,
                "localizations_count": len(localizations) if localizations else 0,
                "anomaly_types": self._count_anomaly_types(result),
                "saved_artifacts": saved_artifacts,
                "additional_info": additional_info if additional_info else {},
                "report_paths": { # Hanya menyimpan path laporan Markdown
                    "markdown": str(markdown_report_path) if markdown_report_path else None,
                },
            }
            
            # Convert the history_entry to ensure all numpy types are handled
            history_entry = self.convert_numpy_types(history_entry)
            
            history = self.load_history()
            # Pastikan history adalah list sebelum melakukan append
            if not isinstance(history, list):
                history = []
            
            # Convert history_entry to ensure all data is serializable
            history_entry = self.convert_numpy_types(history_entry)
            history.append(history_entry)
            
            # Enhanced error handling for JSON serialization
            try:
                with open(self.history_file, 'w') as f:
                    json.dump(history, f, indent=4)
            except TypeError as e:
                # If there's still a serialization error, try to identify and fix it
                print(f"JSON serialization error: {e}")
                # Create a simplified version of history_entry
                simplified_entry = {
                    "id": analysis_id,
                    "timestamp": datetime.now().isoformat(),
                    "video_name": str(video_name),
                    "artifacts_folder": str(artifact_folder),
                    "preservation_hash": str(preservation_hash) if preservation_hash else "unknown",
                    "summary": str(summary) if summary else {},
                    "metadata": str(metadata) if metadata else {},
                    "localizations_count": len(localizations) if localizations else 0,
                    "saved_artifacts": {k: str(v) for k, v in saved_artifacts.items()} if saved_artifacts else {},
                    "additional_info": str(additional_info) if additional_info else {},
                    "error_note": f"Simplified due to serialization error: {str(e)}"
                }
                history[-1] = simplified_entry  # Replace the problematic entry
                with open(self.history_file, 'w') as f:
                    json.dump(history, f, indent=4)

            # Simpan ke database dengan error handling
            try:
                conn = sqlite3.connect(self.db_path)
                conn.execute(
                    "INSERT INTO settings(id, video_name, timestamp, fps_awal, fps_baru, ssim_thresh, z_thresh) VALUES (?,?,?,?,?,?,?)",
                    (
                        analysis_id,
                        video_name,
                        history_entry["timestamp"],
                        additional_info.get("fps_awal") if additional_info else None,
                        additional_info.get("fps_baru") if additional_info else None,
                        additional_info.get("ssim_threshold") if additional_info else None,
                        additional_info.get("z_threshold") if additional_info else None,
                    ),
                )
                conn.commit()
                conn.close()
            except sqlite3.Error as e:
                print(f"Database save error: {e}")
            
            return analysis_id
        except Exception as e:
            print(f"Save analysis error: {e}")
            return None
    
    def load_history(self):
        """Memuat seluruh riwayat analisis dari file JSON."""
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            with open(self.history_file, 'w') as f:
                json.dump([], f)
            return []
    
    def get_analysis(self, analysis_id):
        """Mengambil satu entri riwayat berdasarkan ID uniknya."""
        history = self.load_history()
        return next((entry for entry in history if entry["id"] == analysis_id), None)
    
    def delete_analysis(self, analysis_id):
        """Menghapus satu entri riwayat dan semua artefak terkait."""
        history = self.load_history()
        
        entry_to_delete = self.get_analysis(analysis_id)
        if not entry_to_delete:
            return False

        artifact_folder = Path(entry_to_delete.get("artifacts_folder", ""))
        if artifact_folder.exists() and artifact_folder.is_dir():
            shutil.rmtree(artifact_folder)
        
        updated_history = [entry for entry in history if entry["id"] != analysis_id]
        
        with open(self.history_file, 'w') as f:
            json.dump(updated_history, f, indent=4)
                
        return True
    
    def delete_all_history(self):
        """Menghapus SEMUA riwayat analisis dan semua artefaknya."""
        history = self.load_history()
        count = len(history)
        
        if self.history_folder.exists():
            shutil.rmtree(self.history_folder)
        self.history_folder.mkdir(exist_ok=True)
        
        with open(self.history_file, 'w') as f:
            json.dump([], f)

        return count

    def _format_timestamp(self, iso_timestamp):
        """Memformat timestamp ISO menjadi format yang lebih mudah dibaca."""
        try:
            dt = datetime.fromisoformat(iso_timestamp)
            return dt.strftime("%d %B %Y, %H:%M:%S")
        except (ValueError, TypeError):
            return iso_timestamp
    
    def export_analysis(self, analysis_id):
        """Mengekspor data analisis lengkap (metadata + artefak) sebagai file ZIP."""
        entry = self.get_analysis(analysis_id)
        if not entry:
            return None
        
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Tambahkan laporan Markdown ke ZIP
            report_path_str = entry.get("report_paths", {}).get("markdown")
            if report_path_str and Path(report_path_str).exists():
                report_path = Path(report_path_str)
                zip_file.write(report_path, arcname=report_path.name)

            # Tambahkan semua artefak visual ke dalam folder 'artifacts' di dalam ZIP
            saved_artifacts = entry.get("saved_artifacts", {})
            for key, artifact_path_str in saved_artifacts.items():
                if "report" not in key: # Jangan sertakan laporan lagi
                    artifact_path = Path(artifact_path_str)
                    if artifact_path.exists() and artifact_path.is_file():
                        zip_file.write(artifact_path, arcname=f"artifacts/{artifact_path.name}")
        
        zip_buffer.seek(0)
        return zip_buffer.getvalue()
    
    def _count_anomaly_types(self, result):
        """Helper untuk menghitung jumlah setiap jenis anomali."""
        counts = {"duplication": 0, "insertion": 0, "discontinuity": 0}
        
        # Count from frames that have anomaly types
        frames = getattr(result, 'frames', [])
        if not frames and hasattr(result, 'get'):
            # Handle dict-like result
            frames = result.get('frames', [])
            
        for frame in frames:
            if hasattr(frame, 'get'):
                # Dict-like frame
                frame_type = frame.get('type', '')
            else:
                # Object-like frame
                frame_type = getattr(frame, 'type', '')
                
            if frame_type == 'anomaly_duplication':
                counts['duplication'] += 1
            elif frame_type == 'anomaly_insertion':
                counts['insertion'] += 1
            elif frame_type == 'anomaly_discontinuity':
                counts['discontinuity'] += 1
        
        # Also check localizations for backward compatibility
        localizations = getattr(result, 'localizations', [])
        if not localizations and hasattr(result, 'get'):
            localizations = result.get('localizations', [])
            
        for loc in localizations:
            if hasattr(loc, 'get'):
                event_type = str(loc.get('event', '')).replace('anomaly_', '')
            else:
                event_type = str(getattr(loc, 'event', '')).replace('anomaly_', '')
            if event_type in counts:
                counts[event_type] += 1
                
        return counts

    def cleanup_old_artifacts(self, max_age_days=30):
        """
        Hapus artefak lama untuk menghemat ruang penyimpanan
        Penting untuk Hugging Face Spaces yang memiliki batasan penyimpanan
        """
        try:
            now = datetime.now()
            deleted_count = 0
            
            # Hapus entri lama dari riwayat
            history = self.load_history()
            updated_history = []
            
            for entry in history:
                entry_time = datetime.fromisoformat(entry["timestamp"])
                age = (now - entry_time).days
                
                if age > max_age_days:
                    # Hapus folder artefak
                    artifact_folder = Path(entry.get("artifacts_folder", ""))
                    if artifact_folder.exists():
                        shutil.rmtree(artifact_folder)
                        deleted_count += 1
                else:
                    updated_history.append(entry)
            
            # Update file riwayat
            if deleted_count > 0:
                with open(self.history_file, 'w') as f:
                    json.dump(updated_history, f, indent=4)
                
                print(f"Deleted {deleted_count} old artifact folders")
                
            return deleted_count
        except Exception as e:
            print(f"Cleanup error: {e}")
            return 0
    
    def get_storage_usage(self):
        """Dapatkan informasi penggunaan penyimpanan"""
        try:
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(self.base_path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if os.path.isfile(fp):
                        total_size += os.path.getsize(fp)
            
            history = self.load_history()
            artifacts_count = len(list(self.history_folder.glob("*")))
            
            return {
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "history_count": len(history),
                "artifacts_count": artifacts_count
            }
        except Exception as e:
            print(f"Storage usage error: {e}")
            return {"error": str(e)}

    def _dir_size_bytes(self, path: Path) -> int:
        """Hitung ukuran direktori secara aman dalam byte."""
        total = 0
        try:
            for root, dirs, files in os.walk(path):
                for name in files:
                    fp = os.path.join(root, name)
                    try:
                        if os.path.isfile(fp):
                            total += os.path.getsize(fp)
                    except FileNotFoundError:
                        # File mungkin sudah terhapus saat iterasi berjalan
                        continue
        except Exception:
            pass
        return total

    def cleanup_system_storage(self) -> dict:
        """
        Bersihkan penyimpanan sistem TANPA menghapus riwayat analisis.

        Tindakan yang dilakukan secara aman:
        - Hapus folder kerja sementara yang tertinggal (mis. forensik_analysis_*)
        - Hapus artefak 'yatim' yang tidak lagi direferensikan oleh riwayat
        - Tidak mengubah file riwayat (JSON) maupun database settings

        Returns:
            dict: Ringkasan pembersihan (jumlah yang dihapus dan ruang yang dibebaskan)
        """
        summary = {
            "removed_temp_dirs": 0,
            "removed_orphan_artifacts": 0,
            "freed_mb": 0.0,
            "errors": []
        }

        try:
            before = self.get_storage_usage()
            before_bytes = int(before.get("total_size_mb", 0) * 1024 * 1024)

            # 1) Hapus folder sementara yang tertinggal di base_path
            for temp_dir in self.base_path.glob("forensik_analysis_*"):
                try:
                    if temp_dir.is_dir():
                        # Hitung ukuran sebelum dihapus untuk estimasi freed space
                        size_b = self._dir_size_bytes(temp_dir)
                        shutil.rmtree(temp_dir, ignore_errors=True)
                        summary["removed_temp_dirs"] += 1
                except Exception as e:
                    summary["errors"].append(f"TempDir {temp_dir.name}: {e}")

            # 2) Hapus artefak yang tidak lagi direferensikan oleh riwayat
            try:
                history = self.load_history()
                referenced = set()
                for entry in history:
                    try:
                        p = Path(entry.get("artifacts_folder", ""))
                        if p.name:
                            referenced.add(p.name)
                    except Exception:
                        continue

                for folder in self.history_folder.iterdir():
                    if folder.is_dir() and folder.name not in referenced:
                        try:
                            shutil.rmtree(folder, ignore_errors=True)
                            summary["removed_orphan_artifacts"] += 1
                        except Exception as e:
                            summary["errors"].append(f"Orphan {folder.name}: {e}")
            except Exception as e:
                summary["errors"].append(f"Scan artifacts: {e}")

            after = self.get_storage_usage()
            after_bytes = int(after.get("total_size_mb", 0) * 1024 * 1024)
            freed_b = max(0, before_bytes - after_bytes)
            summary["freed_mb"] = round(freed_b / (1024 * 1024), 2)

        except Exception as e:
            summary["errors"].append(str(e))

        return summary
    
    def _save_artifacts(self, result, folder):
        """Helper untuk menyalin artefak visual penting ke folder riwayat."""
        saved = {}

        # Safely access plots, which might not exist in all result objects
        plots = getattr(result, 'plots', {})
        if isinstance(plots, dict):
            for plot_name, plot_path in plots.items():
                if isinstance(plot_path, (str, Path)) and os.path.exists(plot_path):
                    target_path = folder / Path(plot_path).name
                    shutil.copy(plot_path, target_path)
                    saved[plot_name] = str(target_path)

        localizations = getattr(result, 'localizations', [])
        for i, loc in enumerate(localizations[:3]):  # Simpan hanya 3 contoh anomali pertama
            if loc.get('image') and os.path.exists(loc['image']):
                target_path = folder / f"sample_anomaly_frame_{i}.jpg"
                shutil.copy(loc['image'], target_path)
                saved[f"anomaly_frame_{i}"] = str(target_path) # Kunci menjadi 'anomaly_frame_0', 'anomaly_frame_1', dll

        if getattr(result, 'markdown_report_path', None) and os.path.exists(result.markdown_report_path):
            target_path = folder / Path(result.markdown_report_path).name
            shutil.copy(result.markdown_report_path, target_path)
            saved['markdown_report'] = str(target_path)
        
        return saved
    
    def get_artifact_base64(self, artifact_path):
        """Mengonversi file gambar artefak menjadi string base64 untuk ditampilkan di web."""
        path = Path(artifact_path)
        if not path.is_file():
            return None
            
        try:
            with open(path, "rb") as f:
                data = base64.b64encode(f.read()).decode('utf-8')
            mime_type = "image/png" if path.suffix.lower() == '.png' else "image/jpeg"
            return f"data:{mime_type};base64,{data}"
        except Exception:
            return None

    def get_anomaly_description(self, anomaly_type):
        """Menyediakan deskripsi lengkap untuk setiap jenis anomali."""
        descriptions = {
            "duplication": {
                "title": "Duplikasi Frame", "icon": "🔁", "color": "#FF6B6B",
                "simple": "Frame yang sama diulang beberapa kali dalam video.",
                "technical": "Dideteksi melalui perbandingan pHash dan dikonfirmasi dengan SIFT+RANSAC yang menemukan kecocokan fitur yang sangat tinggi antar frame.",
                "implication": "Ini bisa menjadi indikasi untuk memperpanjang durasi secara artifisial atau untuk menyembunyikan/menutupi konten yang telah dihapus di antara frame yang diduplikasi.",
                "example": "Seperti Anda menyalin sebuah halaman dari buku dan menempelkannya lagi di tempat lain untuk membuat buku terlihat lebih tebal."
            },
            "discontinuity": {
                "title": "Diskontinuitas Video", "icon": "✂️", "color": "#45B7D1",
                "simple": "Terjadi 'lompatan' atau patahan mendadak dalam aliran visual atau gerakan video.",
                "technical": "Dideteksi melalui penurunan drastis pada skor SSIM (kemiripan struktural) atau lonjakan tajam pada magnitudo Optical Flow (aliran gerakan).",
                "implication": "Seringkali ini adalah tanda kuat dari pemotongan (cut) dan penyambungan (paste) video. Aliran alami video terganggu.",
                "example": "Bayangkan sebuah kalimat di mana beberapa kata di tengahnya hilang, membuat kalimatnya terasa aneh dan melompat."
            },
            "insertion": {
                "title": "Penyisipan Konten", "icon": "➕", "color": "#4ECDC4",
                "simple": "Adanya frame atau segmen baru yang tidak ada di video asli/baseline.",
                "technical": "Dideteksi secara definitif dengan membandingkan hash setiap frame dari video bukti dengan video baseline. Frame yang ada di bukti tapi tidak di baseline dianggap sebagai sisipan.",
                "implication": "Ini adalah bukti kuat dari penambahan konten yang bisa mengubah konteks atau narasi video secara signifikan.",
                "example": "Seperti menambahkan sebuah paragraf karangan Anda sendiri ke tengah-tengah novel karya orang lain."
            }
        }
        return descriptions.get(anomaly_type, {
            "title": "Anomali Lain", "icon": "❓", "color": "#808080", "simple": "Jenis anomali tidak dikenali.",
            "technical": "-", "implication": "-", "example": "-"
        })
