import numpy as np
import wave
from src.utils import (gen_square_wave,
                       gen_triangle_wave,
                       gen_zero_wave)


class Melody8bit:
    def __init__(self, bpm, amplitude, one_beat_note='quarter'):
        self.bpm = bpm  # beats per minute 60-240 节拍数
        self.amplitude = amplitude  # 1-255 音量
        self.one_beat_note = one_beat_note  # 'half', 'quarter', 'eighth' 以几分音符为一拍
        self.performances = {}  # 演奏技法
        self.sample_rate = 11025  # Hz 采样率
        self.instrument_duration = 0  # seconds 器乐固有时长

        if self.bpm < 60 or self.bpm > 240:
            raise ValueError("BPM should be between 60 and 240")
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

        one_beat_duration = 60 / self.bpm  # seconds
        eighth_beat_duration = one_beat_duration * 0.125

        self.eighth_beat_sample_count = int(round(eighth_beat_duration * self.sample_rate))
        self.quarter_beat_sample_count = int(self.eighth_beat_sample_count * 2)
        self.half_beat_sample_count = int(self.eighth_beat_sample_count * 4)
        self.one_beat_sample_count = int(self.eighth_beat_sample_count * 8)
        self.two_beat_sample_count = int(self.eighth_beat_sample_count * 16)
        self.four_beat_sample_count = int(self.eighth_beat_sample_count * 32)
        self.eight_beat_sample_count = int(self.eighth_beat_sample_count * 64)

        # 以二分音符为一拍
        if self.one_beat_note == 'half':
            # 二分音符、附点二分音符、四分音符、附点四分音符、八分音符、附点八分音符、全音符的采样点数
            self.note_sample_count = {'1/2': self.one_beat_sample_count,
                                      '1/2.': self.one_beat_sample_count + self.half_beat_sample_count,
                                      '1/4': self.half_beat_sample_count,
                                      '1/4.': self.half_beat_sample_count + self.quarter_beat_sample_count,
                                      '1/8': self.quarter_beat_sample_count,
                                      '1/8.': self.quarter_beat_sample_count + self.eighth_beat_sample_count,
                                      '1': self.two_beat_sample_count}
        # 以四分音符为一拍
        elif self.one_beat_note == 'quarter':
            # 二分音符、附点二分音符、四分音符、附点四分音符、八分音符、附点八分音符、全音符的时长
            self.note_sample_count = {'1/2': self.two_beat_sample_count,
                                      '1/2.': self.two_beat_sample_count + self.one_beat_sample_count,
                                      '1/4': self.one_beat_sample_count,
                                      '1/4.': self.one_beat_sample_count + self.half_beat_sample_count,
                                      '1/8': self.half_beat_sample_count,
                                      '1/8.': self.half_beat_sample_count + self.quarter_beat_sample_count,
                                      '1/16': self.quarter_beat_sample_count,
                                      '1/16.': self.quarter_beat_sample_count + self.eighth_beat_sample_count,
                                      '1': self.four_beat_sample_count}
        # 以八分音符为一拍
        elif self.one_beat_note == 'eighth':
            # 二分音符、附点二分音符、四分音符、附点四分音符、八分音符、附点八分音符、全音符的时长
            self.note_sample_count = {'1/2': self.four_beat_sample_count,
                                      '1/2.': self.four_beat_sample_count + self.two_beat_sample_count,
                                      '1/4': self.two_beat_sample_count,
                                      '1/4.': self.two_beat_sample_count + self.one_beat_sample_count,
                                      '1/8': self.one_beat_sample_count,
                                      '1/8.': self.one_beat_sample_count + self.half_beat_sample_count,
                                      '1/16': self.half_beat_sample_count,
                                      '1/16.': self.half_beat_sample_count + self.quarter_beat_sample_count,
                                      '1': self.eight_beat_sample_count}

    # 生成乐音基础演奏波形，时长仅为器乐固有时长，不占满音符
    def gen_instrument_normal_wave(self, frequency):
        return np.array([], dtype=np.uint8)

    # 生成乐音特殊演奏波形，时长占满音符
    def gen_instrument_technique_wave(self, technique, pitch, one_score_sample_count):
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
        if note not in self.note_sample_count.keys():
            raise ValueError(f'Unknown note: {note}, should be one of {self.note_sample_count.keys()}')

        score_sample_count = self.note_sample_count[note]

        # 休止符
        if pitch == 'O':
            return gen_zero_wave(score_sample_count)

        instrument_frequency = self.pitch_freq[pitch]

        # 普通单音：乐音 + 空白
        if len(technique) == 0:
            instrument_wave = self.gen_instrument_normal_wave(instrument_frequency)
            zero_sample_count = score_sample_count - len(instrument_wave)
            blank_wave = gen_zero_wave(zero_sample_count)
            return np.concatenate([instrument_wave, blank_wave])
        # 特殊技法
        else:
            return self.gen_instrument_technique_wave(technique, pitch, score_sample_count)

    def gen_wave(self, score_list, repeat_times=1):
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
        wav = np.concatenate(wave_list)
        return np.tile(wav, repeat_times)

    def write_wave(self, wav, file_path):
        with wave.open(file_path, 'wb') as f:
            f.setnchannels(1)
            f.setsampwidth(1)
            f.setframerate(self.sample_rate)
            f.writeframes(wav.tobytes())


