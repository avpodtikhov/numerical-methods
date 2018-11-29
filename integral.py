#!/usr/local/bin/python3
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget, QFileDialog, QLabel, QLineEdit, QHBoxLayout, QDialog, QMessageBox, QComboBox)
import pandas as pd
import numpy as np
import interpolation as inter
import os
from math import *

class IntWindow(QDialog):
    def __init__(self, parent = None, fName = 'f(x)', fDir = ''):
        super(IntWindow, self).__init__(parent)
        self.x = np.array([])
        self.fName = fName
        self.fDir = fDir
        grid = QGridLayout()
        self.button = QPushButton('Вычислить интеграл')
        self.button.clicked.connect(self.integral)
        self.button.setEnabled(False)

        self.button1 = QPushButton('Интерполяция')
        self.button1.clicked.connect(self.interpol)
        self.button1.setEnabled(False)
    
        self.buttonT = QPushButton('Записать в файл')
        self.buttonT.clicked.connect(self.saveF)
        self.buttonT.setEnabled(False)

        grid.addWidget(self.makeGroup(), 0, 0)
        grid.addWidget(self.makeBorder(), 1, 0)
        grid.addWidget(self.button, 2, 0, 1, -1)
        grid.addWidget(self.save(), 3, 0)
        grid.addWidget(self.buttonT, 4, 0)
        grid.addWidget(self.button1, 5, 0, 1, -1)

        self.setLayout(grid)
        self.setWindowTitle("Интегрирование")
    
    def interpol(self):
        self.InterpolWindow = inter.InterpolWindow(self, fDir = self.file, fName = 'U(y)')
        self.InterpolWindow.loadButton.setEnabled(True)
        self.InterpolWindow.show()
        self.close()

    def integrate(self):
        ans_arr = []
        if (type(self.lower) == str):
            for lower in range(self.x.shape[0] - 1):
                ans = np.float32(0.)
                for i in range(lower, self.func.shape[0] - 1):
                    ans += (self.x[i + 1] - self.x[i]) * (self.func[i] + self.func[i + 1]) / 2
                ans_arr.append(ans)
            ans_arr.append(0.)
        else:
            ans = np.float32(0.)
            for i in range(self.func.shape[0] - 1):
                ans += (self.x[i + 1] - self.x[i]) * (self.func[i] + self.func[i + 1]) / 2
            ans_arr.append(ans)
        return ans_arr
    
    
    def integral(self):
        self.i1 = self.integrate()
        self.showMessageBox('Успешно', 'Интеграл вычислен\n' + str(self.i1))
        self.buttonT.setEnabled(True)

    def showMessageBox(self, title, message):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        button = msg.addButton('ОК', QMessageBox.AcceptRole)
        msg.exec_()
        msg.deleteLater()
    
    def makeGroup(self):
        groupBox = QGroupBox('Выберите табулированную функцию')
        
        p = QLabel(self.fName + ':')
        self.pDir = QLineEdit(self.fDir)
        self.pDir.setMinimumWidth(80)
        self.pDir.setReadOnly(True)
        pDirButton = QPushButton('...')
        pDirButton.clicked.connect(self.pButton_click)
        self.loadButton = QPushButton('Загрузить данные')
        self.loadButton.clicked.connect(self.load)
        self.loadButton.setMinimumWidth(240)
        self.loadButton.setEnabled(False)
        grid = QGridLayout()
        
        grid.addWidget(p, 0, 0)
        grid.addWidget(self.pDir, 0, 1)
        grid.addWidget(pDirButton, 0, 2)
        grid.addWidget(self.loadButton, 1, 0, 1, -1)
        
        groupBox.setLayout(grid)
        return groupBox
    
    def makeBorder(self):
        groupBox = QGroupBox('Границы интегрирования')
        
        froml = QLabel('От : ')
        self.fromle = QComboBox(self)
        self.fromle.addItems(['y'])
        self.fromle.addItems(map(str, self.x))
        #self.fromle = QLineEdit('0')
        tol = QLabel('До : ')
        
        self.tole = QComboBox(self)
        self.tole.addItems(map(str, self.x))
        self.buttonSave = QPushButton('Сохранить')
        self.buttonSave.clicked.connect(self.saveBorder)
        self.buttonSave.setEnabled(False)
        
        grid = QGridLayout()

        grid.addWidget(froml, 0, 0)
        grid.addWidget(self.fromle, 0, 1)
        grid.addWidget(tol, 1, 0)
        grid.addWidget(self.tole, 1, 1)
        grid.addWidget(self.buttonSave, 2, 0, 1, -1)
        
        groupBox.setLayout(grid)
        return groupBox
    
    def saveBorder(self):
        try:
            indexFrom = self.fromle.currentIndex()
            indexTo = self.tole.currentIndex()
            if (indexFrom == 0):
                self.lower = 'y'
                self.upper = self.x[self.x.shape[0] - indexTo - 1]
            else:
                self.lower = self.x[indexFrom - 1]
                self.upper = self.x[self.x.shape[0] - indexTo - 1]
                if (self.lower > self.upper):
                    raise RuntimeError()
            self.showMessageBox('Успешно', 'Функция ' + self.fName + ' будет интегрироваться на отрезке: \n [ ' + str(self.lower) + ', ' + str(self.upper) + ']')
        except RuntimeError:
            self.showMessageBox('Ошибка', 'Правая граница больше левой.')
            self.lower = 'y'
            self.upper = self.x[-1]
            self.fromle.setCurrentIndex(0)
            self.tole.setCurrentIndex(0)
        self.buttonT.setEnabled(False)
    
    def pButton_click(self):
        name = QFileDialog.getOpenFileName(self, 'Open file', './data',  filter="Comma-Separated Values (*.csv)")[0]
        if name:
            self.pDir.setText(name)
            self.loadButton.setEnabled(True)

    def load(self):
        data = pd.read_csv(self.pDir.text())
        #data = np.array(data)
        self.x = np.array(data['t'])
        print(self.x)
        self.lower = 'y'
        self.upper = self.x[-1]
        self.func = np.array(data['f'])
        print(self.func)
        self.showMessageBox('Успешно', 'Сетка ' + self.fName + ' загружена.')
        for i in range(self.x.shape[0], 0, -1):
            self.fromle.removeItem(i)
            self.tole.removeItem(i)
        self.tole.removeItem(0)
        self.button.setEnabled(True)
        self.fromle.addItems(map(str, self.x))
        self.tole.addItems(map(str, self.x[::-1]))
        self.buttonSave.setEnabled(True)

    def chooseDir(self):
        name = str(QFileDialog.getExistingDirectory(self, "Select Directory", directory = './data'))
        if name:
            self.toFile.setText(name)
            print(self.toFile.text())

    def buttonClick(self):
        name = str(QFileDialog.getExistingDirectory(self, directory = './data'))
        if name:
            self.Dir.setText(name + '/')
            print(self.Dir.text())

    def save(self):
        groupBox = QGroupBox('Выбор директории')
        
        grid = QGridLayout()
        if (self.fDir != ''):
            num = self.fDir.rfind('/')
            self.Dir = QLineEdit(self.fDir[:num] + '/')
        else:
            self.Dir = QLineEdit(os.getcwd() + '/data/')
        self.Dir.setReadOnly(True)
        DirButton = QPushButton('...')
        DirButton.clicked.connect(self.buttonClick)
        lname = QLabel('Имя файла : ')
        self.name = QLineEdit(self.fName[0] + '_int')
        format = QLabel('.csv')
        
        grid.addWidget(self.Dir, 0, 0, 1, 2)
        grid.addWidget(DirButton, 0, 2)
        grid.addWidget(lname, 1, 0)
        grid.addWidget(self.name, 1, 1)
        grid.addWidget(format, 1, 2)
        
        groupBox.setLayout(grid)
        return groupBox

    def saveF(self):
        if (len(set(self.name.text()) & set('\/:*?"<>|+')) != 0 ):
            self.showMessageBox('Ошибка', 'Недопустимые функции в названии файла.')
            return
        if (type(self.lower) == str):
            data = {'f':self.i1, 't':self.x}
            df = pd.DataFrame(data=data)
            self.button1.setEnabled(True)
            self.showMessageBox('Успешно', 'Табулированное значение интеграла сохранено.')
        else:
            data = {'f':self.i1}
            df = pd.DataFrame(data=data)
            self.showMessageBox('Успешно', 'Значение интеграла сохранено.')
        self.file = ''
        self.file = self.Dir.text() + self.name.text() + '.csv'
        df.to_csv(self.file)
