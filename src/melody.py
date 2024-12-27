import numpy as np
import wave
from abc import ABC, abstractmethod
from src.utils import gen_square_wave, gen_triangle_wave, gen_zero_wave, gen_noise_wave, regularize_wave


# 节拍类
class Rhythm8bit(ABC):
    def __init__(self, bpm, one_beat_note='quarter'):
        self.bpm = bpm  # beats per minute 60-240 节拍数
        self.one_beat_note = one_beat_note  # 'half', 'quarter', 'eighth' 以几分音符为一拍
        self.sample_rate = 11025  # 采样率  # Hz 采样率

        # child class set
        self.amplitude = 0  # 0-255 音量
        self.instrument_duration = 0  # seconds 器乐固有时长
        self.performances = {}  # 演奏技法
        self.pitch_dict = {'O': 0}  # 音符字典 必须包含'O'，表示休止符

        if self.bpm < 60 or self.bpm > 240:
            raise ValueError("BPM should be between 60 and 240")
        if self.one_beat_note not in ['half', 'quarter', 'eighth']:
            raise ValueError("One beat note should be 'half', 'quarter', or 'eighth'")

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

    @abstractmethod
    def gen_timbre_wave(self, pitch: str, duration: float) -> np.array:
        """
        生成一个音符的基音波形
        pitch字串是self.pitch_dict中的键值
        duration是音符的时长，单位为秒
        """
        pass

    @abstractmethod
    def gen_instrument_technique_wave(self, pitch: str, one_score_sample_count: int, technique: str) -> np.array:
        """
        生成一个音符的特技演奏波形
        pitch字串是self.pitch_dict中的键值
        one_score_sample_count是一拍的采样点数
        technique是self.performances中的键值，技法名称
        """
        pass

    def gen_one_score_wave(self, score: (str, str, str)) -> np.array:
        """
        生成一个音符的波形
        score是音符，格式为(pitch,note,technique)的元组
        """
        pitch = score[0]
        note = score[1]
        technique = score[2]

        if pitch not in self.pitch_dict.keys():
            raise ValueError(f'Unknown pitch: {pitch}, should be one of {self.pitch_dict.keys()}')
        if note not in self.note_sample_count.keys():
            raise ValueError(f'Unknown note: {note}, should be one of {self.note_sample_count.keys()}')
        if technique not in self.performances.keys() and len(technique) > 0:
            raise ValueError(f'Unknown technique: {technique}, should be one of {self.performances.keys()}')

        score_sample_count = self.note_sample_count[note]

        # 休止符
        if pitch == 'O':
            return gen_zero_wave(score_sample_count)

        # 普通单音
        if len(technique) == 0:
            wav = self.gen_timbre_wave(pitch, self.instrument_duration)
        # 特殊技法
        else:
            wav = self.gen_instrument_technique_wave(pitch, score_sample_count, technique)

        return regularize_wave(wav, score_sample_count)

    def gen_wave(self, score_list: [(str, str, str)], repeat_times=1):
        """
        score_list: [(pitch, note, technique),...]
        """
        wave_list = []
        for score in score_list:
            if not isinstance(score, tuple) or len(score) != 3:
                raise ValueError(f"score_list: [(pitch, note, technique),...]")
            wave_list.append(self.gen_one_score_wave(score))
        wav = np.concatenate(wave_list)
        return np.tile(wav, repeat_times)

    def write_wave(self, wav, file_path):
        with wave.open(file_path, 'wb') as f:
            f.setnchannels(1)
            f.setsampwidth(1)
            f.setframerate(self.sample_rate)
            f.writeframes(wav.tobytes())


