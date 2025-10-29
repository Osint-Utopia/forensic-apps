
import gradio as gr
import numpy as np
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import joblib
import cv2

# === Load ResNet18 and Classifier ===
resnet = models.resnet18(weights='IMAGENET1K_V1')
resnet.fc = torch.nn.Identity()
resnet.eval()
transform = transforms.Compose([transforms.Resize((128, 128)), transforms.ToTensor()])

clf = joblib.load("logreg_cnn.pkl")
label_map = joblib.load("label_map.pkl")
inv_label_map = {v: k for k, v in label_map.items()}

gradients, activations = [], []

def backward_hook(module, grad_input, grad_output):
    gradients.append(grad_output[0])

def forward_hook(module, input, output):
    activations.append(output)

target_layer = resnet.layer4[-1]
target_layer.register_forward_hook(forward_hook)
target_layer.register_backward_hook(backward_hook)

# === Prediction Function ===
def predict_scanner(image):
    img = image.convert("RGB")
    tensor = transform(img).unsqueeze(0)

    with torch.no_grad():
        features = resnet(tensor).squeeze().numpy()

    pred = clf.predict([features])[0]
    proba = clf.predict_proba([features])[0][pred]
    label = inv_label_map[pred]

    # Grad-CAM
    resnet.zero_grad()
    output = resnet(tensor)
    output[0].mean().backward()

    grad = gradients[0].squeeze().detach().numpy()
    act = activations[0].squeeze().detach().numpy()
    weights = np.mean(grad, axis=(1, 2))
    cam = np.zeros(act.shape[1:], dtype=np.float32)
    for i, w in enumerate(weights):
        cam += w * act[i]
    cam = np.maximum(cam, 0)
    cam = cv2.resize(cam, (img.size[0], img.size[1]))
    cam = cam / cam.max()

    rgb_image = np.array(img) / 255.0
    heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
    overlay = np.uint8(255 * rgb_image)
    combined = cv2.addWeighted(overlay, 0.5, heatmap, 0.5, 0)

    return label, f"{proba:.2f}", combined[:, :, ::-1], image

# === Gradio UI ===
with gr.Blocks(css=".gradio-container {background-color: #ffffff; font-family: 'Segoe UI'; color: #2c3e50;}") as app:
    gr.Markdown("""
    <div style="text-align:center;">
        <h1 style="color:#2c3e50;">📄 TraceFinder - Forensic Scanner Identification</h1>
        <p style="font-size:16px;">Upload a scanned document image to identify the source scanner device.</p>
        <p style="font-size:14px; color:#7f8c8d;">Supported formats: .tiff, .png, .jpeg, .jpg</p>
    </div>
    """)

    with gr.Row():
        with gr.Column(scale=1):
            image_input = gr.Image(type="pil", label="📤 Upload Document Image", image_mode="RGB", sources=["upload", "clipboard"])
            submit_btn = gr.Button("🔍 Identify Scanner")
        with gr.Column(scale=1):
            label_output = gr.Text(label="🔖 Predicted Scanner Model")
            confidence_output = gr.Text(label="📊 Confidence Score")
            gradcam_output = gr.Image(label="🧭 Grad-CAM Visualization")
            uploaded_image_display = gr.Image(label="🖼️ Uploaded Image Preview")

    submit_btn.click(
        fn=predict_scanner,
        inputs=image_input,
        outputs=[label_output, confidence_output, gradcam_output, uploaded_image_display]
    )

    gr.Markdown("<p style='text-align:center; font-size:12px; color:#95a5a6;'>Developed by Ashwini | Infosys Virtual Project</p>")

app.launch()
