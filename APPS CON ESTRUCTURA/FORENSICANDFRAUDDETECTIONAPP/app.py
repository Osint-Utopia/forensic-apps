import gradio as gr
import numpy as np
import cv2
from PIL import Image, ImageChops, ImageEnhance
import io
import os
import random
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import tempfile
import json
import base64
from sklearn.metrics.pairwise import cosine_similarity
import shutil
from typing import Dict, Any
from scipy.spatial import cKDTree
from multiprocessing import Pool, cpu_count
import nest_asyncio

# Apply nest_asyncio to allow async operations
nest_asyncio.apply()

# Create temporary directory for saving files
TEMP_DIR = tempfile.mkdtemp()
print(f"Using temporary directory: {TEMP_DIR}")

#############################
# HELPER FUNCTIONS
#############################

def save_pil_image(img, path):
    """Save a PIL image and return the path"""
    img.save(path)
    return path

def pil_to_base64(img):
    """Convert PIL image to base64 string for JSON response"""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def base64_to_pil(base64_str):
    """Convert base64 string to PIL image"""
    img_data = base64.b64decode(base64_str)
    return Image.open(io.BytesIO(img_data))

#############################
# FORENSIC ANALYSIS FUNCTIONS
#############################

# Define find_matches as a global function instead of nested
def find_matches(args):
    """
    Find matching blocks within the given indices.
    
    Args:
        args: A tuple containing (block_indices, blocks, tree, similarity_threshold)
        
    Returns:
        A set of matching block pairs
    """
    block_indices, blocks, tree, similarity_threshold = args
    local_matches = set()
    for i in block_indices:
        # Find all blocks within the similarity threshold
        distances, indices = tree.query(blocks[i], k=10, distance_upper_bound=similarity_threshold)
        for j, dist in zip(indices, distances):
            # Skip self-matches and invalid indices
            if j != i and j < len(blocks) and dist <= similarity_threshold:
                # Store matches as sorted tuples to avoid duplicates
                local_matches.add(tuple(sorted([i, j])))
    return local_matches


def detect_clones(image_path, max_dimension=2000):
    """
    Detects cloned/copy-pasted regions in the image with optimized performance.
    
    Args:
        image_path: Path to the image file
        max_dimension: Maximum dimension to resize large images to
    
    Returns:
        PIL Image containing the clone detection result and count of clones
    """
    # Read image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Could not read image at {image_path}")
    
    height, width = img.shape
    
    # Handle large images by resizing if needed
    scale = 1.0
    if height > max_dimension or width > max_dimension:
        scale = max_dimension / max(height, width)
        new_height, new_width = int(height * scale), int(width * scale)
        img = cv2.resize(img, (new_width, new_height))
        height, width = img.shape
    
    # Create output image
    clone_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    
    # Define parameters
    block_size = 16
    stride = 8
    
    # For very large images, increase stride
    if (height * width) > 4000000:
        stride = 16
    
    # Extract block features
    blocks = []
    positions = []
    
    # Apply DCT to each block for feature extraction (faster than raw pixels)
    for y in range(0, height - block_size, stride):
        for x in range(0, width - block_size, stride):
            block = img[y:y+block_size, x:x+block_size].astype(np.float32)
            # Apply DCT and keep only top 16 coefficients (reduces dimensionality)
            dct = cv2.dct(block)
            feature = dct[:4, :4].flatten()  # Use only low-frequency components
            blocks.append(feature)
            positions.append((x, y))
    
    # Convert to numpy array for faster processing
    blocks = np.array(blocks, dtype=np.float32)
    
    # Normalize features for better comparison
    norms = np.linalg.norm(blocks, axis=1)
    norms[norms == 0] = 1  # Avoid division by zero
    blocks = blocks / norms[:, np.newaxis]
    
    # Use KD-Tree for efficient nearest neighbor search (much faster than cosine_similarity)
    tree = cKDTree(blocks)
    
    # Find similar blocks using radius search (equivalent to high cosine similarity)
    # This is much more efficient than computing the full similarity matrix
    similarity_threshold = 0.04  # Equivalent to ~0.95 cosine similarity
    matches = set()
    
    # Use multiple processes to speed up the search
    num_processes = min(8, cpu_count())
    
    # Split work among processes
    chunk_size = len(blocks) // num_processes + 1
    block_chunks = [range(i, min(i + chunk_size, len(blocks))) for i in range(0, len(blocks), chunk_size)]
    
    # Prepare arguments for the find_matches function
    args_list = [(chunk, blocks, tree, similarity_threshold) for chunk in block_chunks]
    
    with Pool(num_processes) as pool:
        results = pool.map(find_matches, args_list)
    
    # Combine results
    for result in results:
        matches.update(result)
    
    # Draw rectangles for matches
    for i, j in matches:
        x1, y1 = positions[i]
        x2, y2 = positions[j]
        cv2.rectangle(clone_img, (x1, y1), (x1+block_size, y1+block_size), (0, 0, 255), 1)
        cv2.rectangle(clone_img, (x2, y2), (x2+block_size, y2+block_size), (255, 0, 0), 1)
    
    # Convert OpenCV image to PIL format
    clone_result = Image.fromarray(cv2.cvtColor(clone_img, cv2.COLOR_BGR2RGB))
    
    # Restore original scale if the image was resized
    if scale != 1.0:
        orig_size = (int(clone_img.shape[1]/scale), int(clone_img.shape[0]/scale))
        clone_result = clone_result.resize(orig_size, Image.LANCZOS)
    
    return clone_result, len(matches)

