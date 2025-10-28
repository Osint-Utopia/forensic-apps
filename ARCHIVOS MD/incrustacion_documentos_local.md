# Incrustación de Documentos Locales sin APIs Externas

## MODELOS DE EMBEDDING LOCALES

### 1. Sentence Transformers (Recomendado)
```python
# Instalación
pip install sentence-transformers

# Modelos recomendados para español jurídico
from sentence_transformers import SentenceTransformer

# Opción 1: Multilingüe general
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

# Opción 2: Específico para español
model = SentenceTransformer('hiiamsid/sentence_similarity_spanish_es')

# Opción 3: Jurídico especializado (si disponible)
model = SentenceTransformer('law-ai/InLegalBERT')
```

### 2. Modelos Alternativos
```python
# BGE (Beijing Academy of AI)
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('BAAI/bge-m3')

# E5 (Microsoft)
model = SentenceTransformer('intfloat/multilingual-e5-large')

# Modelos específicos para código legal
model = SentenceTransformer('nlpaueb/legal-bert-base-uncased')
```

## PIPELINE COMPLETO DE PROCESAMIENTO

### 1. Preparación de Documentos
```python
import os
import PyPDF2
import docx
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import pickle

class DocumentProcessor:
    def __init__(self, model_name='paraphrase-multilingual-mpnet-base-v2'):
        self.model = SentenceTransformer(model_name)
        self.documents = []
        self.embeddings = None
        self.index = None
    
    def extract_text_from_pdf(self, pdf_path):
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text
    
    def extract_text_from_docx(self, docx_path):
        doc = docx.Document(docx_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    def chunk_text(self, text, chunk_size=500, overlap=50):
        """Divide texto en chunks con overlap para contexto"""
        chunks = []
        words = text.split()
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
        
        return chunks
```

### 2. Chunking Especializado para Documentos Jurídicos
```python
def legal_chunking(text, chunk_type='article'):
    """Chunking específico para documentos legales"""
    chunks = []
    
    if chunk_type == 'article':
        # Dividir por artículos
        articles = text.split('Artículo')
        for i, article in enumerate(articles[1:], 1):
            chunks.append(f"Artículo {article.strip()}")
    
    elif chunk_type == 'paragraph':
        # Dividir por párrafos legales
        paragraphs = text.split('\n\n')
        chunks = [p.strip() for p in paragraphs if len(p.strip()) > 50]
    
    elif chunk_type == 'section':
        # Dividir por secciones/capítulos
        sections = text.split('CAPÍTULO')
        for i, section in enumerate(sections[1:], 1):
            chunks.append(f"CAPÍTULO {section.strip()}")
    
    return chunks

def forensic_chunking(text):
    """Chunking para documentos periciales"""
    chunks = []
    
    # Dividir por secciones de dictamen
    sections = ['ANTECEDENTES', 'METODOLOGÍA', 'OBSERVACIONES', 
                'ANÁLISIS', 'CONCLUSIONES', 'RECOMENDACIONES']
    
    for section in sections:
        if section in text.upper():
            start = text.upper().find(section)
            # Encontrar siguiente sección o final
            next_sections = [s for s in sections if s != section and s in text.upper()[start:]]
            if next_sections:
                end = text.upper().find(next_sections[0], start)
                chunk = text[start:end].strip()
            else:
                chunk = text[start:].strip()
            
            if len(chunk) > 100:
                chunks.append(chunk)
    
    return chunks
```

### 3. Creación de Índice FAISS
```python
def create_faiss_index(self, documents_folder):
    """Crea índice FAISS para búsqueda rápida"""
    all_chunks = []
    all_metadata = []
    
    for filename in os.listdir(documents_folder):
        file_path = os.path.join(documents_folder, filename)
        
        # Extraer texto según tipo de archivo
        if filename.endswith('.pdf'):
            text = self.extract_text_from_pdf(file_path)
        elif filename.endswith('.docx'):
            text = self.extract_text_from_docx(file_path)
        elif filename.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        else:
            continue
        
        # Chunking especializado
        if 'codigo' in filename.lower() or 'ley' in filename.lower():
            chunks = legal_chunking(text, 'article')
        elif 'dictamen' in filename.lower() or 'peritaje' in filename.lower():
            chunks = forensic_chunking(text)
        else:
            chunks = self.chunk_text(text)
        
        # Agregar metadata
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_metadata.append({
                'filename': filename,
                'chunk_id': i,
                'text': chunk[:200] + '...' if len(chunk) > 200 else chunk
            })
    
    # Crear embeddings
    print(f"Creando embeddings para {len(all_chunks)} chunks...")
    embeddings = self.model.encode(all_chunks, show_progress_bar=True)
    
    # Crear índice FAISS
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)  # Producto interno para cosine similarity
    
    # Normalizar embeddings para cosine similarity
    faiss.normalize_L2(embeddings)
    index.add(embeddings.astype('float32'))
    
    # Guardar índice y metadata
    faiss.write_index(index, 'legal_documents.index')
    with open('legal_metadata.pkl', 'wb') as f:
        pickle.dump(all_metadata, f)
    
    print(f"Índice creado con {index.ntotal} documentos")
    return index, all_metadata
```

