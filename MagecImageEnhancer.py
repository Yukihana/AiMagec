import cv2
import numpy as np

def preprocess_image():
    # apply correction (automatically determined)
    # apply upscale
    # apply correction with sharpening (if upscale more than 1.5x)
    pass

def enhance_image():
    pass

def resize_with_padding(image, target_width, target_height, padding_color=(0, 0, 0)):

    # Determine scale
    original_height, original_width = image.shape[:2]
    scale_width = target_width / original_width
    scale_height = target_height / original_height 
    scale = min(scale_width, scale_height)

    # Prepare new dimensions
    pad_width = 0
    pad_height = 0
    new_width = target_width
    new_height = target_height
    
    if scale != scale_width:
        new_width = int(original_width * scale)
        pad_width = (target_width - new_width) // 2
        
    if scale != scale_height:
        new_height = int(original_height * scale)
        pad_height = (target_height - new_height) // 2
        
    # Resize and pad the image
    resized_image = cv2.resize(image, (new_width, new_height))
    padded_image = np.full((target_height, target_width, 3), padding_color, dtype=np.uint8)
    padded_image[pad_height:pad_height + new_height, pad_width:pad_width + new_width] = resized_image
    
    return padded_image
