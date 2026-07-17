import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont
from scipy.signal import stft, istft

# =========================================================================
# CONFIG
# =========================================================================
FLAG = "flag:PUT_YOUR_FLAG_HERE"
INPUT_AUDIO = "original.wav"
OUTPUT_AUDIO = "my_favorite_song.wav"
SAMPLE_RATE = 48000  

HIDDEN_STRENGTH = 0.35 

# =========================================================================
# 1. FIXED: DYNAMIC TEXT IMAGE GENERATOR (Prevents Canvas Edge Clipping)
# =========================================================================
def create_flag_image(text, height=300):
    try:
        font = ImageFont.truetype("couri.ttf", 60) 
    except IOError:
        print("[!] Courier font not found, falling back to default system font.")
        font = ImageFont.load_default()

    letter_spacing = 15
    
    # First pass: Calculate exactly how wide the image needs to be so nothing is cut off
    total_width = 40  # Start with padding for left and right margins
    for char in text:
        bbox = font.getbbox(char) if hasattr(font, 'getbbox') else (0, 0, 35, 60) # Fallback handling
        char_w = bbox[2] - bbox[0]
        total_width += char_w + letter_spacing

    # Create the canvas using the dynamically calculated total width
    img = Image.new("L", (total_width, height), color=0)
    draw = ImageDraw.Draw(img)
    
    current_x = 20
    for char in text:
        bbox = draw.textbbox((0, 0), char, font=font)
        char_w = bbox[2] - bbox[0]
        char_h = bbox[3] - bbox[1]
        
        y = (height - char_h) // 2
        draw.text((current_x, y), char, fill=255, font=font)
        current_x += char_w + letter_spacing

    return np.array(img) / 255.0

# =========================================================================
# 2. EMBED SIGNAL WITH DYNAMIC LENGTH CHECKS
# =========================================================================
def embed_image_to_audio(input_audio_path, flag_matrix, output_audio_path="my_favorite_song.wav", sample_rate=48000, strength=0.35):
    print("[+] Loading cover audio...")
    try:
        audio, sr = sf.read(input_audio_path)
        if sr != sample_rate:
            sr = sample_rate
    except FileNotFoundError:
        print("[!] Input audio file not found. Creating silent canvas.")
        audio = np.zeros(sample_rate * 8)  # Defaulting to a safe 8 seconds
        sr = sample_rate

    if len(audio.shape) > 1:
        audio = audio.mean(axis=1)

    f, t, Zxx = stft(audio, fs=sr, nperseg=4096)
    magnitude = np.abs(Zxx)
    phase = np.angle(Zxx)
    
    num_freqs, num_time = magnitude.shape
    print(f"[+] High-Res Grid: {num_freqs} frequency bins x {num_time} time frames")

    # FAIL-SAFE: Verify if the fully mapped flag fits horizontally inside the track timeline
    if flag_matrix.shape[1] > num_time:
        hop_length = 1024 
        required_samples = flag_matrix.shape[1] * hop_length
        required_seconds = required_samples / sample_rate
        current_seconds = len(audio) / sample_rate
        
        print("\n" + "="*60)
        print("[CRITICAL ERROR] The text flag is too long for the audio file!")
        print(f" -> Audio duration: {current_seconds:.2f} seconds ({num_time} frames available)")
        print(f" -> Text image width requires: {flag_matrix.shape[1]} frames")
        print(f" -> Minimum audio length needed: {required_seconds:.2f} seconds")
        print("="*60 + "\n")
        
        raise ValueError("Embedding failed: Input audio is too short or the flag is too long.")

    # Get target frequency index bounds
    frequencies = np.linspace(0, sr / 2, num_freqs)
    min_target_hz = 18000
    max_target_hz = 23500
    
    idx_min = np.argmin(np.abs(frequencies - min_target_hz))
    idx_max = np.argmin(np.abs(frequencies - max_target_hz))
    target_height = idx_max - idx_min

    # Convert raw flag matrix back to PIL image
    img_obj = Image.fromarray((flag_matrix * 255).astype(np.uint8))
    
    # Resize directly to natural width and the bounded linear height window
    text_width = img_obj.width
    img_resized = img_obj.resize((text_width, target_height), Image.Resampling.LANCZOS)
    text_matrix = np.array(img_resized) / 255.0
    
    # Binary threshold for crispness
    text_matrix = (text_matrix > 0.2).astype(float)
    text_matrix = np.flipud(text_matrix)
    
    # Center the validated text matrix horizontally inside the timeline
    high_freq_grid = np.zeros_like(magnitude)
    pad_x = (num_time - text_width) // 2
    high_freq_grid[idx_min:idx_max, pad_x:pad_x + text_width] = text_matrix

    base_volume = np.max(magnitude) if np.max(magnitude) > 0 else 1.0
    scaled_text = high_freq_grid * (base_volume * strength)
    modified_magnitude = magnitude + scaled_text

    Zxx_new = modified_magnitude * np.exp(1j * phase)
    _, output_audio = istft(Zxx_new, fs=sr)

    if np.max(np.abs(output_audio)) > 0:
        output_audio /= np.max(np.abs(output_audio))

    sf.write(output_audio_path, output_audio, sr)
    print(f"[+] Complete, sharp, unclipped hidden audio generated: {output_audio_path}")

if __name__ == "__main__":
    flag_matrix = create_flag_image(FLAG)
    embed_image_to_audio(INPUT_AUDIO, flag_matrix, OUTPUT_AUDIO, SAMPLE_RATE, HIDDEN_STRENGTH)