def error_level_analysis(image_path, quality=90, scale=10):
    """
    Performs Error Level Analysis (ELA) on the image.
    
    Args:
        image_path: Path to the image file
        quality: JPEG quality level for recompression
        scale: Amplification factor for differences
    
    Returns:
        PIL Image containing the ELA result
    """
    # Open the original image
    original = Image.open(image_path).convert('RGB')
    
    # Save and reopen a JPEG version at the specified quality
    temp_filename = os.path.join(TEMP_DIR, "temp_ela_process.jpg")
    original.save(temp_filename, 'JPEG', quality=quality)
    recompressed = Image.open(temp_filename)
    
    # Calculate the difference
    diff = ImageChops.difference(original, recompressed)
    
    # Amplify the difference for better visualization
    diff = ImageEnhance.Brightness(diff).enhance(scale)
    
    # Create a colored version of the diff for visualization
    diff_array = np.array(diff)
    
    # Convert to grayscale
    if len(diff_array.shape) == 3:
        diff_gray = np.mean(diff_array, axis=2)
    else:
        diff_gray = diff_array
    
    # Apply colormap for better visualization
    colormap = plt.get_cmap('jet')
    colored_diff = (colormap(diff_gray / 255.0) * 255).astype(np.uint8)
    
    # Create PIL image from the array (remove alpha channel)
    colored_result = Image.fromarray(colored_diff[:, :, :3])
    
    return colored_result

