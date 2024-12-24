import numpy as np
import wave
import matplotlib.pyplot as plt
from src.melody import GuitarMelody8bit, BassMelody8bit, DrumMelody8bit

guitar = GuitarMelody8bit(120)
bass = BassMelody8bit(120)
wav_guitar = guitar.gen_wave([('O', '1/4', ''), ('C4', '1/4', ''), ('C4', '1/4', ''), ('G4', '1/4', ''),
                              ('G4', '1/4', ''), ('A4', '1/4', ''), ('A4', '1/4', ''), ('G4', '1/4', ''),
                              ('O', '1/4', ''), ('F4', '1/4', ''), ('F4', '1/4', ''), ('E4', '1/4', ''),
                              ('E4', '1/4', ''), ('D4', '1/4', ''), ('D4', '1/4', ''), ('C4', '1/4', ''),
                              ('O', '1/4', '')])

wav_bass = bass.gen_wave([('O', '1/4', ''), ('C4', '1/4', ''), ('G4', '1/4', ''), ('E4', '1/4', ''),
                          ('G4', '1/4', ''), ('C4', '1/4', ''), ('G4', '1/4', ''), ('E4', '1/4', ''),
                          ('G4', '1/4', ''), ('C4', '1/4', ''), ('G4', '1/4', ''), ('E4', '1/4', ''),
                          ('G4', '1/4', ''), ('C4', '1/4', ''), ('G4', '1/4', ''), ('E4', '1/4', ''),
                          ('G5', '1/4', '')])

wav = wav_guitar + wav_bass

with wave.open('star_guitar.wav', 'wb') as f:
    f.setnchannels(1)
    f.setsampwidth(1)
    f.setframerate(guitar.sample_rate)
    f.writeframes(wav.tobytes())