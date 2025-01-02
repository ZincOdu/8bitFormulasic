from src.melody import Band8bit

guitar_score = [('O', '1/4', ''),
                ('G4', '1/8', 'pr'), ('A4', '1/8', 'pr'),
                ('C5', '1/4.', 'tr'), ('D5', '1/8', 'pr'), ('E5', '1/8', 'sl'), ('B4', '1/8', 'pr'),
                ('A4', '1/16', 'sl'), ('B4', '1/16', 'sl'), ('G4', '1/8', 'pr'),
                ('A4', '1/2', 'tr'), ('O', '1/2', '')]

bass_score = [('O', '1/2', ''),
              ('E3', '1/2', 'min-chord'), ('C3', '1/2', 'maj-arpeggio'),
              ('D3', '1/2', 'maj-chord'), ('O', '1/2', '')]

drum_score1 = [('O', '1/2', ''), ('X', '1/2', 'triple')]
drum_score2 = [('X', '1/8', ''), ('X', '1/8', 'hi-hat'), ('X', '1/8', 'hi-hat'), ('X', '1/8', 'hi-hat')]
drum_score3 = [('O', '1/2', '')]

band = Band8bit(72, {'guitar_theme':'guitar', 'bass_accompaniment':'bass', 'drum':'drum'})

band.gen_music({'guitar_theme':[(guitar_score,1)],
                'bass_accompaniment':[(bass_score,1)],
                'drum':[(drum_score1,1),(drum_score2,2),(drum_score3,1)]})

band.write_music('girl_love.wav')