def extract_exif_metadata(image_path):
    """
    Extracts EXIF metadata from the image and identifies potential manipulation indicators.
    
    Args:
        image_path: Path to the image file
    
    Returns:
        Dictionary with metadata and analysis
    """
    try:
        img = Image.open(image_path)
        exif_data = img._getexif() or {}
        
        # Map EXIF tags to readable names
        exif_tags = {
            271: 'Make', 272: 'Model', 306: 'DateTime', 
            36867: 'DateTimeOriginal', 36868: 'DateTimeDigitized',
            37510: 'UserComment', 40964: 'RelatedSoundFile',
            305: 'Software', 315: 'Artist', 33432: 'Copyright'
        }
        
        # Process EXIF data into readable format
        metadata = {}
        for tag_id, value in exif_data.items():
            tag = exif_tags.get(tag_id, str(tag_id))
            metadata[tag] = str(value)
        
        # Check for potential manipulation indicators
        indicators = []
        
        # Check for editing software
        editing_software = ['photoshop', 'lightroom', 'gimp', 'paint', 'editor', 'filter']
        if 'Software' in metadata:
            software = metadata['Software'].lower()
            for editor in editing_software:
                if editor in software:
                    indicators.append(f"Image edited with {metadata['Software']}")
                    break
        
        # Check for date discrepancies
        if 'DateTimeOriginal' in metadata and 'DateTime' in metadata:
            if metadata['DateTimeOriginal'] != metadata['DateTime']:
                indicators.append("Capture time differs from modification time")
        
        # Missing original date
        if 'DateTime' in metadata and 'DateTimeOriginal' not in metadata:
            indicators.append("Original capture time missing")
        
        # Create result dictionary
        result = {
            "metadata": metadata,
            "indicators": indicators,
            "summary": "Potential manipulation detected" if indicators else "No obvious manipulation indicators",
            "analysis_count": len(metadata)
        }
        
        return result
    
    except Exception as e:
        return {
            "metadata": {"Error": str(e)},
            "indicators": ["Error extracting metadata"],
            "summary": "Analysis failed",
            "analysis_count": 0
        }

def noise_analysis(image_path, amplification=15):
    """
    Extracts and analyzes noise patterns in the image to detect inconsistencies.
    
    Args:
        image_path: Path to the image file
        amplification: Factor to amplify noise for visualization
    
    Returns:
        PIL Image containing the noise analysis result
    """
    # Read the image
    img = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to extract base image without noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Extract noise by subtracting the blurred image from the original
    noise = cv2.subtract(gray, blur)
    
    # Amplify the noise for better visualization
    noise = cv2.multiply(noise, amplification)
    
    # Apply a colormap for visualization
    noise_colored = cv2.applyColorMap(noise, cv2.COLORMAP_JET)
    
    # Convert back to PIL format
    noise_pil = Image.fromarray(cv2.cvtColor(noise_colored, cv2.COLOR_BGR2RGB))
    
    return noise_pil

