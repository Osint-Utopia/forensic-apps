import numpy as np
import torch
from PIL import Image

from transformers import AutoImageProcessor, AutoModel

# Modello base (addestrato su ImageNet) -- dimensione media.
# Puoi anche provare "google/vit-base-patch16-224" (senza -in21k),
# "openai/clip-vit-base-patch32", o altri modelli vision.
MODEL_NAME = "google/vit-base-patch16-224-in21k"

processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)
model.eval()  # Modalità di sola inferenza

def get_embedding(pil_image: Image.Image) -> np.ndarray:
    """
    Converte l'immagine PIL in embedding (vettore) usando il modello Vit.
    """
    # Prepara i tensori per il modello
    inputs = processor(images=pil_image, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    
    # outputs.last_hidden_state: [batch_size, seq_len, hidden_size]
    # Usiamo il mean pooling sui token dell'immagine per ottenere un vettore unico
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze()
    return embeddings.cpu().numpy()

def compare_signatures(pil_image1: Image.Image, pil_image2: Image.Image) -> float:
    """
    Estrae gli embedding da due firme e calcola la similarità (cosine similarity).
    Maggiore il valore, più simili (1 = identiche, 0 = ortogonali, -1 = opposte).
    """
    emb1 = get_embedding(pil_image1)
    emb2 = get_embedding(pil_image2)
    
    # Calcoliamo la cos similarity
    cos_sim = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
    return cos_sim


import gradio as gr

def gradio_compare_signatures(img1, img2):
    # Confronta le due firme e ritorna la similarità
    if img1 is None or img2 is None:
        return "Carica entrambe le firme."
    sim = compare_signatures(img1, img2)
    return f"Similarità (cosine): {sim:.4f}"

demo = gr.Interface(
    fn=gradio_compare_signatures,
    inputs=[gr.Image(type="pil"), gr.Image(type="pil")],
    outputs="text",
    title="Signature Similarity"
)

if __name__ == "__main__":
    demo.launch()
