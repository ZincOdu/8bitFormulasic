import numpy as np
def gen_square_wave(frequency, amplitude, duration, sample_rate):
    """
    amplitude: 0-255
    return an uint8 array of square wave
    """
    num_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, num_samples, endpoint=False)
    square_wave = np.where(np.mod(frequency * t, 1) < 0.5, amplitude, 0)
    square_wave = np.uint8(square_wave)
    return square_wave


def gen_triangle_wave(frequency, amplitude, duration, sample_rate):
    """
    amplitude: 0-255
    return an uint8 array of triangle wave
    """
    num_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, num_samples, endpoint=False)
    triangle_wave = np.abs(np.mod(frequency * t, 1) - 0.5) * 2 * amplitude
    triangle_wave = np.uint8(triangle_wave)
    return triangle_wave


def gen_zero_wave(num_samples):
    """
    return an uint8 array of zero wave
    """
    zero_wave = np.zeros(num_samples, dtype=np.uint8)
    return zero_wave


def gen_noise_wave(amplitude, duration, sample_rate):
    """
    return an uint8 array of noise wave
    """
    num_samples = int(duration * sample_rate)
    noise_wave = np.random.randint(0, amplitude, num_samples, dtype=np.uint8)
    return noise_wave


def regularize_wave(wav, num_samples):
    if len(wav) < num_samples:
        zero_sample_count = num_samples - len(wav)
        wav = np.concatenate([wav, gen_zero_wave(zero_sample_count)])
    elif len(wav) > num_samples:
        wav = wav[:num_samples]
    return wav