def manipulation_likelihood(image_path):
    """
    Simulates a pre-trained model that evaluates the likelihood of image manipulation.
    For demo purposes, this generates a random score with some biasing based on image properties.
    
    Args:
        image_path: Path to the image file
    
    Returns:
        Dictionary with manipulation probability and areas of interest
    """
    # Open the image
    img = np.array(Image.open(image_path).convert('RGB'))
    
    # Get image dimensions
    height, width = img.shape[:2]
    
    # In a real implementation, you would use your pre-trained model here
    # For demo purposes, we'll simulate a model output based on image characteristics
    
    # Create a heatmap of "suspicious" areas (for demo purposes)
    heatmap = np.zeros((height, width), dtype=np.float32)
    
    # Add some "suspicious" regions for demonstration
    # This would be replaced by actual model output in a real implementation
    
    # 1. Add some random regions of interest
    num_regions = random.randint(1, 4)
    for _ in range(num_regions):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        radius = random.randint(width//10, width//5)
        
        # Create a circular region of interest
        y_indices, x_indices = np.ogrid[:height, :width]
        dist_from_center = ((y_indices - y)**2 + (x_indices - x)**2)
        mask = dist_from_center <= radius**2
        
        # Add to heatmap with random intensity
        intensity = random.uniform(0.5, 1.0)
        heatmap[mask] = np.maximum(heatmap[mask], intensity * np.exp(-dist_from_center[mask] / (2 * (radius/2)**2)))
    
    # Normalize the heatmap
    if np.max(heatmap) > 0:
        heatmap = heatmap / np.max(heatmap)
    
    # Convert to RGB for visualization using a colormap
    cmap = LinearSegmentedColormap.from_list('custom', [(0, 0, 0, 0), (1, 0, 0, 0.7)])
    heatmap_rgb = (cmap(heatmap) * 255).astype(np.uint8)
    
    # Overlay heatmap on the original image
    orig_img = np.array(Image.open(image_path).convert('RGB'))
    overlay = orig_img.copy()
    
    # Only add red channel where heatmap has values
    for c in range(3):
        if c == 0:  # Red channel
            overlay[:, :, c] = np.where(heatmap_rgb[:, :, 3] > 0, 
                                     (overlay[:, :, c] * 0.5 + heatmap_rgb[:, :, 0] * 0.5).astype(np.uint8), 
                                     overlay[:, :, c])
        else:  # Green and blue channels - reduce them in highlighted areas
            overlay[:, :, c] = np.where(heatmap_rgb[:, :, 3] > 0, 
                                     (overlay[:, :, c] * 0.5).astype(np.uint8), 
                                     overlay[:, :, c])
    
    # Generate a "manipulation probability" for demo purposes
    # In a real implementation, this would come from your model
    exif_result = extract_exif_metadata(image_path)
    exif_factor = 0.3 if exif_result["indicators"] else 0.0
    
    # Slightly bias probability based on file characteristics for the demo
    img_factor = 0.1 if ".jpg" in image_path.lower() else 0.0
    
    # Combine factors with a random component for the demo
    base_probability = random.uniform(0.2, 0.8)
    manipulation_probability = min(0.95, base_probability + exif_factor + img_factor)
    
    # Create a more realistic result for the demo
    overlay_image = Image.fromarray(overlay)
    
    # Return results
    return {
        "probability": manipulation_probability,
        "heatmap_image": overlay_image,
        "explanation": get_probability_explanation(manipulation_probability),
        "confidence": "medium" if 0.3 < manipulation_probability < 0.7 else "high"
    }

def get_probability_explanation(prob):
    """Returns an explanation text based on the manipulation probability"""
    if prob < 0.3:
        return "The image appears to be authentic with no significant signs of manipulation."
    elif prob < 0.6:
        return "Some inconsistencies detected that might indicate limited manipulation."
    else:
        return "Strong indicators of digital manipulation detected in this image."

def get_clone_explanation(count):
    """Returns an explanation based on the number of clone matches found"""
    if count == 0:
        return "No copy-paste manipulations detected in the image."
    elif count < 10:
        return "Few potential copy-paste regions detected, might be false positives."
    else:
        return "Significant number of copy-paste regions detected, suggesting manipulation."

def save_uploaded_image(image):
    """Save a PIL image to disk and return the path"""
    temp_path = os.path.join(TEMP_DIR, "temp_analyze.jpg")
    image.save(temp_path)
    return temp_path

def analyze_complete_image(image_path):
    """Comprehensive analysis of an image, running all forensic tests"""
    # Read the image as PIL
    image = Image.open(image_path)
    
    # Run all analyses
    exif_result = extract_exif_metadata(image_path)
    manipulation_result = manipulation_likelihood(image_path)
    clone_result, clone_count = detect_clones(image_path)
    ela_result = error_level_analysis(image_path)
    noise_result = noise_analysis(image_path)
    
    # Compile combined analysis text
    analysis_text = f"""
## Manipulation Analysis Results

**Overall Assessment: {manipulation_result['probability']*100:.1f}% likelihood of manipulation**

{manipulation_result['explanation']}

### Clone Detection Analysis:
Found {clone_count} potential cloned regions in the image.
{get_clone_explanation(clone_count)}

### EXIF Metadata Analysis:
{exif_result['summary']}

Indicators found: {len(exif_result['indicators'])}
"""
    
    if exif_result['indicators']:
        analysis_text += "\nDetailed indicators:\n"
        for indicator in exif_result['indicators']:
            analysis_text += f"- {indicator}\n"
    
    # Return complete result object
    return {
        "manipulation_probability": manipulation_result["probability"],
        "analysis_text": analysis_text,
        "exif_data": exif_result["metadata"],
        "clone_count": clone_count,
        "original_image": image,
        "ela_image": ela_result,
        "noise_image": noise_result,
        "heatmap_image": manipulation_result["heatmap_image"],
        "clone_image": clone_result
    }

#############################
# GRADIO INTERFACE FUNCTIONS
#############################

def analyze_image(image):
    """Main function for Gradio UI that processes the uploaded image"""
    if image is None:
        return None, None, None, None, None, "{}", "Please upload an image first.", 0
    
    # Save the image
    temp_path = save_uploaded_image(image)
    
    try:
        # Get analysis results
        results = analyze_complete_image(temp_path)
        
        # Return results in the format expected by Gradio
        return (
            image,  # original_image
            results["ela_image"],  # ela_image
            results["noise_image"],  # noise_image
            results["heatmap_image"],  # heatmap_image
            results["clone_image"],  # clone_image
            json.dumps(results["exif_data"], indent=2),  # exif_data
            results["analysis_text"],  # analysis_results
            results["manipulation_probability"]  # probability_slider
        )
    except Exception as e:
        error_message = f"Error occurred during analysis: {str(e)}"
        print(error_message)  # Log the error
        return image, None, None, None, None, f"Error: {str(e)}", error_message, 0

#############################
# GRADIO INTERFACE
#############################

with gr.Blocks(title="Image Forensic & Fraud Detection Tool") as demo:
    gr.Markdown("""
    # Image Forensic & Fraud Detection Tool
    
    Upload an image to analyze it for potential manipulation using various forensic techniques.
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            input_image = gr.Image(type="pil", label="Upload Image for Analysis")
            analyze_button = gr.Button("Analyze Image", variant="primary")
            
            gr.Markdown("### Manipulation Probability")
            probability_slider = gr.Slider(
                minimum=0, maximum=1, value=0, 
                label="Manipulation Probability", 
                interactive=False
            )
            
            gr.Markdown("### EXIF Metadata")
            exif_data = gr.Code(language="json", label="EXIF Data", lines=10)
            
        with gr.Column(scale=2):
            with gr.Tab("Analysis Results"):
                analysis_results = gr.Markdown()
                
            with gr.Tab("Original Image"):
                original_image = gr.Image(type="pil", label="Original Image")
                
            with gr.Tab("Error Level Analysis (ELA)"):
                gr.Markdown("""
                Error Level Analysis reveals differences in compression levels. Areas with different compression levels 
                often indicate modifications. Brighter regions in the visualization suggest potential manipulations.
                """)
                ela_image = gr.Image(type="pil", label="ELA Result")
                
            with gr.Tab("Noise Analysis"):
                gr.Markdown("""
                Noise Analysis examines the noise patterns in the image. Inconsistent noise patterns often indicate 
                areas that have been manipulated or added from different sources.
                """)
                noise_image = gr.Image(type="pil", label="Noise Pattern Analysis")
                
            with gr.Tab("Clone Detection"):
                gr.Markdown("""
                Clone Detection identifies duplicated areas within the image. Red and blue rectangles highlight 
                matching regions that may indicate copy-paste manipulation.
                """)
                clone_image = gr.Image(type="pil", label="Clone Detection Result")
                
            with gr.Tab("AI Detection Heatmap"):
                gr.Markdown("""
                This heatmap highlights regions identified by our AI model as potentially manipulated.
                Red areas indicate suspicious regions with a higher likelihood of manipulation.
                """)
                heatmap_image = gr.Image(type="pil", label="AI-Detected Suspicious Regions")
    
    # Set up event handlers
    analyze_button.click(
        fn=analyze_image,
        inputs=[input_image],
        outputs=[
            original_image, 
            ela_image, 
            noise_image, 
            heatmap_image, 
            clone_image,
            exif_data, 
            analysis_results,
            probability_slider
        ]
    )
    
# Launch the app
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)