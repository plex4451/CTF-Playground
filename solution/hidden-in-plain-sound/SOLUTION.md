# Solution for Hidden in Plain Sound

## Explanation
The challenge hides a text flag within an audio file by leveraging the concept of a spectrogram and the physical limits of human hearing.

An audio signal can be broken down into its individual frequencies over time using a mathematical process called a Short-Time Fourier Transform (STFT). When visualized, this creates a spectrogram where the horizontal axis represents time, the vertical axis represents frequency, and the brightness represents amplitude (volume).

Because the perfect upper limit of human hearing is roughly 20,000 Hz (and lower for most adults), any sound injected above 18,000 Hz is completely silent to a listener. The challenge generates a custom image of the flag text and uses a script to translate the pixels of that image directly into intense high-frequency audio tones mapped strictly between 18,000 Hz and 23,500 Hz.

To solve the challenge, a player cannot rely on standard audio playback. Instead, they must open the file in an audio analysis tool, switch the visual representation from a standard time-domain waveform to a frequency-domain spectrogram, and adjust the vertical frequency bounds to display the ultrasonic spectrum using a linear scale. This visually reconstructs the text pixels directly on the screen, revealing the flag.


## Walkthrough - Audacity

1. Download the provided challenge file, my_favorite_song.wav.
2. Open the audio file using Audacity (a free, open-source audio editor).
3. By default, Audacity displays the standard audio waveform. Click the small downward-pointing arrow next to the track name on the left side of the screen.
4. Select Spectrogram from the drop-down menu. You will see the visual representation of the audio, but the top will likely look empty or squished.
5. Click the track name drop-down menu again and select Spectrogram Settings... (or go to Edit > Preferences > Spectrograms).
6. Change the Scale option from Logarithmic (or Mel/Bark) to Linear.
7. Change the Maximum Frequency (Hz) to 24000 (which is the physical limit of our 48kHz sample rate). Click OK.
8. Scroll or zoom your view to look at the very top of the spectrogram, specifically the band between 18,000 Hz and 23,500 Hz.
9. The flag should now be visible.

## Flag

```
flag:never_gonna_spektrogram_you_up