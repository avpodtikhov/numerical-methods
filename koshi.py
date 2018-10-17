#!/usr/local/bin/python3
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
        QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget, QFileDialog, QLabel, QLineEdit, QHBoxLayout, QDialog, QMessageBox)
import pandas as pd
import numpy as np
import difeq

class KoshiWindow(QDialog):

    def __init__(self, parent=None, mode = None, sDir = None, zDir = None, uDir = None, f = None):
        super(KoshiWindow, self).__init__(parent)
        self.le81 = None
        self.mode = mode
        self.sDir = sDir
        self.zDir = zDir
        self.uDir = uDir
        self.f = f
        self.buttonSolve = QPushButton('Решить')
        self.buttonSolve.clicked.connect(self.solve)
        self.buttonSolve.setEnabled(False)
        
        grid = QGridLayout()
        grid.addWidget(self.data(), 0, 0)
        grid.addWidget(self.buttonSolve, 1, 0, 1, -1)
        self.setLayout(grid)
        self.setWindowTitle("Табуляция функции: ")
        self.setFixedSize(320, 400)
    
    def solve(self):
        self.difeq = difeq.DifEqWindow(self, 'x', self.uDir, 'y', self.sDir, self.x0, self.y0)
        self.difeq.show()

    def data(self):
        groupbox1 = QGroupBox('Данные')
        grid = QGridLayout()
        if (self.mode == 0):
            l1 = QLabel('Ручной режим')
            l8 = QLabel('b = ')
            self.le8 = QLineEdit('0')
            grid.addWidget(l8, 2, 0)
            grid.addWidget(self.le8, 2, 1, 1, -1)
        else:
            l1 = QLabel('Автоматический режим')
            l8 = QLabel('Диапозон b: ')
            self.le8 = QLineEdit('0')
            self.le81 = QLineEdit('1')
            l81 = QLabel(', ')
            grid.addWidget(l8, 2, 0)
            grid.addWidget(self.le8, 2, 1)
            grid.addWidget(l81, 2, 2)
            grid.addWidget(self.le81, 2, 3)
        first = self.sDir[:self.sDir.rfind('/')]
        func = first[first.rfind('/'):]
        l2 = QLabel('S(t) : ...' + func + self.sDir[self.sDir.rfind('/') : ])
        first = self.zDir[:self.zDir.rfind('/')]
        func = first[first.rfind('/'):]
        l3 = QLabel('z(t) : ...' + func + self.zDir[self.zDir.rfind('/') : ])
        first = self.uDir[:self.uDir.rfind('/')]
        func = first[first.rfind('/'):]
        l4 = QLabel('U(y) : ...' + func + self.uDir[self.uDir.rfind('/') : ])
        l5 = QLabel('f(z,x,s,b) = ' + self.f)
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop)
        vbox.addWidget(l1)
        vbox.addWidget(l2)
        vbox.addWidget(l3)
        vbox.addWidget(l4)
        vbox.addWidget(l5)
        groupbox1.setLayout(vbox)

        groupbox2 = QGroupBox('Параметры')
        l6 = QLabel('X_0 = ')
        self.le6 = QLineEdit('0')
        l7 = QLabel('Y_0 = ')
        self.le7 = QLineEdit('0')

        button = QPushButton('Сохранить')
        button.clicked.connect(self.saveParam)
        grid.addWidget(l6, 0 , 0)
        grid.addWidget(self.le6, 0 , 1, 1, -1)
        grid.addWidget(l7, 1 , 0)
        grid.addWidget(self.le7, 1 , 1, 1, -1)
        grid.addWidget(button, 3 , 0, 1, -1)
        groupbox2.setLayout(grid)
        
        groupbox = QGroupBox()
        vbox = QVBoxLayout()
        vbox.addWidget(groupbox1)
        vbox.addWidget(groupbox2)
        groupbox.setLayout(vbox)
        return groupbox

    def saveParam(self):
        try:
            self.x0 = float(self.le6.text())
            self.y0 = float(self.le7.text())
            self.bmin = float(self.le8.text())
            if (self.le81 == None):
                self.bmax = float(self.le8.text())
            else:
                self.bmax = float(self.le81.text())
            self.showMessageBox('Успешно', 'Параметры установлены')
            self.buttonSolve.setEnabled(True)
        except:
            self.showMessageBox('Ошибка', 'Неверные типы параметров.\n Допустимый тип: float')

    def showMessageBox(self, title, message):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        button = msg.addButton('ОК', QMessageBox.AcceptRole)
        msg.exec_()
        msg.deleteLater()
