import matplotlib.pyplot as plt
from src.melody import Guitar8bit, Bass8bit, Drum8bit, MelodyAssist8bit

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

res = melody_assist.gen_random_chord_progression('C-min', 'T-S-D-T')

print(res)