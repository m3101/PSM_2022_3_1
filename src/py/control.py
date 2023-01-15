import os
import random
import sys

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton,
                               QHBoxLayout, QGroupBox, QWidget, QSlider)
import numpy as np

path=""

def load(f):
    with open(f"src/numpy/filter{f}.np",'rb') as i_f:
        return np.load(i_f)

filters = [load(i) for i in range(10)]
print(filters)


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
                    slider.setMaximum(50)
                    slider.setMinimum(-50)

                    thislabel = QLabel("0dB", slider)

                    def genCallback(slider,thislabel):
                        @Slot()
                        def callback():
                            thislabel.setText(f"{slider.value()}dB")
                            f = sum([
                                f*np.exp(slider.value()/20)
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


if __name__ == "__main__":

    try:
        path = os.environ["PSM_PIPE"]
    except:
        raise LookupError("Could not look up environment variable «PSM_PIPE».")
    if not os.path.exists(path):
        raise LookupError("Pipe doesn't exist. Please start the filtering host.")

    app = QApplication(sys.argv)

    widget = EqualiserWidget()
    widget.show()

    sys.exit(app.exec_())