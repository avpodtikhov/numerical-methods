#!/usr/local/bin/python3
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
                             QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget, QFileDialog, QLabel, QLineEdit, QHBoxLayout, QDialog, QMessageBox)
import pandas as pd
import numpy as np
import os
import spline

class InterpolWindow(QDialog):
    def __init__(self, parent=None, fDir = '', fName = 'f(x)'):
        super(InterpolWindow, self).__init__(parent)
        self.fDir = fDir
        self.fName = fName
        self.intButton = QPushButton('Вычислить к-ты интерполяции')
        self.intButton.clicked.connect(self.interpolCef)
        self.intButton.setEnabled(False)
        
        self.buttonT = QPushButton('Записать в файл')
        self.buttonT.clicked.connect(self.saveF)
        self.buttonT.setEnabled(False)

        grid = QGridLayout()
        grid.addWidget(self.makeGroup(), 0, 0)
        grid.addWidget(self.intButton, 1, 0)
        grid.addWidget(self.save(), 2, 0)
        grid.addWidget(self.buttonT, 3, 0)
        self.setLayout(grid)
        self.setWindowTitle("Интерполяция")
    #self.setFixedSize(300, 320)
    
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
    
    def interpolCef(self):
        s = spline.Spline(self.t, self.f)
        self.cef = s.write_cef()
        self.showMessageBox('Успешно', 'К-ты интерполяции функции ' + self.fName + '\n Вычислены')
        self.buttonT.setEnabled(True)
    #self.saveButton.setEnabled(True)
    
    def pButton_click(self):
        name = QFileDialog.getOpenFileName(self, 'Open file', filter="Comma-Separated Values (*.csv)")[0]
        if name:
            self.pDir.setText(name)
            self.loadButton.setEnabled(True)

    def load(self):
        try:
            data = pd.read_csv(self.pDir.text())
            self.t = data['t']
            self.f = data['f']
            print(self.t)
            print('------')
            print(self.f)
            self.showMessageBox('Успешно', 'Сетка ' + self.fName + ' загружена.')
            self.intButton.setEnabled(True)
        except:
            self.showMessageBox('Ошибка', 'Что-то пошло не так')
        #self.intButton.setEnabled(True)

    def buttonClick(self):
        name = str(QFileDialog.getExistingDirectory(self))
        if name:
            self.Dir.setText(name + '/')
            print(self.Dir.text())

    def save(self):
        groupBox = QGroupBox('Выбор директории')
        
        grid = QGridLayout()
        if (self.fDir != ''):
            num = self.fDir.rfind('/')
            self.Dir = QLineEdit(self.fDir[:num] + '/')
            self.Dir.setReadOnly(True)
        else:
            self.Dir = QLineEdit(os.getcwd() + '/data/')
            self.Dir.setReadOnly(True)
        DirButton = QPushButton('...')
        DirButton.clicked.connect(self.buttonClick)
        lname = QLabel('Имя файла : ')
        self.name = QLineEdit(self.fName[0] + '_interpol')
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
        print(self.cef[0])
        print(self.cef[1])
        print(self.cef[2])
        print(self.cef[3])
        cefb = np.append(self.cef[3], np.zeros(1))
        cefa = np.append(self.cef[2], np.zeros(1))
        data = {'t':self.cef[0], 'm':self.cef[1], 'a':cefa, 'b':cefb}
        df = pd.DataFrame(data=data)
        file = ''
        file = self.Dir.text() + self.name.text() + '.csv'
        df.to_csv(file)
        self.showMessageBox('Успешно', 'Табулированные значения функции находятся в файле: \n' + file)
