import json
import numpy as np
from PIL import Image, ImageDraw
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip

# --- Step 1: Load configuration ---
with open("config.json", "r") as f:
    config = json.load(f)

presentation_path = config["presentation_video"]
avatar_path = config["avatar_video"]
output_path = config["output_video"]
avatar_size = tuple(config["avatar_size"])
start_time = config["start_time"]
switch_time = config["switch_time"]
use_circular_mask = config.get("use_circular_mask", True)

# --- Step 2: Load video clips ---
presentation = VideoFileClip(presentation_path)
avatar = VideoFileClip(avatar_path).resize(avatar_size)

# --- Step 3: Create circular mask if needed ---
def create_circle_mask(size):
    mask_img = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask_img)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)
    return np.array(mask_img) / 255.0

if use_circular_mask:
    circle_mask = create_circle_mask(avatar_size)
    mask_clip = ImageClip(circle_mask, ismask=True).set_duration(avatar.duration)
    avatar = avatar.set_mask(mask_clip)

# --- Step 4: Calculate positions ---
video_w, video_h = presentation.size
left_pos = (0, video_h - avatar_size[1])
right_pos = (video_w - avatar_size[0], video_h - avatar_size[1])

# --- Step 5: Define animation logic ---
def position_func(t):
    if t < start_time:
        return (-500, -500)  # hide before appearing
    elif start_time <= t < switch_time:
        return left_pos
    else:
        return right_pos

avatar = avatar.set_position(position_func)

# --- Step 6: Trim durations to match ---
min_duration = min(presentation.duration, avatar.duration)
presentation = presentation.subclip(0, min_duration)
avatar = avatar.subclip(0, min_duration)

# --- Step 7: Compose and export final video ---
final = CompositeVideoClip([presentation, avatar])
final.write_videofile(output_path, codec="libx264", audio_codec="aac")
