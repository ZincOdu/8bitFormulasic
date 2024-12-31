import matplotlib.pyplot as plt
from src.melody import Guitar8bit, Bass8bit, Drum8bit, MelodyAssist8bit
import numpy as np
import wave

guitar = Guitar8bit(72)
bass = Bass8bit(72)
drum = Drum8bit(72)

# wav_guitar = guitar.gen_wave([('O', '1/4', ''),
#                               ('G4', '1/8', 'pr'), ('A4', '1/8', 'pr'),
#                               ('C5', '1/4.', 'tr'), ('D5', '1/8', 'pr'), ('E5', '1/8', 'sl'), ('B4', '1/8', 'pr'),
#                               ('A4', '1/16', 'sl'), ('B4', '1/16', 'sl'), ('G4', '1/8', 'pr'),
#                               ('A4', '1/2', 'tr'), ('O', '1/2', '')])
# wav_bass = bass.gen_wave([('O', '1/2', ''),
#                           ('E3', '1/2', 'min-chord'), ('C3', '1/2', 'maj-arpeggio'),
#                           ('D3', '1/2', 'maj-chord'), ('O', '1/2', '')])
#
# wav_drum = drum.gen_wave([('O', '1/2', ''), ('X', '1/2', 'triple'),
#                           ('X', '1/8', ''), ('X', '1/8', 'hi-hat'), ('X', '1/8', 'hi-hat'), ('X', '1/8', 'hi-hat'),
#                           ('X', '1/8', ''), ('X', '1/8', 'hi-hat'), ('X', '1/8', 'hi-hat'), ('X', '1/8', 'hi-hat'),
#                           ('O', '1/2', '')])
#
# wav = wav_guitar + wav_bass + wav_drum
#
# guitar.write_wave(wav_drum, 'girl_love_drum.wav')

melody_assist = MelodyAssist8bit()

pitches = melody_assist.get_chord_pitches('C4','maj7')

wavs = []

for pitch in pitches:
    wav = guitar.gen_wave([('O', '1/4', ''),
                           (pitch, '1/2', 'pr'),
                           ('O', '1/4', '')])
    wavs.append(wav)

wav = np.zeros(len(wavs[0]), dtype=np.uint8)
for i in range(len(wavs)):
    wav += wavs[i]

with wave.open('chord.wav', 'wb') as f:
    f.setnchannels(1)
    f.setsampwidth(1)
    f.setframerate(11025)
    f.writeframes(wav.tobytes())