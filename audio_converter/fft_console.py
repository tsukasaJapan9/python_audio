import numpy as np
import pyaudio
from image import ImageConsole
from numpy import int16, empty
import pygame
import time
from kbhit import KBHit

class Sound:
    def __init__(self, pg, sound_name, amp_thres, freq_min_thres, freq_max_thres):
        self._pg = pg
        self._sound_name = sound_name
        self._sound = self._pg.mixer.Sound(self._sound_name)
        self._amp_thres = amp_thres
        self._freq_min_thres = freq_min_thres
        self._freq_max_thres = freq_max_thres
        self._play_flag = False

    def play(self, amp, freq):
        if amp < self._amp_thres: return
        if freq < self._freq_min_thres or self._freq_max_thres < freq: return

        self._sound.play()

class AudioConverter:
    # 入力音パラメータ
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    # スペクトル画像
    image = ImageConsole()

    # 描画用
    MAX_X = 80
    MAX_Y = 25
    AMP_THRES = 20000

    # どの程度FFTを細かく行うか
    FFT_LEN = MAX_X * 2
    CHUNK = FFT_LEN

    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format = self.FORMAT,
                                      channels = self.CHANNELS,
                                      rate = self.RATE,
                                      input = True,
                                      output = False,
                                      frames_per_buffer = self.CHUNK)

        self.data = empty(self.FFT_LEN, dtype=int16)
        self.freqlist = np.fft.fftfreq(self.FFT_LEN, d=1.0/self.RATE)
        self.hammingWindow = np.hamming(self.FFT_LEN)

        self.kick = Sound(pygame, "kick.wav", 25, 5, 10)
        self.snare = Sound(pygame, "snare.wav", 25, 50, 60)

    def mapping(self, value):
        v = value
        if self.AMP_THRES < v:
            v = self.AMP_THRES
        elif v < 0:
            v = 0
        v = v * (self.MAX_Y / self.AMP_THRES)
        return int(v)

    def loop(self):
        try:
            while True :
                self.data = self.audioinput()
                windata = self.hammingWindow * self.data

                f = np.fft.fft(windata)
                amplitude = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in f]

                self.image.clear()
                for i in range(self.MAX_X):
                    amp = amplitude[i]
                    plot_y = self.mapping(amp)

                    for j in range(plot_y):
                        self.image.set_pixel(i, self.MAX_Y - j - 1, 1)

                for i in range(self.MAX_X):
                    amp = amplitude[i]
                    plot_y = self.mapping(amp)

                    self.kick.play(plot_y, i)
                    self.snare.play(plot_y, i)

                self.image.show()

        except KeyboardInterrupt:
            print("End")
            pass

    def audioinput(self):
        frame = self.stream.read(self.CHUNK)
        frame = np.fromstring(frame, dtype=int16)
        return frame

    def fft(self):
        pass

if __name__ == "__main__":
    kb = KBHit()

    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    pygame.mixer.init()

    pygame.mixer.set_num_channels(1)

    # kick = Sound(pygame, "kick.wav")
    # snare = Sound(pygame, "snare.wav")
    #
    # while True:
    #     if kb.kbhit():
    #         c = ord(kb.getch())
    #         if c == 97:
    #             print("kick")
    #             kick.play()
    #         if c == 108:
    #             print("snare")
    #             snare.play()
    #         elif c == 27:
    #             break

    sa = AudioConverter()
    sa.loop()
