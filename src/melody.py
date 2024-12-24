import numpy as np


class Melody8bit:
    def __init__(self, bpm, amplitude, one_beat_note='quarter'):
        self.bpm = bpm  # beats per minute 120-240 节拍数
        self.amplitude = amplitude  # 1-255 音量
        self.one_beat_note = one_beat_note  # 'half', 'quarter', 'eighth' 以几分音符为一拍
        self.performances = {}  # 演奏技法
        self.sample_rate = 11025  # Hz 采样率
        self.instrument_duration = 0  # seconds 乐音持续时间

        if self.bpm < 120 or self.bpm > 240:
            raise ValueError("BPM should be between 120 and 240")
        if self.amplitude < 1 or self.amplitude > 255:
            raise ValueError("Amplitude should be between 1 and 255")
        if self.one_beat_note not in ['half', 'quarter', 'eighth']:
            raise ValueError("One beat note should be 'half', 'quarter', or 'eighth'")

        self.pitch_freq = {'C3': 130.81, 'D3': 146.83, 'E3': 164.81, 'F3': 174.61, 'G3': 196.00, 'A3': 220.00,
                           'B3': 246.94, 'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23, 'G4': 392.00,
                           'A4': 440.00, 'B4': 493.88, 'C5': 523.25, 'D5': 587.33, 'E5': 659.26, 'F5': 698.46,
                           'G5': 783.99, 'A5': 880.00, 'B5': 987.77, 'C6': 1046.50, 'D6': 1174.66, 'E6': 1318.51,
                           'F6': 1396.91, 'G6': 1567.98, 'A6': 1760.00, 'B6': 1975.53, 'C7': 2093.00, 'D7': 2349.32,
                           'E7': 2637.02, 'F7': 2793.83, 'G7': 3135.96, 'A7': 3520.00, 'B7': 3951.07, '#C3': 138.59,
                           '#D3': 155.56, '#F3': 185.00, '#G3': 207.65, '#A3': 233.08, '#C4': 277.18, '#D4': 311.13,
                           '#F4': 369.99, '#G4': 415.30, '#A4': 466.16, '#C5': 554.37, '#D5': 622.25, '#F5': 739.99,
                           '#G5': 830.61, '#A5': 932.33, '#C6': 1108.73, '#D6': 1244.51, '#F6': 1479.98, '#G6': 1661.22,
                           '#A6': 1864.66, '#C7': 2217.46, '#D7': 2489.02, '#F7': 2959.96, '#G7': 3322.44, 'O': 0.0}

        self.one_beat_duration = 60 / self.bpm  # seconds
        self.half_beat_duration = self.one_beat_duration * 0.5
        self.quarter_beat_duration = self.one_beat_duration * 0.25
        self.eighth_beat_duration = self.one_beat_duration * 0.125
        self.two_beat_duration = self.one_beat_duration * 2
        self.four_beat_duration = self.one_beat_duration * 4
        self.eight_beat_duration = self.one_beat_duration * 8

        # 以二分音符为一拍
        if self.one_beat_note == 'half':
            # 二分音符、附点二分音符、四分音符、附点四分音符、八分音符、附点八分音符、全音符的时长
            self.note_duration = {'1/2': self.one_beat_duration,
                                  '1/2.': self.one_beat_duration + self.half_beat_duration,
                                  '1/4': self.half_beat_duration,
                                  '1/4.': self.half_beat_duration + self.quarter_beat_duration,
                                  '1/8': self.quarter_beat_duration,
                                  '1/8.': self.quarter_beat_duration + self.eighth_beat_duration,
                                  '1': self.two_beat_duration}
        # 以四分音符为一拍
        elif self.one_beat_note == 'quarter':
            # 二分音符、附点二分音符、四分音符、附点四分音符、八分音符、附点八分音符、全音符的时长
            self.note_duration = {'1/2': self.two_beat_duration,
                                  '1/2.': self.two_beat_duration + self.one_beat_duration,
                                  '1/4': self.one_beat_duration,
                                  '1/4.': self.one_beat_duration + self.half_beat_duration,
                                  '1/8': self.half_beat_duration,
                                  '1/8.': self.half_beat_duration + self.quarter_beat_duration,
                                  '1': self.four_beat_duration}
        # 以八分音符为一拍
        elif self.one_beat_note == 'eighth':
            # 二分音符、附点二分音符、四分音符、附点四分音符、八分音符、附点八分音符、全音符的时长
            self.note_duration = {'1/2': self.four_beat_duration,
                                  '1/2.': self.four_beat_duration + self.two_beat_duration,
                                  '1/4': self.two_beat_duration,
                                  '1/4.': self.two_beat_duration + self.one_beat_duration,
                                  '1/8': self.one_beat_duration,
                                  '1/8.': self.one_beat_duration + self.half_beat_duration,
                                  '1': self.eight_beat_duration}

    def gen_zero_wave(self, duration):
        num_samples = int(duration * self.sample_rate)
        zero_wave = np.zeros(num_samples, dtype=np.uint8)
        return zero_wave

    # 生成乐音基础演奏波形
    def gen_instrument_normal_wave(self, frequency):
        return np.array([], dtype=np.uint8)

    # 生成乐音特殊演奏波形
    def gen_instrument_technique_wave(self, technique, frequency, duration):
        return np.array([], dtype=np.uint8)

    # 生成一个音符的波形
    def gen_one_score_wave(self, score):
        """
        # 音名 音符 特殊技法
        score example: ('C4', '1/4', '')
        """
        pitch = score[0]
        note = score[1]
        technique = score[2]

        if pitch not in self.pitch_freq.keys():
            raise ValueError(f'Unknown pitch: {pitch}, should be one of {self.pitch_freq.keys()}')
        if note not in self.note_duration:
            raise ValueError(f'Unknown note: {note}, should be one of {self.note_duration.keys()}')

        score_duration = self.note_duration[note]
        # 休止符
        if pitch == 'O':
            return self.gen_zero_wave(score_duration)
        instrument_frequency = self.pitch_freq[pitch]

        if len(technique) == 0:
            zero_duration = max(0, score_duration - self.instrument_duration)
            return np.concatenate([self.gen_instrument_normal_wave(instrument_frequency),
                                   self.gen_zero_wave(zero_duration)])
        else:
            return self.gen_instrument_technique_wave(technique, instrument_frequency, score_duration)

    def gen_wave(self, score_list):
        """
        score_list example: [('C4', '1/4', ''),
                             ('D4', '1/4', ''),
                             ('E4', '1/2', '')]
        """
        wave_list = []
        for score in score_list:
            if not isinstance(score, tuple) or len(score) != 3:
                raise ValueError(f"score_list example: [('C4', '1/4', ''),...]")
            wave_list.append(self.gen_one_score_wave(score))
        return np.concatenate(wave_list)


