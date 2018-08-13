import numpy as np
import pyaudio
from image import ImageConsole
from numpy import int16, empty

class AudioAnalyzer:
    # 入力データ
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    # 描画用
    MAX_X = 80
    MAX_Y = 25

    # どの程度FFTを細かく行うか
    FFT_LEN = MAX_X * 2
    CHUNK = FFT_LEN

    AMP_THRES = 20000

    image = ImageConsole()

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
    sa = AudioAnalyzer()
    sa.loop()
