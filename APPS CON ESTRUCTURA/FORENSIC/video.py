import cv2
import numpy as np
import random
import tempfile
import os  # Ensure os is imported
from moviepy.video.io.VideoFileClip import VideoFileClip

def add_and_detect_watermark_video(video_path, watermark_text, num_watermarks=5):
    def add_watermark_to_frame(frame):
        watermark_positions = []

        # Resize frame to be divisible by 8 (required for DCT)
        h, w, _ = frame.shape
        h_new = (h // 8) * 8
        w_new = (w // 8) * 8
        frame_resized = cv2.resize(frame, (w_new, h_new))
        
        # Convert to YCrCb color space and extract Y channel
        ycrcb_image = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2YCrCb)
        y_channel, cr_channel, cb_channel = cv2.split(ycrcb_image)
        
        # Apply DCT to the Y channel
        dct_y = cv2.dct(np.float32(y_channel))
        
        # Add watermark in the DCT domain
        rows, cols = dct_y.shape
        font = cv2.FONT_HERSHEY_SIMPLEX
        for _ in range(num_watermarks):
            text_size = cv2.getTextSize(watermark_text, font, 0.5, 1)[0]
            text_x = random.randint(0, cols - text_size[0])
            text_y = random.randint(text_size[1], rows)
            watermark = np.zeros_like(dct_y)
            watermark = cv2.putText(watermark, watermark_text, (text_x, text_y), font, 0.5, (1, 1, 1), 1, cv2.LINE_AA)
            dct_y += watermark * 0.01
            watermark_positions.append((text_x, text_y, text_size[0], text_size[1]))
        
        # Apply inverse DCT
        idct_y = cv2.idct(dct_y)
        
        # Merge channels and convert back to BGR
        ycrcb_image[:, :, 0] = idct_y
        watermarked_frame = cv2.cvtColor(ycrcb_image, cv2.COLOR_YCrCb2BGR)
        
        # Highlight watermarks for visualization
        watermark_highlight = watermarked_frame.copy()
        for (text_x, text_y, text_w, text_h) in watermark_positions:
            cv2.putText(watermark_highlight, watermark_text, (text_x, text_y), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.rectangle(watermark_highlight, (text_x, text_y - text_h), (text_x + text_w, text_y), (0, 0, 255), 2)
        
        return watermarked_frame, watermark_highlight

    try:
        # Load video using MoviePy
        video = VideoFileClip(video_path)
        
        # Apply watermark to each frame
        video_with_watermark = video.fl_image(lambda frame: add_watermark_to_frame(frame)[0])
        video_with_highlight = video.fl_image(lambda frame: add_watermark_to_frame(frame)[1])

        # Create temporary files for output videos
        temp_fd, watermarked_video_path = tempfile.mkstemp(suffix=".mp4")
        temp_fd_highlight, highlight_video_path = tempfile.mkstemp(suffix=".mp4")
        os.close(temp_fd)
        os.close(temp_fd_highlight)
        
        # Write output videos
        video_with_watermark.write_videofile(watermarked_video_path, codec='libx264')
        video_with_highlight.write_videofile(highlight_video_path, codec='libx264')

        return watermarked_video_path, highlight_video_path

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

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
        os.close(temp_fd)  # Make sure to close the file descriptor
        
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
