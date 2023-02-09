import os
import random
import sys

import threading
from typing import List
from PySide6.QtCore import Qt, Slot, QTimer
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QVBoxLayout,
                               QHBoxLayout, QGroupBox, QWidget, QProgressBar, QSlider)
import numpy as np
import pyaudio as pa

path=""

def load(f):
    with open(f"src/numpy/filter{f}.np",'rb') as i_f:
        return np.load(i_f)

filters = [load(i) for i in range(10)]


class EqualiserWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.freqs = np.array([32,64,128,256,512,1000,2000,4000,8000,16000])
        self.sliders = [
            QSlider(
                Qt.Orientation.Vertical,
                self
            )
            for f in self.freqs
        ]
        self.labels = []

        self.layout = QHBoxLayout(self)
        for slider,f in zip(self.sliders,self.freqs):
            parent = self
            class Vgroup(QGroupBox):
                def __init__(self):
                    super().__init__(f"{f}hz",parent)
                    self.layout = QHBoxLayout(self)
                    slider.setTickPosition(QSlider.TickPosition.TicksLeft)
                    slider.setTickInterval(5)
                    slider.setMaximum(12)
                    slider.setMinimum(-12)

                    thislabel = QLabel("0dB", slider)

                    def genCallback(slider,thislabel):
                        @Slot()
                        def callback():
                            thislabel.setText(f"{slider.value()}dB")
                            f = sum([
                                f*(10**(slider.value()/20))
                                for f,slider in zip(filters,parent.sliders)
                            ])
                            with open(path,'wb') as o_f:
                                o_f.write(f.astype(np.float32).tobytes())
                        return callback

                    slider.callback = genCallback(slider,thislabel)

                    slider.valueChanged.connect(slider.callback)

                    parent.labels.append(
                        thislabel
                    )

                    self.layout.addWidget(parent.labels[-1])

                    self.layout.addWidget(slider)
            self.layout.addWidget(Vgroup())

SR = 44100
centres = np.array([32,64,128,256,512,1000,2000,4000,8000,16000])
cutoffs = (centres[1:]+centres[:-1])/2
cutoffs = np.concatenate(([0],cutoffs,[44100/2]))

def freq_to_i(f,n):
    return int((2*f/SR)*n)

bars:List[QProgressBar] = []

import datetime
vals = np.zeros((10),int)

FRAMERATE = 25
interval =  datetime.timedelta(seconds=1/FRAMERATE)
last = datetime.datetime.now()

def audiohandler(samples, n, time_info, status):
    global vals,last
    now = datetime.datetime.now()
    if (now-last)>interval:
        last=now
        samples = np.ndarray((n),np.float32,samples)
        transform = np.abs(np.fft.rfft(samples))
        s=transform.sum()
        transform = transform/(s if s!=0 else 1)
        for f0,f1,i in zip(cutoffs[:-1],cutoffs[1:],range(10)):
            vals[i]=(int(
                100*(-np.log(.1)+np.log(.1+transform[
                    freq_to_i(f0,n):
                    freq_to_i(f1,n)
                ].sum()))/(np.log(1.1)-np.log(.1))
            ))
        return (b'', pa.paContinue)
p = pa.PyAudio()

stream = p.open(
    SR,1,
    pa.paFloat32,
    True,
    frames_per_buffer=4096
)

class BarWidget(QWidget):
    @Slot()
    def updateaudio(self):
        audiohandler(stream.read(4096),4096,0,0)
        try:
            for v,bar in zip(vals,bars):
                bar.setValue(int(v))
        except:
            pass
    def __init__(self):
        global bars
        QWidget.__init__(self)

        timer = QTimer(self)
        timer.timeout.connect(self.updateaudio)
        timer.start(30)

        self.layout = QHBoxLayout(self)

        bars = [
            QProgressBar(self)
            for _ in range(10)
        ]

        stream.start_stream()

        for bar in bars:
            bar.setOrientation(Qt.Orientation.Vertical)
            self.layout.addWidget(bar)

class FullWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout=QVBoxLayout(self)
        self.layout.addWidget(BarWidget())
        self.layout.addWidget(EqualiserWidget())

if __name__ == "__main__":
    try:
        path = os.environ["PSM_PIPE"]
    except:
        raise LookupError("Could not look up environment variable «PSM_PIPE».")
    if not os.path.exists(path):
        raise LookupError("Pipe doesn't exist. Please start the filtering host.")
    
    app = QApplication(sys.argv)

    widget = FullWidget()
    widget.show()

    app.exec_()
    stream.close()
    p.terminate()