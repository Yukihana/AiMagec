import os
import cv2
import uuid
from dataclasses import dataclass

# Frame

def extract_frame(video_path, frame_number):
    
    # Open file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Error opening video file")

    # Read frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    success, frame = cap.read()
    if not success:
        raise ValueError("Error reading the frame")

    # Release
    cap.release()
    return frame

def display_frame(frame, debug_messages):
    if debug_messages:
        print("Showing frame window")

    try:
        window_name = f'Frame_{uuid.uuid4()}'
        cv2.imshow(window_name, frame)
        cv2.waitKey(0)
        cv2.destroyWindow(window_name)
    except:
        pass

    if debug_messages:
        print("Frame window destroyed.")

# Get files

def list_asset_files(directory):
    mp4_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.mp4'):
                mp4_files.append(os.path.join(root, file))
    return mp4_files

# Get metadata

@dataclass
class VideoInfo:
    path: str
    frame_count: int
    width: int
    height: int
    container: str = None
    video_codec: str = None
    audio_codec: str = None

def get_video_info(video_path):
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Error opening video file")

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    cap.release()
    result = VideoInfo(
        path = video_path,
        frame_count = frame_count,
        height = height,
        width = width
    )
    
    return result

# Info collection and mapping

def collect_video_infos(file_list):
    info_collection = []
    for file in file_list:
        video_info = get_video_info(file)
        info_collection.append(video_info)
    return info_collection

def determine_sampling_resolution(video_infos):
    width_max = 0
    height_max = 0
    for video_info in video_infos:
        if video_info.width > width_max:
            width_max = video_info.width
        if video_info.height > height_max:
            height_max = video_info.height
    return width_max, height_max
    
def create_range_map(info_collection):
    end_frame_map = {}
    total_frames = 0
    for video_info in info_collection:
        end_frame_map[total_frames] = video_info
        total_frames += video_info.frame_count
    return end_frame_map

def translate_index(range_map, index):
    sorted_keys = sorted(range_map.keys())

    # traverse and take the last key before key value exceeds index
    last_start = 0
    for start_frame in sorted_keys:
        if index < start_frame:
            break
        last_start = start_frame

    # select item and calculate frame offset
    offset = index - last_start
    path = range_map[last_start].path
    frame_count = range_map[last_start].frame_count
    if offset > frame_count:
        raise ValueError("Index out of range")
    return path, offset

# Display

def pp_range_map(range_map):
    # ANSI escape codes for colors
    COLORS = {
        'cobalt': '\033[38;5;38m',    # Cobalt blue
        'hotpink': '\033[38;5;213m',  # Hot pink
        'grey': '\033[38;5;240m',     # Grey
        'reset': '\033[0m'            # Reset to default
    }
    
    # Function to apply color formatting
    def colorize(text, color):
        return f"{COLORS[color]}{text}{COLORS['reset']}"
    
    for start_frame, video_info in range_map.items():
        res_str = f"{video_info.width}x{video_info.height}"
        formatted_output = (
            f"{colorize(str(start_frame), 'cobalt')} : "
            f"{colorize(str(video_info.frame_count), 'hotpink')} * "
            f"{colorize(str(res_str), 'hotpink')} - "
            f"{colorize(video_info.path, 'grey')}"
        )
        print(formatted_output)