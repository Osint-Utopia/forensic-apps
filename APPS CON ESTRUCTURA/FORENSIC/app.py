import gradio as gr
from image import add_and_detect_watermark_image
from video import add_and_detect_watermark_video
from detect import detect_watermark_image, detect_watermark_video

# Image Interface
image_inputs = [
    gr.Image(type="numpy", label="Upload Image"),
    gr.Textbox(label="Watermark Text")
]

image_outputs = [
    gr.Image(type="numpy", label="Watermarked Image"),
    gr.Image(type="numpy", label="Watermark Highlight"),
    gr.File(label="Download Watermarked Image"),
    gr.File(label="Download Watermark Highlight")
]

def process_image(image, text):
    watermarked_image, highlight, watermarked_image_path, highlight_path = add_and_detect_watermark_image(image, text)
    return watermarked_image, highlight, watermarked_image_path, highlight_path

image_interface = gr.Interface(
    fn=process_image,
    inputs=image_inputs,
    outputs=image_outputs,
    title="Image Watermark Application",
    description="Upload an image and add a watermark text. Detect watermark and highlight its position."
)

# Video Interface
video_inputs = [
    gr.Video(label="Upload Video"),
    gr.Textbox(label="Watermark Text")
]

video_outputs = [
    gr.Video(label="Watermarked Video"),
    gr.Video(label="Watermark Highlight"),
    gr.File(label="Download Watermarked Video"),
    gr.File(label="Download Watermark Highlight")
]

def process_video(video, text):
    watermarked_video_path, highlight_video_path, _, _ = add_and_detect_watermark_video(video, text)
    return watermarked_video_path, highlight_video_path, watermarked_video_path, highlight_video_path

video_interface = gr.Interface(
    fn=process_video,
    inputs=video_inputs,
    outputs=video_outputs,
    title="Video Watermark Application",
    description="Upload a video and add a watermark text. Detect watermark and highlight its position."
)

# Forensic Watermark Detection Interface
detect_inputs = [
    gr.Image(type="numpy", label="Upload Image")
]

detect_outputs = [
    gr.Image(type="numpy", label="Watermark Detection Result")
]

detect_interface = gr.Interface(
    fn=detect_watermark_image,
    inputs=detect_inputs,
    outputs=detect_outputs,
    title="Forensic Watermark Detection",
    description="Upload an image to detect forensic watermarks."
)

# Video Detection Interface
video_detect_inputs = [
    gr.Video(label="Upload Video")
]

video_detect_outputs = [
    gr.Video(label="Watermark Detection Result")
]

def detect_video(video):
    detected_video_path = detect_watermark_video(video)
    return detected_video_path

video_detect_interface = gr.Interface(
    fn=detect_video,
    inputs=video_detect_inputs,
    outputs=video_detect_outputs,
    title="Video Watermark Detection",
    description="Upload a video to detect forensic watermarks."
)

# Combine interfaces in tabs
app = gr.TabbedInterface(
    interface_list=[image_interface, video_interface, detect_interface, video_detect_interface],
    tab_names=["Image", "Video", "Detect", "Video Detect"]
)

if __name__ == "__main__":
    app.launch(
        share=True
    )
