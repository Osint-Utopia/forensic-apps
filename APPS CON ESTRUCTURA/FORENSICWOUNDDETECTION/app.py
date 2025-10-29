import gradio as gr
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image

# ------------------- Wound Descriptions -------------------
wound_descriptions = {
    "wound_hesitation": "บาดแผลลังเล (Hesitation wound): มักพบในผู้พยายามทำร้ายตนเอง...",
    "wound_laceration": "บาดแผลฉีกขาดขอบไม่เรียบ (Laceration): เกิดจากวัตถุแข็ง...",
    "wound_open_fracture": "บาดแผลกระดูกหักแบบเปิด (open fracture): เกิดจากกระดูกหักทิ่ม...",
    "wound_burn": "บาดแผลไหม้ (burn): บาดแผลที่เกิดจากการไหม้...",
    "wound_hanging": "บาดแผลกดรัดบริเวณลำคอ แขวนคอ (hanging)...",
    "wound_strangulation": "บาดแผลกดรัดบริเวณลำคอ รัดคอ (strangulation)...",
    "gsw_entrance": "บาดแผลทางเข้ากระสุนปืน...",
    "gsw_exit": "บาดแผลทางออกกระสุนปืน..."
}

# ------------------- Load Model -------------------
model = YOLO("models/best.pt")

# ------------------- Detection Function -------------------
def detect_wounds(image, conf_thresh=0.25):
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Run YOLO detection
    results = model(img_cv, conf=conf_thresh)
    annotated_bgr = results[0].plot()
    annotated_rgb = cv2.cvtColor(annotated_bgr, cv2.COLOR_BGR2RGB)

    # Extract detected classes
    detected_classes = set()
    for r in results[0].boxes.cls.cpu().numpy():
        cls_name = results[0].names[int(r)]
        detected_classes.add(cls_name)

    # Build description text
    desc_texts = []
    for cls in detected_classes:
        if cls in wound_descriptions:
            desc_texts.append(f"**{cls}**: {wound_descriptions[cls]}")
        else:
            desc_texts.append(f"**{cls}**: (No description available)")

    return Image.fromarray(annotated_rgb), "\n\n".join(desc_texts)


# ------------------- Gradio Interface -------------------
with gr.Blocks() as demo:
    gr.Markdown("# 🤕 Forensic Wound Detection 🔎")
    gr.Markdown("Upload an image or use your webcam for live wound detection.")

    with gr.Row():
        with gr.Column():
            image_input = gr.Image(type="pil", label="Upload Image", sources=["upload", "webcam"])
            conf_slider = gr.Slider(0, 1, value=0.25, step=0.05, label="Confidence Threshold")
            run_button = gr.Button("Run Detection")
        with gr.Column():
            output_image = gr.Image(type="pil", label="Detection Result")
            output_text = gr.Markdown("")

    run_button.click(
        fn=detect_wounds,
        inputs=[image_input, conf_slider],
        outputs=[output_image, output_text]
    )

    gr.Markdown("---")
    gr.Markdown("Forensic education Version 1.0.0 | © 2025 BH")

# ------------------- Launch -------------------
if __name__ == "__main__":
    demo.launch()
