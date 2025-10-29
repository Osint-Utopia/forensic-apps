---
title: ForeInsight Video
emoji: 🔍
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: 1.49.1
app_file: streamlit_app.py
pinned: false
---

# ForeInsight Video: Sistem Deteksi Forensik Keaslian Video

## Deskripsi
ForeInsight Video adalah sistem profesional untuk mendeteksi manipulasi video menggunakan metode:
- **K-Means** untuk klasterisasi adegan
- **Localization Tampering** untuk deteksi anomali
- **ELA** (Error Level Analysis) untuk deteksi editing
- **SIFT** untuk pencocokan fitur

## Fitur Utama
- 🔍 **Deteksi Duplikasi Frame**: Identifikasi frame yang diulang
- ✂️ **Deteksi Diskontinuitas**: Temukan pemotongan/penghapusan frame
- ➕ **Deteksi Penyisipan**: Temukan frame asing dalam video
- 📊 **Analisis FERM**: Forensic Evidence Reliability Matrix
- 📄 **Laporan Lengkap**: Export hasil dalam PDF dan DOCX
- 📜 **Riwayat Analisis**: Simpan dan kelola hasil analisis sebelumnya

## Cara Menggunakan
1. Upload video bukti (format: MP4, AVI, MOV, MKV, max 200MB)
2. Upload video baseline (opsional, untuk perbandingan)
3. Atur parameter analisis (FPS dan threshold)
4. Klik "Jalankan Analisis Forensik"
5. Tunggu proses analisis selesai
6. Lihat hasil lengkap di tab yang tersedia
7. Download laporan dalam format PDF/DOCX

## Teknologi
- **Frontend**: Streamlit
- **Computer Vision**: OpenCV, scikit-image
- **Machine Learning**: scikit-learn (K-Means)
- **Image Processing**: PIL, imagehash
- **Visualization**: Matplotlib, Plotly
- **Reporting**: ReportLab, python-docx
- **Deployment**: Hugging Face Spaces

## Parameter Analisis
- **Frame Extraction FPS**: 1-30 fps (default: 10)
- **SSIM Threshold**: 0.20-0.50 (default: 0.30)
- **Optical Flow Z-score**: 3.0-8.0 (default: 4.0)
- **Auto Threshold**: Otomatis menyesuaikan parameter (recommended)

## Jenis Deteksi
### 1. Duplikasi Frame
- **Metode**: pHash comparison + SIFT+RANSAC
- **Konfirmasi**: SSIM analysis
- **Visualisasi**: Frame comparison dengan source frame

### 2. Diskontinuitas Video
- **Metode**: SSIM drop detection + Optical Flow spike
- **Konfirmasi**: K-Means cluster jump
- **Visualisasi**: Temporal plot dengan anomali marker

### 3. Penyisipan Frame
- **Metode**: Frame hash comparison dengan baseline
- **Konfirmasi**: ELA analysis untuk compression artifacts
- **Visualisasi**: Frame difference map

## Struktur Laporan
### Ringkasan Eksekutif
- Statistik analisis
- Penilaian reliabilitas FERM
- Temuan utama

### Investigasi Anomali
- Detail setiap peristiwa
- Bukti visual (frame, ELA, SIFT)
- Metrik teknis

### Analisis FERM
- Kesimpulan reliabilitas
- Kekuatan bukti
- Karakterisasi anomali
- Analisis kausalitas

### Metadata Video
- Format, resolusi, durasi
- Bitrate, codec information
- Creation/modification timestamp

## Batasan Sistem
- **Ukuran file maksimal**: 200MB
- **Format video**: MP4, AVI, MOV, MKV
- **Durasi analisis**: Bergantung pada ukuran video (1-10 menit)
- **Akurasi**: Tergantung kualitas video dan parameter threshold

## Tips untuk Hasil Optimal
1. Gunakan video dengan kualitas baik
2. Untuk deteksi penyisipan, sediakan video baseline
3. Sesuaikan threshold sesuai karakteristik video
4. Gunakan auto threshold untuk hasil yang konsisten
5. Periksa visualisasi temporal untuk memahami konteks anomali

## Developer
- **Nama**: [Nama Anda]
- **Institusi**: Universitas Halu Oleo
- **Email**: [email Anda]
- **Repository**: [Link GitHub jika ada]

## Lisensi
MIT License - lihat file LICENSE untuk detail

## Citation
Jika Anda menggunakan sistem ini dalam penelitian, mohon cite:
```bibtex
@software{foreinsight_video,
  title={ForeInsight Video: Sistem Deteksi Forensik Keaslian Video},
  author={[Nama Anda]},
  year={2024},
  url={https://huggingface.co/spaces/USERNAME/SPACE_NAME}
}