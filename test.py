import matplotlib.pyplot as plt
from src.melody import GuitarMelody8bit, BassMelody8bit, DrumMelody8bit

guitar = GuitarMelody8bit(72)
bass = BassMelody8bit(72)
drum = DrumMelody8bit(72)

wav_guitar = guitar.gen_wave([('O', '1/4', ''),
                              ('G3', '1/8', 'pr'),('A3', '1/8', 'pr'),
                              ('C4','1/4.','tr'),('D4','1/8','pr'),('E4','1/8','sl'),('B3','1/8','pr'),
                              ('A3','1/16', 'sl'), ('B3','1/16', 'sl'), ('G3','1/8', 'pr'),
                              ('A3','1/2', 'tr'), ('O', '1/2', '')])
wav_bass = bass.gen_wave([('O', '1/2', ''),
                          ('E3', '1/2', 'min-chord'), ('C3', '1/2', 'maj-arpeggio'),
                          ('D3', '1/2', 'maj-chord'), ('O', '1/2', '')])

wav_drum = drum.gen_wave([('O', '1/2', ''),
                          ('X', '1/2', ''), ('X', '1/2', ''),
                          ('X', '1/2', 'triple'), ('O', '1/2', '')])

wav = wav_guitar + wav_bass + wav_drum

guitar.write_wave(wav, 'girl_love.wav')