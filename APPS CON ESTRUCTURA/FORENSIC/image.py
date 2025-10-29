import cv2
import numpy as np
import random
import tempfile
from utils import resize_image, text_to_image

def add_and_detect_watermark_image(image, watermark_text, num_watermarks=5):
    watermark_positions = []

    h, w, _ = image.shape
    h_new = (h // 8) * 8
    w_new = (w // 8) * 8
    image_resized = cv2.resize(image, (w_new, h_new))
    
    ycrcb_image = cv2.cvtColor(image_resized, cv2.COLOR_BGR2YCrCb)
    y_channel, cr_channel, cb_channel = cv2.split(ycrcb_image)
    
    dct_y = cv2.dct(np.float32(y_channel))
    
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
    
    idct_y = cv2.idct(dct_y)
    
    ycrcb_image[:, :, 0] = idct_y
    watermarked_image = cv2.cvtColor(ycrcb_image, cv2.COLOR_YCrCb2BGR)
    
    watermark_highlight = watermarked_image.copy()
    for (text_x, text_y, text_w, text_h) in watermark_positions:
        cv2.putText(watermark_highlight, watermark_text, (text_x, text_y), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.rectangle(watermark_highlight, (text_x, text_y - text_h), (text_x + text_w, text_y), (0, 0, 255), 2)

    # Save watermarked image and highlight to temporary files
    _, watermarked_image_path = tempfile.mkstemp(suffix=".png")
    _, watermark_highlight_path = tempfile.mkstemp(suffix=".png")
    cv2.imwrite(watermarked_image_path, watermarked_image)
    cv2.imwrite(watermark_highlight_path, watermark_highlight)
    
    return watermarked_image, watermark_highlight, watermarked_image_path, watermark_highlight_path