# 吉他音色波形
class GuitarMelody8bit(Melody8bit):
    def __init__(self, bpm):
        super().__init__(bpm, 16)
        # 特殊技法：延音、颤音
        self.performances = {'pr': 'prolong 延音',
                             'tr': 'trill 颤音',
                             'sl': 'slide 滑音',
                             'maj-chord': 'major triad 大三和弦',
                             'maj-arpeggio': 'major triad arpeggio 大三和弦琶音',
                             'maj-broken1': 'major triad broken chord 大三和弦分解演奏1型',
                             'min-chord': 'minor triad 小三和弦',
                             'min-arpeggio': 'minor triad arpeggio 小三和弦琶音',
                             'min-broken1': 'minor triad broken chord 小三和弦分解演奏1型',
                             'dim-chord': 'diminished triad 减三和弦',
                             'dim-arpeggio': 'diminished triad arpeggio 减三和弦琶音',
                             'dim-broken1': 'diminished triad broken chord 减三和弦分解演奏1型',
                             'aug-chord': 'augmented triad 增三和弦',
                             'aug-arpeggio': 'augmented triad arpeggio 增三和弦琶音',
                             'aug-broken1': 'augmented triad broken chord 增三和弦分解演奏1型',
                             }
        self.instrument_duration = 0.1  # seconds

        self.timbre_function = gen_square_wave

    def gen_instrument_normal_wave(self, frequency):
        return self.timbre_function(frequency, self.amplitude, self.instrument_duration, self.sample_rate)

    def gen_prolong_wave(self, frequency, one_score_sample_count):
        one_score_duration = one_score_sample_count / self.sample_rate
        prolong_duration = one_score_duration * 0.9
        wav1 = self.timbre_function(frequency, self.amplitude, prolong_duration, self.sample_rate)
        zero_sample_count = one_score_sample_count - len(wav1)
        wav2 = gen_zero_wave(zero_sample_count)
        return np.concatenate([wav1, wav2])

    def gen_trill_wave(self, frequency, one_score_sample_count):
        trill_blank_duration = 0.01
        instrument_duration = self.instrument_duration * 0.8
        wav1 = self.timbre_function(frequency, self.amplitude, instrument_duration, self.sample_rate)
        trill_blank_sample_count = int(round(trill_blank_duration * self.sample_rate))
        wav2 = gen_zero_wave(trill_blank_sample_count)
        wav_one_trill = np.concatenate([wav1, wav2])
        trill_count = int(one_score_sample_count / len(wav_one_trill))
        wav_trills = np.tile(wav_one_trill, trill_count)
        res_sample_count = one_score_sample_count - len(wav_trills)
        res_wave = gen_zero_wave(res_sample_count)
        return np.concatenate([wav_trills, res_wave])

    def gen_slide_wave(self, frequency, one_score_sample_count):
        one_score_duration = one_score_sample_count / self.sample_rate
        wav = self.timbre_function(frequency, self.amplitude, one_score_duration, self.sample_rate)
        if len(wav) < one_score_sample_count:
            zero_sample_count = one_score_sample_count - len(wav)
            wav = np.concatenate([wav, gen_zero_wave(zero_sample_count)])
        elif len(wav) > one_score_sample_count:
            wav = wav[:one_score_sample_count]
        return wav

    def get_chord_frequency(self, pitch, chord_type):
        if chord_type == 'maj':
            # 根音、三音（大三度）、五音（小三度）
            root_frequency = self.pitch_freq[pitch]
            third_frequency = root_frequency * 1.259921
            fifth_frequency = root_frequency * 1.498307
            return root_frequency, third_frequency, fifth_frequency
        elif chord_type == 'min':
            # 根音、三音（小三度）、五音（大三度）
            root_frequency = self.pitch_freq[pitch]
            third_frequency = root_frequency * 1.189207
            fifth_frequency = root_frequency * 1.498307
            return root_frequency, third_frequency, fifth_frequency
        elif chord_type == 'dim':
            # 根音、三音（小三度）、五音（小三度）
            root_frequency = self.pitch_freq[pitch]
            third_frequency = root_frequency * 1.189207
            fifth_frequency = root_frequency * 1.414214
            return root_frequency, third_frequency, fifth_frequency
        elif chord_type == 'aug':
            # 根音、三音（大三度）、五音（大三度）
            root_frequency = self.pitch_freq[pitch]
            third_frequency = root_frequency * 1.259921
            fifth_frequency = root_frequency * 1.587401
            return root_frequency, third_frequency, fifth_frequency

    def gen_chord_wave(self, root_frequency, third_frequency, fifth_frequency, one_score_sample_count):
        wav1 = self.gen_prolong_wave(root_frequency, one_score_sample_count)
        wav2 = self.gen_prolong_wave(third_frequency, one_score_sample_count)
        wav3 = self.gen_prolong_wave(fifth_frequency, one_score_sample_count)
        wav = wav1 + wav2 + wav3
        return wav

    def gen_arpeggio_wave(self, root_frequency, third_frequency, fifth_frequency, one_score_sample_count):
        pass
        # TODO: 实现和弦琶音演奏波形

    def gen_broken1_wave(self, root_frequency, third_frequency, fifth_frequency, one_score_sample_count):
        pass
        # TODO: 实现和弦分解演奏1型

    def gen_instrument_technique_wave(self, technique, pitch, one_score_sample_count):
        if technique not in self.performances.keys():
            raise ValueError(f'Unknown technique: {technique}, should be one of {self.performances.keys()}')
        if '-' not in technique:
            frequency = self.pitch_freq[pitch]
            if technique == 'pr':
                return self.gen_prolong_wave(frequency, one_score_sample_count)
            elif technique == 'tr':
                return self.gen_trill_wave(frequency, one_score_sample_count)
            elif technique == 'sl':
                return self.gen_slide_wave(frequency, one_score_sample_count)
        else:
            techniques = technique.split('-')
            chord_type = techniques[0]
            perform_type = techniques[1]
            root_frequency, third_frequency, fifth_frequency = self.get_chord_frequency(pitch, chord_type)
            if perform_type == 'chord':
                return self.gen_chord_wave(root_frequency, third_frequency, fifth_frequency, one_score_sample_count)
            elif perform_type == 'arpeggio':
                return self.gen_arpeggio_wave(root_frequency, third_frequency, fifth_frequency, one_score_sample_count)
            elif perform_type == 'broken1':
                return self.gen_broken1_wave(root_frequency, third_frequency, fifth_frequency, one_score_sample_count)


# 贝司音色波形
class BassMelody8bit(GuitarMelody8bit):
    def __init__(self, bpm):
        super().__init__(bpm)
        self.timbre_function = gen_triangle_wave


# 架子鼓音色波形
class DrumMelody8bit(Melody8bit):
    def __init__(self, bpm):
        super().__init__(bpm, 16)
        self.instrument_duration = 0.1  # seconds

    def gen_instrument_normal_wave(self, frequency):
        pass
        # TODO: 实现架子鼓音色波形
