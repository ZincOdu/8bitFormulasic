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
