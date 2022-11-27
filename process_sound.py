import os
import wave
import librosa
from IPython.display import Audio, display
import matplotlib.pyplot as plt
import numpy as np
from playsound import playsound
import librosa.display


processing_folder = os.path.join("static", "files/")


def func(function, *argv):
    for arg in argv:
        print(arg)
    filename = argv[0]
    wav_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), processing_folder, filename)
    wav_file = get_data(wav_path)  # wczytaj plik
    data = argv[1]

    function(wav_file, data)
    save_wave(wav_file, processing_folder + filename)


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
    print('get data')
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


def reverse(wav_file, data):
    # ta funkcja odwraca wybrany dźwięk
    wav_file.frames = wav_file.frames[::-1]
    return wav_file


# def echo(filename, data):
#     print('echo')
#     delay=data['delay']
#     decay=data['decay']
#     file = open(processing_folder + filename, 'a')
#     # funkcja coś robi
#     file.write(f'echo {delay}, {decay}\n')
#     # koniec akcji funkcji - zamykam plik #
#     file.close()


# # noinspection GrazieInspection
# def amp(filename, data):
#     print('amplification')
#     amplitude = data
#     file = open(processing_folder + filename, 'a')
#     # funkcja coś robi
#     file.write(f'amp {amplitude} \n')
#     # koniec akcji funkcji - zamykam plik #
#     file.close()


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