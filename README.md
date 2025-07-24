# 🎥 Avatar Overlay on Presentation Video (Python)

This project overlays a circular avatar video on top of a presentation video using MoviePy in Python. The avatar appears in the **bottom-left corner from 1s to 80s**, and then **jumps to the bottom-right corner until the end**. The avatar is masked into a **circular shape** using `PIL`.

---

## ✅ Features

- 📁 Simple file structure (no nested input/output folders)
- 🎯 Circular avatar using `PIL` mask
- ⏱️ Time-based animation for avatar position
- 🧠 Automatically handles durations of both clips
- 🎬 Clean and export-ready result using `MoviePy`

---

## 🧾 Requirements

Install dependencies:

```bash
pip install moviepy pillow numpy
```

---

## 📂 Files Required

Place these files in the same directory as the script:

- `presentation.mp4` – Your main screen recording or presentation video
- `avatar.mp4` – The avatar/lip-synced video (with transparent or green screen background)

---

## 🚀 How to Run

Save the following Python script as `prepare_files.py`:

```python
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip
import numpy as np
from PIL import Image, ImageDraw

# Load base video and avatar
presentation = VideoFileClip("presentation.mp4")
avatar = VideoFileClip("avatar.mp4").resize((250, 250))  # ← updated size

# Make circular mask
def create_circle_mask(size=(250, 250)):
    mask_img = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask_img)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)
    return np.array(mask_img) / 255.0

circle_mask = create_circle_mask()
mask_clip = ImageClip(circle_mask, ismask=True).set_duration(avatar.duration)
avatar = avatar.set_mask(mask_clip)

# Video size
video_w, video_h = presentation.size
left_pos = (0, video_h - 250)
right_pos = (video_w - 250, video_h - 250)

# Animate position: left from 1s to 80s, then jump to right
def position_func(t):
    if t < 1:
        return (-500, -500)  # hide before 1s
    elif 1 <= t < 80:
        return left_pos
    else:
        return right_pos

avatar = avatar.set_position(position_func)

# Ensure avatar and presentation match durations
min_duration = min(presentation.duration, avatar.duration)
avatar = avatar.subclip(0, min_duration)
presentation = presentation.subclip(0, min_duration)

# Compose final
final = CompositeVideoClip([presentation, avatar])

# Export
final.write_videofile("final_output.mp4", codec="libx264", audio_codec="aac")
```

---

## 📦 Output

- ✅ `final_output.mp4` – Video with avatar overlay (circular, animated left-to-right)

---

## 📸 Example

| Time     | Avatar Position |
|----------|------------------|
| 0–1s     | Hidden           |
| 1–80s    | Bottom Left      |
| 80s–end  | Bottom Right     |

---

## 🛠️ Customization

- Change `resize((250, 250))` to resize the avatar.
- Adjust timings in `position_func(t)` as per your need.

---

## 💡 Tip

To avoid errors related to mismatched shapes (e.g., (250,250,3) vs (250,250,4)), ensure your `avatar.mp4` doesn't have an alpha channel, or let MoviePy handle masking using `set_mask()` as done above.

---

## 📃 License

This project is open-source under the MIT License.