# 旋律类
class Melody8bit:
    def __init__(self):
        # 十二平均律
        self.pitch_dict = {'C1': 32.70, 'D1': 36.71, 'E1': 41.20, 'F1': 43.65, 'G1': 48.99, 'A1': 55.00,
                           'B1': 61.74, 'C2': 65.41, 'D2': 73.42, 'E2': 82.41, 'F2': 87.31, 'G2': 97.99,
                           'A2': 110.00, 'B2': 123.47, 'C3': 130.81, 'D3': 146.83, 'E3': 164.81, 'F3': 174.61,
                           'G3': 196.00, 'A3': 220.00, 'B3': 246.94, 'C4': 261.63, 'D4': 293.66, 'E4': 329.63,
                           'F4': 349.23, 'G4': 392.00, 'A4': 440.00, 'B4': 493.88, 'C5': 523.25, 'D5': 587.33,
                           'E5': 659.26, 'F5': 698.46, 'G5': 783.99, 'A5': 880.00, 'B5': 987.77, 'C6': 1046.50,
                           'D6': 1174.66, 'E6': 1318.51, 'F6': 1396.91, 'G6': 1567.98, 'A6': 1760.00, 'B6': 1975.53,
                           'C7': 2093.00, 'D7': 2349.32, 'E7': 2637.02, 'F7': 2793.83, 'G7': 3135.96, 'A7': 3520.00,
                           'B7': 3951.07, '#C1': 34.65, '#D1': 39.20, '#F1': 46.25, '#G1': 52.00, '#A1': 58.27,
                           '#C2': 69.30, '#D2': 78.39, '#F2': 92.50, '#G2': 103.83, '#A2': 116.54, '#C3': 138.59,
                           '#D3': 155.56, '#F3': 185.00, '#G3': 207.65, '#A3': 233.08, '#C4': 277.18, '#D4': 311.13,
                           '#F4': 369.99, '#G4': 415.30, '#A4': 466.16, '#C5': 554.37, '#D5': 622.25, '#F5': 739.99,
                           '#G5': 830.61, '#A5': 932.33, '#C6': 1108.73, '#D6': 1244.51, '#F6': 1479.98, '#G6': 1661.22,
                           '#A6': 1864.66, '#C7': 2217.46, '#D7': 2489.02, '#F7': 2959.96, '#G7': 3322.44,
                           '#A7': 3729.31,
                           'O': 0.0}

        # 音名的音阶关系 方便计算用
        self.pitch_scale = {'C': 0, '#C': 1, 'D': 2, '#D': 3, 'E': 4, 'F': 5,
                            '#F': 6, 'G': 7, '#G': 8, 'A': 9, '#A': 10, 'B': 11}
        self.scale_pitch = {0: 'C', 1: '#C', 2: 'D', 3: '#D', 4: 'E', 5: 'F',
                            6: '#F', 7: 'G', 8: '#G', 9: 'A', 10: '#A', 11: 'B'}

    # 音名计算
    def cal_pitch(self, in_pitch, method):
        """
        method example:
            '+maj3' 加三大度
            '-min3' 减三小度
            '-semi5' 减五个半音
        """
        method_scale_dict = {'maj3': 4, 'min3': 3,
                             'semi1': 1, 'semi2': 2, 'semi3': 3, 'semi4': 4, 'semi5': 5, 'semi6': 6, 'semi7': 7,
                             'semi8': 8, 'semi9': 9, 'semi10': 10, 'semi11': 11, 'semi12': 12}
        if method[0] not in ['+', '-']:
            raise ValueError("method example: '+maj3', '-semi5'")
        method_start = method[0]
        method_scale = method[1:]
        if method_scale not in method_scale_dict.keys():
            raise ValueError(f"Unknown scale: {method_scale}, should be one of {method_scale_dict.keys()}")
        if in_pitch in self.pitch_scale.keys():
            base_pitch = in_pitch
            base_pitch_scale = self.pitch_scale[base_pitch]
            if method_start == '+':
                new_pitch_scale = (base_pitch_scale + method_scale_dict[method_scale]) % 12
            else:
                new_pitch_scale = (base_pitch_scale - method_scale_dict[method_scale]) % 12
            return self.scale_pitch[new_pitch_scale]
        elif in_pitch in self.pitch_dict.keys():
            n = int(in_pitch[-1])
            base_pitch = in_pitch[:-1]
            base_pitch_scale = self.pitch_scale[base_pitch]
            if method_start == '+':
                new_pitch_scale = (base_pitch_scale + method_scale_dict[method_scale]) % 12
                n_add = (base_pitch_scale + method_scale_dict[method_scale]) // 12
            else:
                new_pitch_scale = (base_pitch_scale - method_scale_dict[method_scale]) % 12
                n_add = (base_pitch_scale - method_scale_dict[method_scale]) // 12
            new_pitch = self.scale_pitch[new_pitch_scale] + str(n + n_add)
            return new_pitch
        else:
            raise ValueError(f"Unknown pitch: {in_pitch}, should be one of "
                             f"{self.pitch_dict.keys()} or {self.pitch_scale.keys()}")


