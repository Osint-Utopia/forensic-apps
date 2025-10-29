import json
import gradio as gr
import torch
import PIL
import os
from models import ViTClassifier
from datasets import load_dataset
from transformers import TrainingArguments, ViTConfig, ViTForImageClassification
from torchvision import transforms
import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def load_config(config_path):
    with open(config_path, 'r') as f:
        config = json.load(f)
    print("Config Loaded:", config)  # Debugging
    return config

def load_model(config, device='cuda'):
    device = torch.device(device if torch.cuda.is_available() else 'cpu')
    ckpt = torch.load(config['checkpoint_path'], map_location=device)
    print("Checkpoint Loaded:", ckpt.keys())  # Debugging
    model = ViTClassifier(config, device=device, dtype=torch.float32)
    print("Model Loaded:", model)  # Debugging
    model.load_state_dict(ckpt['model'])
    return model.to(device).eval()

def prepare_model_for_push(model, config):
    # Create a VisionTransformerConfig
    vit_config = ViTConfig(
        image_size=config['model']['input_size'],
        patch_size=config['model']['patch_size'],
        hidden_size=config['model']['hidden_size'],
        num_heads=config['model']['num_attention_heads'],
        num_layers=config['model']['num_hidden_layers'],
        mlp_ratio=4,  # Common default for ViT
        hidden_dropout_prob=config['model']['hidden_dropout_prob'],
        attention_probs_dropout_prob=config['model']['attention_probs_dropout_prob'],
        layer_norm_eps=config['model']['layer_norm_eps'],
        num_classes=config['model']['num_classes']
    )
    # Create a VisionTransformer model
    vit_model = ViTForImageClassification(vit_config)
    # Copy the weights from your custom model to the VisionTransformer model
    state_dict = vit_model.state_dict()
    for key in state_dict.keys():
        if key in model.state_dict():
            state_dict[key] = model.state_dict()[key]
    vit_model.load_state_dict(state_dict)
    return vit_model, vit_config

def run_inference(input_image, model):
    print("Input Image Type:", type(input_image))  # Debugging
    # Directly use the PIL Image object
    fake_prob = model.forward(input_image).item()
    result_description = get_result_description(fake_prob)
    return {
        "Fake Probability": fake_prob,
        "Result Description": result_description
    }

def get_result_description(fake_prob):
    if fake_prob > 0.5:
        return "The image is likely a fake."
    else:
        return "The image is likely real."

def run_evaluation(dataset_name, model, config, device):
    dataset = load_dataset(dataset_name)
    eval_df, accuracy = evaluate_model(model, dataset, config, device)
    return accuracy, eval_df.to_csv(index=False)

def evaluate_model(model, dataset, config, device):
    device = torch.device(device if torch.cuda.is_available() else 'cpu')
    model.to(device).eval()
    norm_mean = config['preprocessing']['norm_mean']
    norm_std = config['preprocessing']['norm_std']
    resize_size = config['preprocessing']['resize_size']
    crop_size = config['preprocessing']['crop_size']
    augment_list = [
        transforms.Resize(resize_size),
        transforms.CenterCrop(crop_size),
        transforms.ToTensor(),
        transforms.Normalize(mean=norm_mean, std=norm_std),
        transforms.ConvertImageDtype(torch.float32),
    ]
    preprocess = transforms.Compose(augment_list)
    true_labels = []
    predicted_probs = []
    predicted_labels = []
    with torch.no_grad():
        for sample in dataset:
            image = sample['image']
            label = sample['label']
            image = preprocess(image).unsqueeze(0).to(device)
            output = model.forward(image)
            prob = output.item()
            true_labels.append(label)
            predicted_probs.append(prob)
            predicted_labels.append(1 if prob > 0.5 else 0)
    eval_df = pd.DataFrame({
        'True Label': true_labels,
        'Predicted Probability': predicted_probs,
        'Predicted Label': predicted_labels
    })
    accuracy = (eval_df['True Label'] == eval_df['Predicted Label']).mean()
    return eval_df, accuracy

def main():
    # Load configuration
    config_path = "config.json"
    config = load_config(config_path)
    # Load model
    device = config['device']
    model = load_model(config, device=device)
    # Define Gradio interface for inference
    def simple_predict(input_image):
        """Quick and simple check.

        Args:
            input_image: Image to analyze
        Returns:
            result: String
        """
        return run_inference(input_image, model)
    # Create Gradio Tabs
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column():
                input_image = gr.Image(type="pil", label="Upload Image")
            with gr.Column():
                output = gr.JSON(label="Classification Result")
        input_image.change(fn=simple_predict, inputs=input_image, outputs=output)
    # Launch the Gradio app
    demo.launch(show_error=True)

if __name__ == "__main__":
    main()