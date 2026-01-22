import numpy as np
import scipy.io.wavfile as wavfile
import random
import os

SAMPLE_RATE = 44100

def generate_sine_wave(freq, duration, amplitude=0.5):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    return wave

def generate_square_wave(freq, duration, amplitude=0.5):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    wave = amplitude * np.sign(np.sin(2 * np.pi * freq * t))
    return wave

def generate_noise(duration, amplitude=0.1):
    return np.random.normal(0, amplitude, int(SAMPLE_RATE * duration))

def envelope(wave, attack=0.01, release=0.5):
    total_samples = len(wave)
    attack_samples = min(int(attack * SAMPLE_RATE), total_samples // 2)
    release_samples = min(int(release * SAMPLE_RATE), total_samples // 2)
    
    env = np.ones(total_samples)
    
    # Attack
    if attack_samples > 0:
        env[:attack_samples] = np.linspace(0, 1, attack_samples)
    
    # Release
    if release_samples > 0:
        env[-release_samples:] = np.linspace(1, 0, release_samples)
        
    return wave * env

def apply_delay(wave, delay_sec=0.3, decay=0.5):
    delay_samples = int(delay_sec * SAMPLE_RATE)
    new_wave = np.zeros(len(wave) + delay_samples)
    new_wave[:len(wave)] = wave
    new_wave[delay_samples:] += wave * decay
    return new_wave[:len(wave)] # Truncate to original length

def get_scale(root_freq, scale_type="Major"):
    # Ratios from root
    major = [1, 9/8, 5/4, 4/3, 3/2, 5/3, 15/8, 2]
    minor = [1, 9/8, 6/5, 4/3, 3/2, 8/5, 9/5, 2]
    pentatonic = [1, 9/8, 5/4, 3/2, 5/3, 2] # Major Pent.
    dorian = [1, 9/8, 6/5, 4/3, 3/2, 5/3, 16/9, 2]
    
    selected_ratios = major
    if scale_type == "Minor": selected_ratios = minor
    elif scale_type == "Pentatonic": selected_ratios = pentatonic
    elif scale_type == "Dorian": selected_ratios = dorian
    
    return [root_freq * r for r in selected_ratios]

def generate_lofi_track(duration_sec, style="Lo-Fi Beats", output_filename="assets/generated/generated_track.wav"):
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)

    # Base track (silence)
    total_samples = int(SAMPLE_RATE * duration_sec)
    track = np.zeros(total_samples)
    
    # 1. Add Vinyl Crackle (Pink/White noise low amplitude)
    track += generate_noise(duration_sec, 0.015)
    
    # Determine musical parameters based on style
    root_freq_choice = random.choice([261.63, 220.00, 196.00, 174.61]) # C4, A3, G3, F3
    
    scale_type = "Major"
    bpm = 75
    instrument_decay = 0.8
    wave_func = generate_sine_wave
    use_delay = False
    
    if style == "Lo-Fi Beats":
        scale_type = "Minor"
        bpm = random.choice([70, 75, 80, 85])
        instrument_decay = 1.0
        wave_func = generate_sine_wave # Soft sine for 'keys'
        
    elif style == "Piano":
        scale_type = "Major"
        bpm = random.choice([60, 65, 70])
        instrument_decay = 2.0
        wave_func = generate_sine_wave

    elif style == "Ambient":
        scale_type = "Dorian"
        bpm = 60
        instrument_decay = 4.0
        use_delay = True
        
    elif style == "Synth":
        scale_type = "Pentatonic"
        bpm = 90
        instrument_decay = 0.5
        wave_func = generate_square_wave # Gritty square wave
        use_delay = True

    elif style == "Jazz Hop":
        scale_type = "Dorian"
        bpm = 85
        instrument_decay = 0.8
        wave_func = generate_sine_wave
        use_delay = False
    
    elif style == "Meditation":
        scale_type = "Pentatonic"
        bpm = 40
        instrument_decay = 5.0 # Very long pads
        wave_func = generate_sine_wave
        use_delay = True
        
    elif style == "8-Bit":
        scale_type = "Major"
        bpm = 120
        instrument_decay = 0.3 # Plucky
        wave_func = generate_square_wave
        use_delay = False

    scale = get_scale(root_freq_choice, scale_type)
    
    # 2. Chord Progression / Melody
    current_time = 0
    beat_dur = 60 / bpm
    
    # 4-bar loop length in seconds
    bar_length = beat_dur * 4
    
    while current_time < duration_sec:
        # Determine chord duration (1 bar or 1/2 bar)
        measure_rem = bar_length - (current_time % bar_length)
        step_duration = min(measure_rem, random.choice([beat_dur, beat_dur*2]))
        
        if style == "Meditation":
            step_duration = bar_length # Long drones
            
        if current_time + step_duration > duration_sec:
            step_duration = duration_sec - current_time
            
        if step_duration <= 0.05: break # Avoid tiny clips at end

        # Pick a random root note from scale low end
        root_idx = random.randint(0, 3) 
        
        # Build chord (Root, 3rd, 5th)
        chord_indices = [root_idx, (root_idx+2)%len(scale), (root_idx+4)%len(scale)]
        chord_freqs = [scale[i] for i in chord_indices]
        
        if style == "Jazz Hop":
             # Add a 7th note for jazz feel
             chord_indices.append((root_idx+6)%len(scale))
             chord_freqs = [scale[i] for i in chord_indices]

        # Random Melody Note (higher pitch)
        melody_note = None
        if random.random() > 0.3 and style != "Meditation":
            melody_note = scale[random.randint(3, len(scale)-1)] * (2 if random.random()>0.7 else 1)
        elif style == "Meditation" and random.random() > 0.7:
             # Occasional chime
             melody_note = scale[random.randint(4, len(scale)-1)] * 2

        # Generate Chord Audio
        for freq in chord_freqs:
            # Randomize decay slightly for human feel
            this_decay = instrument_decay * random.uniform(0.8, 1.2)
            
            note_dur = step_duration 
            if style in ["Ambient", "Meditation"]: note_dur += 3.0 # Let it ring overlap
            
            wave = wave_func(freq, note_dur, 0.15)
            
            # Specific Envelopes
            if style == "Meditation":
                 wave = envelope(wave, attack=1.0, release=3.0)
            elif style == "8-Bit":
                 wave = envelope(wave, attack=0.01, release=0.2)
            else:
                 wave = envelope(wave, attack=0.05, release=min(this_decay, note_dur))
            
            if use_delay:
                wave = apply_delay(wave, 0.4, 0.4)
            
            # Mix into track
            start_sample = int(current_time * SAMPLE_RATE)
            end_sample = start_sample + len(wave)
            
            if end_sample > total_samples:
                # Truncate wave to fit end of track
                valid_len = total_samples - start_sample
                if valid_len > 0:
                    track[start_sample:] += wave[:valid_len]
            else:
                track[start_sample:end_sample] += wave
                
        # Generate Melody Audio choice
        if melody_note:
            mel_start_offset = random.choice([0, beat_dur/2, beat_dur])
            if style == "Jazz Hop":
                 # Swing feel: delay off-beats slightly
                 if mel_start_offset == beat_dur/2:
                      mel_start_offset += 0.05 
                      
            mel_dur = step_duration - mel_start_offset
            if mel_dur > 0: 
                wave = wave_func(melody_note, mel_dur, 0.1)
                
                if style == "Meditation":
                     wave = envelope(wave, 0.5, 2.0)
                elif style == "8-Bit":
                     wave = envelope(wave, 0.01, 0.1) # Staccato
                else:
                     wave = envelope(wave, 0.02, 0.3)
                     
                if use_delay: wave = apply_delay(wave, 0.25, 0.3)
                
                start_s = int((current_time + mel_start_offset) * SAMPLE_RATE)
                end_s = start_s + len(wave)
                if end_s <= total_samples:
                    track[start_s:end_s] += wave
                elif start_s < total_samples:
                     track[start_s:] += wave[:total_samples-start_s]

        current_time += step_duration

    # 3. Add Drums
    if style in ["Lo-Fi Beats", "Synth", "Jazz Hop", "8-Bit"]:
        current_beat = 0
        while current_beat < duration_sec:
            # Kick on 1
            if current_beat < duration_sec:
                kick_dur = 0.15
                kick_freq = 55
                if style == "8-Bit": kick_dur = 0.1; kick_freq = 80 # Punchier
                
                kick = generate_sine_wave(random.choice([kick_freq, kick_freq+5]), kick_dur, 0.5)
                if style == "8-Bit": kick = generate_square_wave(kick_freq, kick_dur, 0.4) # Chiptune kick
                
                kick = envelope(kick, 0.01, 0.1)
                start = int(current_beat * SAMPLE_RATE)
                end = start + len(kick)
                if end <= total_samples: track[start:end] += kick
            
            # Snare/Clap on 2 
            snare_time = current_beat + beat_dur
            if style == "Jazz Hop":
                 # Slight laid back snare
                 snare_time += 0.03
                 
            if snare_time < duration_sec:
                snare_dur = 0.1
                snare = generate_noise(snare_dur, 0.25)
                if style == "8-Bit": snare = generate_noise(0.05, 0.3) # Short noise burst
                
                snare = envelope(snare, 0.005, 0.08)
                start = int(snare_time * SAMPLE_RATE)
                end = start + len(snare)
                if end <= total_samples: track[start:end] += snare
            
            # Hi-hats
            hat_subdiv = 4 # 16th notes
            if style == "Jazz Hop": hat_subdiv = 3 # Triplet feel sometimes? Or just swing 8ths
            
            for i in range(hat_subdiv):
                hat_time = current_beat + (i * (beat_dur/(hat_subdiv/2))) # Wait logic check..
                # Simple 8th notes: 0, 0.5
                # 16th notes: 0, 0.25, 0.5, 0.75
                
                if style == "Jazz Hop":
                     # Swing 8ths
                     if i == 0: hat_time = current_beat
                     elif i == 1: hat_time = current_beat + (beat_dur * 0.66) # Swing
                     else: continue
                else:
                     hat_time = current_beat + (i * (beat_dur/2))

                if hat_time < duration_sec:
                    if random.random() > 0.2: 
                        hat_dur = 0.05
                        hat = generate_noise(hat_dur, 0.1)
                        if style == "8-Bit": hat = generate_square_wave(800, 0.03, 0.1) # Blip hat
                        
                        hat = envelope(hat, 0.002, 0.03)
                        start = int(hat_time * SAMPLE_RATE)
                        end = start + len(hat)
                        if end <= total_samples: track[start:end] += hat

            current_beat += beat_dur * 2

    # Normalize
    max_val = np.max(np.abs(track))
    if max_val > 0:
        track = track / max_val * 0.95
        
    track_int16 = (track * 32767).astype(np.int16)
    wavfile.write(output_filename, SAMPLE_RATE, track_int16)
    return output_filename
