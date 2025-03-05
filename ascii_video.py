import os
import time
import subprocess
import numpy as np
from PIL import Image
from rich.console import Console
from rich.text import Text
from shutil import get_terminal_size

# 🎨 ASCII Characters Ordered by Density
ASCII_CHARS = "@%#*+=-:. "[::-1]  # Light to Dark (Reversed for correct mapping)

console = Console()

def image_to_ascii(image_path, width):
    """ Convert image to high-resolution ASCII with colors """
    img = Image.open(image_path).convert("RGB")

    # Dynamically calculate height for correct aspect ratio
    term_width, term_height = get_terminal_size()
    aspect_ratio = 0.45  # Adjust for terminal font
    new_height = int((width / img.width) * img.height * aspect_ratio)

    img = img.resize((width, new_height))
    img_data = np.array(img)

    ascii_image = []
    for row in img_data:
        line = []
        for pixel in row:
            r, g, b = pixel
            brightness = sum(pixel) / 3  # Get average brightness
            char = ASCII_CHARS[int((brightness / 255) * (len(ASCII_CHARS) - 1))]
            line.append(f"[rgb({r},{g},{b})]{char}[/rgb({r},{g},{b})]")  # Colorful ASCII
        ascii_image.append("".join(line))

    return "\n".join(ascii_image)

def play_ascii_video(frame_folder, audio_file, fps=30):
    """ Play high-resolution ASCII animation with synchronized audio """
    frames = sorted([f for f in os.listdir(frame_folder) if f.endswith(".png")])

    term_width, _ = get_terminal_size()
    width = term_width - 5 # Use full width, cap at 120

    # Start playing audio in the background
    audio_process = subprocess.Popen(["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", audio_file])

    for frame in frames:
        ascii_frame = image_to_ascii(os.path.join(frame_folder, frame), width)

        # Print updated ASCII frame (no flickering)
        console.print(Text.from_markup(ascii_frame), end="\r", justify="left")
        time.sleep(1 / fps)

    # Wait for audio to finish playing
    audio_process.wait()

if __name__ == "__main__":
    play_ascii_video("frames", "audio.mp3", fps=30)  # Play with audio sync
