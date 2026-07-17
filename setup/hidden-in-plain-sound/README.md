# Setup: Hidden in Plain Sight

This guide provides the necessary steps to configure, test, and deploy the "Hidden in Plain Sight" audio steganography challenge.

---

## 1. Prerequisites & Dependencies

The challenge deployment relies on Python 3 and a few external data processing libraries. Ensure the system has the following dependencies installed before running the generation script.

### System Libraries
* **libsndfile** (Required by `soundfile` on Linux distributions):
```bash
sudo apt-get update && sudo apt-get install libsndfile1
```

### Python Packages

Install the required Python modules via `pip`:

```bash
pip install numpy soundfile pillow scipy
```

---

## 2. Directory Structure

Organize your challenge development folder as follows before executing the script:

```text
hidden_in_plain_sound/
├── original.wav             # The source audio track (e.g., Never Gonna Give You Up)
├── create_hidden_sound.py    # The Python embedding script provided below
├── challenge.md             # The player-facing challenge description
└── README.md                # This setup guide

```

---

## 3. Configuration & Deployment

Follow these steps to customize the flag value and bake it into the final audio distribution file.

### Step 1: Set Your Secret Flag

Open `generate_challenge.py` and modify the global configuration parameters at the top of the file:

```python
# =========================================================================
# CONFIG
# =========================================================================
FLAG = "flag:PUT_YOUR_FLAG_HERE"                # Change to your desired flag
INPUT_AUDIO = "original.wav"                    # Must be placed in the directory
OUTPUT_AUDIO = "my_favorite_song.wav"           # Output file name for distribution
SAMPLE_RATE = 48000                             # Enforced high sample-rate for ultrasonic bands

```

### Step 2: Run the Generator

Execute the generation script. The script automatically calculates the minimum time duration required for your specific flag length to prevent text clipping:

```bash
python generate_challenge.py

```

**Expected Console Output:**

```text
[+] Loading cover audio...
[+] High-Res Grid: 2049 frequency bins x 1280 time frames
[+] Complete, sharp, unclipped hidden audio generated: my_favorite_song.wav

```

---

## 4. Local Quality Assurance & Verification

Before publishing the challenge infrastructure, verify that the artifact was compiled cleanly and meets visual visibility metrics.

1. **Open the Generated File:** Import `my_favorite_song.wav` into an audio visualization suite like **Audacity**.
2. **Switch to Spectrogram View:** Click the track drop-down menu on the left pane and select **Spectrogram**.
3. **Adjust Spectrum Settings:**
* Navigate to *Preferences -> Spectrograms*.
* Ensure the **Scale** is set to `Linear`.
* Set the **Max Frequency** bound to at least `24000 Hz`.


4. **Inspect the Target Window:** Scroll or zoom directly into the upper boundary region between `18,000 Hz` and `23,500 Hz`. Confirm that the font contours are solid, continuous, and clearly legible without edge clipping.

---

## 5. Artifact Distribution

Once local validation passes, package only the following resources to be distributed to players via the CTF platform:

* `challenge.md` (Contains the story description and hints)
* `my_favorite_song.wav` (The generated steganographic audio track)

> [!CAUTION]
> Do **not** package `original.wav` or `generate_challenge.py` into the public-facing download archive, as they contain reference materials.
