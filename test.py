import matplotlib.pyplot as plt
from src.melody import Band8bit, MelodyAssist8bit

guitar_theme = [('O', '1/4', ''),
                ('G4', '1/8', 'pr'), ('A4', '1/8', 'pr'),
                ('C5', '1/4.', 'tr'), ('D5', '1/8', 'pr'), ('E5', '1/8', 'sl'), ('B4', '1/8', 'pr'),
                ('A4', '1/16', 'sl'), ('B4', '1/16', 'sl'), ('G4', '1/8', 'pr'),
                ('A4', '1/2', 'tr'), ('O', '1/2', '')]

bass = [('O', '1/2', ''),
        ('E3', '1/2', 'min-chord'), ('C3', '1/2', 'maj-arpeggio'),
        ('D3', '1/2', 'maj-chord'), ('O', '1/2', '')]

drum = [('O', '1/2', ''), ('X', '1/2', 'triple'),
        ('X', '1/8', ''), ('X', '1/8', 'hi-hat'), ('X', '1/8', 'hi-hat'), ('X', '1/8', 'hi-hat'),
        ('X', '1/8', ''), ('X', '1/8', 'hi-hat'), ('X', '1/8', 'hi-hat'), ('X', '1/8', 'hi-hat'),
        ('O', '1/2', '')]

band = Band8bit(72, {'guitar_theme':'guitar', 'bass':'bass', 'drum':'drum'})

band.gen_music({'guitar_theme':[(guitar_theme,1)], 'bass':[(bass,1)], 'drum':[(drum,1)]})

band.write_music('girl_love.wav')


