import os
import wave
import librosa
from IPython.display import Audio, display
import matplotlib.pyplot as plt
import numpy as np
from playsound import playsound
import librosa.display



def func(function, *argv):
    for arg in argv:
        print(arg)
    wav_path = argv[0]
    wav_file = get_data(wav_path)  # wczytaj plik
    data = argv[1]

    function(wav_file, data)
    save_wave(wav_file, wav_path)


class WaveFile:
    def __init__(self, n_channels, n_samples, n_sampwidth, framerate, t_audio, frames):
        self.n_channels = n_channels
        self.n_samples = n_samples
        self.n_sampwidth = n_sampwidth
        self.framerate = framerate
        self.t_audio = t_audio
        self.frames = frames

    def print(self):
        print("Number of channels :", self.n_channels)
        print("Number of frames :", self.n_samples)
        print("Sample Width: ", self.n_sampwidth)
        print("Frame Rate :", self.framerate)
        print("Audio Time :", self.t_audio)


def get_data(wavepath):
    # Funkcja która pobiera potrzebne dane z pliku .wav
    obj = wave.open(wavepath, "rb")
    number_of_channels = obj.getnchannels()
    n_samples = obj.getnframes()
    n_sampwidth = obj.getsampwidth()
    sample_freq = obj.getframerate()
    signal_wave = obj.readframes(-1)

    obj.close()

    t_audio = n_samples/sample_freq

    # Converting signal wave to immutable array of audio signal
    signal_array = np.frombuffer(signal_wave, dtype=np.int16)

    # Converting immutable array of audio signal to mutable array of audio signal
    # this array can be modified to achieve different effects

    signal_array_mut = np.array(signal_array)
    wav = WaveFile(number_of_channels, n_samples, n_sampwidth, sample_freq, t_audio, signal_array_mut)
    return wav


def save_wave(wav_file, filename):
    # Funkcja która zapisuje plik .wav pod podaną nazwę
    obj = wave.open(filename, "wb")
    save_data(wav_file, obj)
    obj.close()


def save_data(wav_file, obj):
    # Funkcja która zapisuje dane do nowego pliku .wav
    obj.setnchannels(wav_file.n_channels)
    obj.setsampwidth(wav_file.n_sampwidth)
    obj.setframerate(wav_file.framerate)
    obj.writeframes(wav_file.frames)


def amp(wav_file, data):
    # Ta funkcja wzmacnia sygnał o wartość podaną przez użytkownika w prcentach
    amplify_ratio = data
    for i in range(0, len(wav_file.frames)-1):
        wav_file.frames[i] = (amplify_ratio/100) * wav_file.frames[i]
    return wav_file


def echo(wav_file, data):
    print('echo')
    delay=data['delay']
    decay_ratio=data['decay']
    # Ta funkcja realizuje efekt echa
    print("Delay ms : ", delay)
    print('Decay_ratio: ', decay_ratio)
    # Converting delay time to index by multiplying the delay by the sample frequency
    delay_index = int(delay*wav_file.framerate)
    for i in range(0, len(wav_file.frames) - 1):
        if (i + delay_index) < (len(wav_file.frames) - 1):
            wav_file.frames[i + delay_index] = wav_file.frames[i] * decay_ratio + wav_file.frames[i + delay_index]
    return wav_file


def rev(wav_file, data):
    print('rev')
    temp = np.copy(wav_file.frames)
    for i in range(0, len(wav_file.frames)-1):
        wav_file.frames[i] = temp[len(wav_file.frames)-1-i]
    return wav_file


def low_pass(wav_file, data):
    print('low_pass')
    cutoff_freq = data
    # Ta funkcja realizuje filtr dolnoprzepustowy
    input_signal = np.copy(wav_file.frames)
    filter_output = np.zeros_like(input_signal)

    dn_1 = 0
    for n in range(input_signal.shape[0]):
        break_frequency = cutoff_freq

        tan = np.tan(np.pi * float(break_frequency/wav_file.framerate))
        a1 = (tan-1) / (tan + 1)

        filter_output[n] = float(a1 * input_signal[n] + dn_1)
        dn_1 = float(input_signal[n] - a1 * filter_output[n])

    lowpass_output = input_signal + filter_output
    for i in range(0, len(lowpass_output)):
        lowpass_output[i] *= 0.5
    wav_file.frames = lowpass_output
    return wav_file


def high_pass(wav_file, data):
    print('high_pass')
    cutoff_freq = data
    # Ten efekt realizuje filtr górnoprzepustowy
    input_signal = np.copy(wav_file.frames)
    filter_output = np.zeros_like(input_signal)

    dn_1 = 0
    for n in range(input_signal.shape[0]):
        break_frequency = cutoff_freq
        tan = np.tan(np.pi * float(break_frequency / wav_file.framerate))
        a1 = (tan - 1) / (tan + 1)
        filter_output[n] = float(a1 * input_signal[n] + dn_1)
        dn_1 = float(input_signal[n] - a1 * filter_output[n])

    for i in range(0, len(filter_output)):
        filter_output[i] *= -1

    lowpass_output = input_signal + filter_output

    for i in range(0, len(lowpass_output)):
        lowpass_output[i] *= 0.5

    wav_file.frames = lowpass_output
    return wav_file


def repeat(wav_file, data):
    print('repeat')
    n_repeat = data
    wav_file.n_samples = n_repeat * wav_file.n_samples
    wav_file.t_audio = wav_file.n_samples/wav_file.framerate
    single_sound = np.copy(wav_file.frames)
    for i in range(0, n_repeat-1):
        wav_file.frames = np.append(wav_file.frames, single_sound)
    return wav_file


# def play_audio(wavepath=None):
#     # Funkcja która odtwarza wybrany plik .wav
#     if wavepath == None:
#         wavepath = input("Podaj nazwę pliku .wav : ")
#
#     abs_path = os.path.abspath(wavepath)
#     print(abs_path)
#     playsound(abs_path)


# def open_wave(wavepath=None):
#     # Funkcja która otwiera plik wave wybrany przez użytkownika
#     #file = WaveFile()
#     if wavepath == None:
#         wavepath = input("Podaj ścieżkę do pliku .wav : ")
#
#     abs_path = os.path.abspath(wavepath)
#     opened_wav = get_data(abs_path)
#     return opened_wav