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

def generate_lofi_track(duration_sec, style="Lo-Fi Beats"):
    # Base track (silence)
    total_samples = int(SAMPLE_RATE * duration_sec)
    track = np.zeros(total_samples)
    
    # 1. Add Vinyl Crackle (Pink/White noise low amplitude)
    track += generate_noise(duration_sec, 0.02)
    
    # 2. Chord Progression (Simple randomized chords)
    # C major scale frequencies
    # C4, D4, E4, F4, G4, A4, B4
    scale = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88]
    
    # Style customization
    if style == "Piano":
        instrument_decay = 1.5
    elif style == "Ambient":
        instrument_decay = 3.0
    else:
        instrument_decay = 0.8

    # Generate some chords/melody
    current_time = 0
    while current_time < duration_sec:
        chord_duration = 2.0 # seconds
        if current_time + chord_duration > duration_sec:
            chord_duration = duration_sec - current_time
            
        # Pick a random root note
        root_idx = random.randint(0, len(scale)-3)
        # Simple triad
        chord_freqs = [scale[root_idx], scale[root_idx+2]]
        if random.random() > 0.5: # sometimes add 3rd note
            if root_idx + 4 < len(scale):
                chord_freqs.append(scale[root_idx+4])
        
        for freq in chord_freqs:
            wave = generate_sine_wave(freq, chord_duration, 0.2)
            wave = envelope(wave, attack=0.1, release=instrument_decay)
            
            start_sample = int(current_time * SAMPLE_RATE)
            end_sample = start_sample + len(wave)
            
            # Simple mixing (add to track)
            if end_sample <= total_samples:
                track[start_sample:end_sample] += wave
                
        current_time += chord_duration

    # 3. Add Drums (Simple kick/snare pattern) if "Beats" or "Lo-Fi"
    if "Beats" in style or style == "Lo-Fi Beats":
        bpm = 80
        beat_interval = 60 / bpm
        current_beat = 0
        while current_beat < duration_sec:
            # Kick on beat 1
            kick_dur = 0.2
            kick = generate_sine_wave(60, kick_dur, 0.4)
            kick = envelope(kick, 0.01, 0.1)
            
            start = int(current_beat * SAMPLE_RATE)
            end = start + len(kick)
            if end <= total_samples:
                track[start:end] += kick
            
            # Snare/Hat on beat 2 (just noise burst)
            if current_beat + beat_interval < duration_sec:
                snare_time = current_beat + beat_interval
                snare_dur = 0.1
                snare = generate_noise(snare_dur, 0.15)
                snare = envelope(snare, 0.005, 0.05)
                
                start = int(snare_time * SAMPLE_RATE)
                end = start + len(snare)
                if end <= total_samples:
                    track[start:end] += snare
            
            current_beat += beat_interval * 2

    # Normalize to avoid clipping
    max_val = np.max(np.abs(track))
    if max_val > 0:
        track = track / max_val * 0.9
        
    # Convert to 16-bit PCM
    track_int16 = (track * 32767).astype(np.int16)
    
    filename = "generated_track.wav"
    wavfile.write(filename, SAMPLE_RATE, track_int16)
    return filename