## SISTEMA DE BÚSQUEDA Y RECUPERACIÓN

### 1. Búsqueda Semántica
```python
class LegalRAG:
    def __init__(self, index_path='legal_documents.index', 
                 metadata_path='legal_metadata.pkl'):
        self.model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
        self.index = faiss.read_index(index_path)
        
        with open(metadata_path, 'rb') as f:
            self.metadata = pickle.load(f)
    
    def search_documents(self, query, top_k=5, threshold=0.7):
        """Búsqueda semántica en documentos"""
        # Crear embedding de la consulta
        query_embedding = self.model.encode([query])
        faiss.normalize_L2(query_embedding)
        
        # Buscar documentos similares
        scores, indices = self.index.search(query_embedding.astype('float32'), top_k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if score > threshold:
                results.append({
                    'score': float(score),
                    'metadata': self.metadata[idx],
                    'content': self.metadata[idx]['text']
                })
        
        return results
    
    def hybrid_search(self, query, keywords=None, top_k=5):
        """Búsqueda híbrida: semántica + palabras clave"""
        # Búsqueda semántica
        semantic_results = self.search_documents(query, top_k)
        
        # Filtrar por palabras clave si se proporcionan
        if keywords:
            filtered_results = []
            for result in semantic_results:
                content_lower = result['content'].lower()
                if any(keyword.lower() in content_lower for keyword in keywords):
                    filtered_results.append(result)
            return filtered_results
        
        return semantic_results
```

### 2. Integración con Mistral
```python
def create_context_prompt(query, search_results, max_context_length=3000):
    """Crea prompt con contexto de documentos relevantes"""
    context = "DOCUMENTOS RELEVANTES:\n\n"
    
    for i, result in enumerate(search_results[:3], 1):
        context += f"Documento {i} ({result['metadata']['filename']}):\n"
        context += f"{result['content']}\n\n"
    
    # Truncar si excede límite
    if len(context) > max_context_length:
        context = context[:max_context_length] + "...\n\n"
    
    prompt = f"{context}CONSULTA: {query}\n\nRespuesta basada en los documentos:"
    return prompt

# Uso con Mistral
def query_with_context(query, rag_system):
    # Buscar documentos relevantes
    results = rag_system.hybrid_search(query, top_k=3)
    
    # Crear prompt con contexto
    context_prompt = create_context_prompt(query, results)
    
    # Enviar a Mistral (usando tu cliente local)
    # response = mistral_client.generate(context_prompt)
    
    return context_prompt, results
```

## OPTIMIZACIONES ESPECÍFICAS

### 1. Para Códigos y Leyes
```python
# Preprocesamiento especializado
def preprocess_legal_text(text):
    """Limpieza específica para textos legales"""
    # Normalizar referencias
    text = re.sub(r'Art\.\s*(\d+)', r'Artículo \1', text)
    text = re.sub(r'Frac\.\s*([IVX]+)', r'Fracción \1', text)
    
    # Limpiar formato
    text = re.sub(r'\s+', ' ', text)  # Espacios múltiples
    text = re.sub(r'\n+', '\n', text)  # Saltos de línea múltiples
    
    return text

# Chunking por estructura legal
def structured_legal_chunking(text):
    """Chunking que respeta estructura legal"""
    chunks = []
    
    # Dividir por artículos manteniendo estructura
    article_pattern = r'(Artículo\s+\d+\.?[^Artículo]*)'
    articles = re.findall(article_pattern, text, re.IGNORECASE | re.DOTALL)
    
    for article in articles:
        # Dividir fracciones si el artículo es muy largo
        if len(article) > 1000:
            fraction_pattern = r'([IVX]+\.\s*[^IVX]*)'
            fractions = re.findall(fraction_pattern, article)
            if fractions:
                base_article = re.split(fraction_pattern, article)[0]
                chunks.append(base_article.strip())
                for fraction in fractions:
                    chunks.append(f"{base_article.split('.')[0]}. {fraction}")
            else:
                chunks.append(article.strip())
        else:
            chunks.append(article.strip())
    
    return chunks
```

### 2. Configuración de Hardware
```bash
# Instalación optimizada
pip install sentence-transformers[cpu]  # Solo CPU
pip install sentence-transformers[gpu]  # Con GPU

# Para modelos grandes con poca RAM
export TRANSFORMERS_CACHE=/path/to/large/storage
export HF_DATASETS_CACHE=/path/to/large/storage

# Configuración de FAISS
pip install faiss-cpu  # CPU
pip install faiss-gpu  # GPU
```

Este sistema te permitirá tener un RAG completamente local sin dependencias de APIs externas, optimizado para documentos jurídico-forenses.