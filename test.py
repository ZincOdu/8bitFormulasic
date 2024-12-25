import wave
from src.melody import GuitarMelody8bit, BassMelody8bit

guitar = GuitarMelody8bit(72)
bass = BassMelody8bit(72)
wav_guitar = guitar.gen_wave([('O', '1/4', ''),
                              ('G3', '1/8', 'pr'),('A3', '1/8', 'pr'),
                              ('C4','1/4.','tr'),('D4','1/8','pr'),('E4','1/8','sl'),('B3','1/8','pr'),
                              ('A3','1/16', 'sl'), ('B3','1/16', 'sl'), ('G3','1/8', 'pr'),
                              ('A3','1/2', 'tr')])
# wav_bass = bass.gen_wave([('O', '1/2', ''),
#                           ('E2', '1/2', '')])

guitar.write_wave(wav_guitar, 'sister_love.wav')