# 吉他
class Guitar8bit(Rhythm8bit):
    def __init__(self, bpm):
        super().__init__(bpm)
        self.instrument_duration = 0.1  # seconds
        self.amplitude = 16
        # 特殊技法：延音、颤音、滑音、三和弦、三和弦琶音
        self.performances = {'pr': 'prolong 延音',
                             'tr': 'trill 颤音',
                             'sl': 'slide 滑音',
                             'maj-chord': 'major triad 大三和弦',
                             'maj-arpeggio': 'major triad arpeggio 大三和弦琶音',
                             'min-chord': 'minor triad 小三和弦',
                             'min-arpeggio': 'minor triad arpeggio 小三和弦琶音',
                             'dim-chord': 'diminished triad 减三和弦',
                             'dim-arpeggio': 'diminished triad arpeggio 减三和弦琶音',
                             'aug-chord': 'augmented triad 增三和弦',
                             'aug-arpeggio': 'augmented triad arpeggio 增三和弦琶音',
                             }
        self.melody = Melody8bit()
        self.pitch_dict = self.melody.pitch_dict

    def gen_timbre_wave(self, pitch, duration):
        frequency = self.pitch_dict[pitch]
        return gen_square_wave(frequency, self.amplitude, duration, self.sample_rate)

    def gen_prolong_wave(self, pitch, one_score_sample_count):
        one_score_duration = one_score_sample_count / self.sample_rate
        prolong_duration = one_score_duration * 0.9
        wav = self.gen_timbre_wave(pitch, prolong_duration)
        return regularize_wave(wav, one_score_sample_count)

    def gen_trill_wave(self, pitch, one_score_sample_count):
        trill_blank_duration = 0.01
        instrument_duration = self.instrument_duration * 0.8
        wav1 = self.gen_timbre_wave(pitch, instrument_duration)
        trill_blank_sample_count = int(round(trill_blank_duration * self.sample_rate))
        wav2 = gen_zero_wave(trill_blank_sample_count)
        wav_one_trill = np.concatenate([wav1, wav2])
        trill_count = int(one_score_sample_count / len(wav_one_trill))
        return np.tile(wav_one_trill, trill_count)

    def gen_slide_wave(self, pitch, one_score_sample_count):
        one_score_duration = one_score_sample_count / self.sample_rate
        return self.gen_timbre_wave(pitch, one_score_duration)

    def get_chord_pitch(self, pitch, chord_type):
        if chord_type == 'maj':
            # 根音、三音（大三度）、五音（小三度）
            third_pitch = self.melody.cal_pitch(pitch, '+maj3')
            fifth_pitch = self.melody.cal_pitch(third_pitch, '+min3')
            return pitch, third_pitch, fifth_pitch
        elif chord_type == 'min':
            # 根音、三音（小三度）、五音（大三度）
            third_pitch = self.melody.cal_pitch(pitch, '+min3')
            fifth_pitch = self.melody.cal_pitch(third_pitch, '+maj3')
            return pitch, third_pitch, fifth_pitch
        elif chord_type == 'dim':
            # 根音、三音（小三度）、五音（小三度）
            third_pitch = self.melody.cal_pitch(pitch, '+min3')
            fifth_pitch = self.melody.cal_pitch(third_pitch, '+min3')
            return pitch, third_pitch, fifth_pitch
        elif chord_type == 'aug':
            # 根音、三音（大三度）、五音（大三度）
            third_pitch = self.melody.cal_pitch(pitch, '+maj3')
            fifth_pitch = self.melody.cal_pitch(third_pitch, '+maj3')
            return pitch, third_pitch, fifth_pitch

    def gen_chord_wave(self, root_pitch, third_pitch, fifth_pitch, one_score_sample_count):
        wav1 = self.gen_prolong_wave(root_pitch, one_score_sample_count)
        wav2 = self.gen_prolong_wave(third_pitch, one_score_sample_count)
        wav3 = self.gen_prolong_wave(fifth_pitch, one_score_sample_count)
        wav = wav1 + wav2 + wav3
        return wav

    def gen_arpeggio_wave(self, root_pitch, third_pitch, fifth_pitch, one_score_sample_count):
        blank_duration = 0.01
        blank_sample_count = int(round(blank_duration * self.sample_rate))
        instrument_duration = 0.1
        root_pitch_high = self.melody.cal_pitch(root_pitch, '+semi12')
        wav_root = self.gen_timbre_wave(root_pitch, instrument_duration)
        wav_third = self.gen_timbre_wave(third_pitch, instrument_duration)
        wav_fifth = self.gen_timbre_wave(fifth_pitch, instrument_duration)
        wav_root_high = self.gen_timbre_wave(root_pitch_high, instrument_duration)
        wav_blank = gen_zero_wave(blank_sample_count)
        return np.concatenate([wav_root, wav_blank, wav_third, wav_blank, wav_fifth, wav_blank, wav_root_high])

    def gen_instrument_technique_wave(self, pitch, one_score_sample_count, technique):
        if technique not in self.performances.keys():
            raise ValueError(f'Unknown technique: {technique}, should be one of {self.performances.keys()}')
        if '-' not in technique:
            if technique == 'pr':
                return self.gen_prolong_wave(pitch, one_score_sample_count)
            elif technique == 'tr':
                return self.gen_trill_wave(pitch, one_score_sample_count)
            elif technique == 'sl':
                return self.gen_slide_wave(pitch, one_score_sample_count)
        else:
            techniques = technique.split('-')
            chord_type = techniques[0]
            perform_type = techniques[1]
            root_pitch, third_pitch, fifth_pitch = self.get_chord_pitch(pitch, chord_type)
            if perform_type == 'chord':
                return self.gen_chord_wave(root_pitch, third_pitch, fifth_pitch, one_score_sample_count)
            elif perform_type == 'arpeggio':
                return self.gen_arpeggio_wave(root_pitch, third_pitch, fifth_pitch, one_score_sample_count)


