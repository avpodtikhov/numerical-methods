#!/usr/local/bin/python3
from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
import random
import math

def gaussian(x, mu, sigma):
    return math.exp(-0.5*((x-mu)/sigma)**2) / sigma / math.sqrt(2*math.pi)

class GraphicsWindow(QDialog):
    def __init__(self, parent=None):
        super(GraphicsWindow, self).__init__(parent)

        self.figure = plt.figure()
        self.figure.subplots_adjust(top=0.95,bottom=0.105,left=0.105,right=0.93,hspace=0.43,wspace=0.32)        
        self.canvas = FigureCanvas(self.figure)
        self.button = QPushButton('Обновить графики')
        self.button.clicked.connect(self.plot)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.plot()
        self.setWindowTitle('Графики')
        self.setFixedSize(800, 800)

    def plot(self):
        data = [random.random() for i in range(10)]
        self.figure.clear()
        ax1 = self.figure.add_subplot(221, xlabel='t', ylabel='показы')
        ax2 = self.figure.add_subplot(222, xlabel='t', ylabel='S(t) - x(t)')
        ax3 = self.figure.add_subplot(224, xlabel='w', ylabel='p(w)')
        ax4 = self.figure.add_subplot(223, xlabel='x', ylabel='S')
        w = np.arange(0, 10.5, 0.5)
        t = np.arange(0, 1, 0.01)
        s = 3*t + np.sin(t)
        x = t * 3.84147098481
        sx = 3 * (x/3.84147098481) + np.sin(x / 3.84147098481)
        diftx = s - x
        z = 4*t + np.cos(t)
        p = [gaussian(x, 5, 2) for x in w]
        ax1.plot(t, s, label='S(t)')
        ax1.plot(t,x, label='x(t)')
        ax2.plot(t, diftx)
        ax3.plot(w, p, label ='p(w)')
        ax3.vlines(6, 0, p[12], linestyles='--', label='y(t)')
        x1 = np.arange(6, 10.5, 0.5)
        zer = np.zeros(len(p))
        ax3.fill_between(x1, y1=p[12:], y2=zer[12:], where=p[12:] >zer[12:], alpha=0.5)
        ax1.plot(t, z, label='z(t)')
        ax4.plot(x, sx, label='S(x)')
        ax1.legend()
        ax2.legend()
        ax3.legend()
        ax4.legend()
        self.canvas.draw()