# 吉他音色波形
class GuitarMelody8bit(Melody8bit):
    def __init__(self, bpm):
        super().__init__(bpm, 16)
        # 特殊技法：延音、颤音
        self.performances = {'pr': 'prolong',
                             'tr': 'trill'}
        self.instrument_duration = 0.1  # seconds

    def gen_instrument_normal_wave(self, frequency):
        num_samples = int(self.instrument_duration * self.sample_rate)
        t = np.linspace(0, self.instrument_duration, num_samples, endpoint=False)
        square_wave = np.where(np.mod(frequency * t, 1) < 0.5, self.amplitude, 0)
        square_wave = np.uint8(square_wave)
        return square_wave

    def gen_prolong_wave(self, frequency, duration):
        pass
        # TODO: 实现延音

    def gen_trill_wave(self, frequency, duration):
        pass
        # TODO: 实现颤音

    def gen_instrument_technique_wave(self, technique, frequency, duration):
        if technique == 'pr':
            return self.gen_prolong_wave(frequency, duration)
        elif technique == 'tr':
            return self.gen_trill_wave(frequency, duration)
        else:
            raise ValueError(
                f'Unknown technique: {technique}, should be one of {self.performances.keys()} or empty string')


# 贝司音色波形
class BassMelody8bit(Melody8bit):
    def __init__(self, bpm):
        super().__init__(bpm, 32)
        self.instrument_duration = 0.1  # seconds

    def gen_instrument_normal_wave(self, frequency):
        num_samples = int(self.instrument_duration * self.sample_rate)
        t = np.linspace(0, self.instrument_duration, num_samples, endpoint=False)
        triangle_wave = np.abs(np.mod(frequency * t, 1) - 0.5) * 2 * self.amplitude
        triangle_wave = np.uint8(triangle_wave)
        return triangle_wave


# 架子鼓音色波形
class DrumMelody8bit(Melody8bit):
    def __init__(self, bpm):
        super().__init__(bpm, 16)
        self.instrument_duration = 0.1  # seconds

    def gen_instrument_normal_wave(self, frequency):
        pass
        # TODO: 实现架子鼓音色波形
