import numpy as np
import scipy.io.wavfile as wavfile
import random
import os

SAMPLE_RATE = 44100

def generate_sine_wave(freq, duration, amplitude=0.5):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    return wave

def generate_noise(duration, amplitude=0.1):
    return np.random.normal(0, amplitude, int(SAMPLE_RATE * duration))

def envelope(wave, attack=0.01, release=0.5):
    total_samples = len(wave)
    attack_samples = int(attack * SAMPLE_RATE)
    release_samples = int(release * SAMPLE_RATE)
    
    env = np.ones(total_samples)
    
    # Attack
    if attack_samples > 0:
        env[:attack_samples] = np.linspace(0, 1, attack_samples)
    
    # Release
    if release_samples > 0:
        env[-release_samples:] = np.linspace(1, 0, release_samples)
        
    return wave * env

def generate_lofi_track(duration_sec, style="Lo-Fi Beats", output_filename="assets/generated/generated_track.wav"):
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)

    # Base track (silence)
    total_samples = int(SAMPLE_RATE * duration_sec)
    track = np.zeros(total_samples)
    
    # 1. Add Vinyl Crackle (Pink/White noise low amplitude)
    track += generate_noise(duration_sec, 0.02)
    
    # ... (rest of logic unaffected, skip to file writing) ...

    # Convert to 16-bit PCM
    track_int16 = (track * 32767).astype(np.int16)
    
    wavfile.write(output_filename, SAMPLE_RATE, track_int16)
    return output_filename