# 贝司音色波形
class Bass8bit(Guitar8bit):
    def __init__(self, bpm):
        super().__init__(bpm)
        self.amplitude = 32

    def gen_timbre_wave(self, pitch, duration):
        frequency = self.pitch_dict[pitch]
        return gen_triangle_wave(frequency, self.amplitude, duration, self.sample_rate)


# 架子鼓音色波形
class Drum8bit(Rhythm8bit):
    def __init__(self, bpm):
        super().__init__(bpm)
        self.amplitude = 16
        self.instrument_duration = 0.1  # seconds
        self.pitch_dict = {'X': 0.0, 'O': 0.0}
        self.performances = {'triple': 'triple beat 三连音',
                             'hi-hat': 'hi-hat 镲音'}

    def gen_timbre_wave(self, pitch, duration):
        if pitch == 'X':
            return gen_noise_wave(self.amplitude, duration, self.sample_rate)

    def gen_triple_wave(self, pitch, one_score_sample_count):
        zero_duration = 0.01
        zero_sample_count = int(round(zero_duration * self.sample_rate))
        wav1 = self.gen_timbre_wave(pitch, self.instrument_duration)
        wav2 = gen_zero_wave(zero_sample_count)
        wav = np.concatenate([wav1, wav2])
        return np.tile(wav, 3)

    def gen_hi_hat_wave(self, pitch, one_score_sample_count):
        instrument_duration = 0.02
        return self.gen_timbre_wave(pitch, instrument_duration)

    def gen_instrument_technique_wave(self, pitch, one_score_sample_count, technique):
        if technique not in self.performances.keys():
            raise ValueError(f'Unknown technique: {technique}, should be one of {self.performances.keys()}')

        if technique == 'triple':
            return self.gen_triple_wave(pitch, one_score_sample_count)
        elif technique == 'hi-hat':
            return self.gen_hi_hat_wave(pitch, one_score_sample_count)


class Band8bit:
    def __init__(self, bpm, one_beat_note='quarter'):
        self.bpm = bpm
        self.one_beat_note = one_beat_note

        self.guitar1 = Guitar8bit(bpm)
        self.guitar2 = Guitar8bit(bpm)
        self.bass = Bass8bit(bpm)
        self.drum = Drum8bit(bpm)


class MelodyAssist8bit(Melody8bit):
    def __init__(self):
        super().__init__()
        self.tonic_chords = ['1-maj', '6-min']
        self.dominant_chords = ['5-maj', '3-min', '7-dim']
        self.subdominant_chords = ['2-min', '4-maj']
        self.chord_func_dict = {'T': self.tonic_chords, 'D': self.dominant_chords, 'S': self.subdominant_chords}

        self.popular_chord_progression_types = ['T-S-D-T', 'S-D-D-T-S-D-T-T', 'T-D-T-D-S-T-S-T']

    # 根据给定调性生成自然音音名
    def get_natural_pitches(self, tonality):
        """
        mode example:
         'C-maj': C major C大调
         'A-min': a minor a小调
         '#F-maj': #F major #F大调
        """
        pitch_list = []

        tonality = tonality.split('-')
        if len(tonality) != 2:
            raise ValueError("mode example: 'C-maj', 'A-min', '#F-maj'")
        base_pitch = tonality[0]
        mode = tonality[1]
        if base_pitch not in self.pitch_scale.keys():
            raise ValueError("mode example: 'C-maj', 'A-min', '#F-maj'")
        if mode not in ['maj', 'min']:
            raise ValueError("mode example: 'C-maj', 'A-min', '#F-maj'")
        scales = []
        if mode == 'maj':
            # 大调 全全半全全全半
            scales = [0, 2, 2, 1, 2, 2, 2, 1]
        elif mode == 'min':
            # 小调 全半全全半全全
            scales = [0, 2, 1, 2, 2, 1, 2, 2]
        pitch_scale = self.pitch_scale[base_pitch]
        for scale in scales:
            pitch_scale += scale
            pitch_list.append(self.scale_pitch[pitch_scale % 12])
        return pitch_list

    # 根据给定调性和和弦类型生成和弦进行
    def gen_chord_progression(self, tonality, chord_progression_type):
        chords = chord_progression_type.split('-')
        for chord in chords:
            pass