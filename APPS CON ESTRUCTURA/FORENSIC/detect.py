import cv2
import numpy as np

import random
import os
import tempfile
from moviepy.video.io.VideoFileClip import VideoFileClip

def detect_watermark_image(image):
    ycrcb_image = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    y_channel, _, _ = cv2.split(ycrcb_image)
    dct_y = cv2.dct(np.float32(y_channel))
    
    # Detecting the watermark
    watermark = np.zeros_like(dct_y)
    rows, cols = dct_y.shape
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = "WATERMARK"
    text_size = cv2.getTextSize(text, font, 0.5, 1)[0]
    text_x = np.random.randint(0, cols - text_size[0])
    text_y = np.random.randint(text_size[1], rows)
    watermark = cv2.putText(watermark, text, (text_x, text_y), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
    
    detected_image = cv2.idct(dct_y + watermark)
    detected_image = np.uint8(np.clip(detected_image, 0, 255))
    
    return detected_image

def detect_watermark_video(video_path, watermark_text="WATERMARK"):
    """Detect watermarks in a video file using OpenCV.
    
    Args:
        video_path (str): Path to the video file
        watermark_text (str): The watermark text to detect
        
    Returns:
        str: Path to the output video with detected watermarks
    """
    try:
        # Use OpenCV directly for frame processing
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video file {video_path}")
            return None
            
        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        # Create output video file
        temp_fd, output_path = tempfile.mkstemp(suffix=".mp4")
        os.close(temp_fd)
        
        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MP4 codec
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        # Track detection results
        frame_count = 0
        detected_frames = 0
        
        # Process each frame
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Apply watermark detection to the frame
            frame_count += 1
            
            # Detect watermark in current frame
            ycrcb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
            y_channel, _, _ = cv2.split(ycrcb_image)
            
            # Check if frame dimensions are suitable for DCT
            h, w = y_channel.shape[:2]
            if h % 8 != 0 or w % 8 != 0:
                y_channel = cv2.resize(y_channel, ((w//8)*8, (h//8)*8))
            
            dct_y = cv2.dct(np.float32(y_channel))
            
            # Simple detection logic: look for anomalies in DCT coefficients
            mid_freq_sum = np.sum(np.abs(dct_y[2:6, 2:6]))
            detected = mid_freq_sum > 1000  # Threshold for detection
            
            if detected:
                detected_frames += 1
                # Add visual indicator of detection
                frame = cv2.putText(frame, "WATERMARK DETECTED", (30, 30), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
            out.write(frame)
            
        # Release resources
        cap.release()
        out.release()
        
        print(f"Processed {frame_count} frames, detected watermarks in {detected_frames} frames")
        
        return output_path
            
    except Exception as e:
        print(f"Error detecting watermark in video: {e}")
        return None
