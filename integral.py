#!/usr/local/bin/python3
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget, QFileDialog, QLabel, QLineEdit, QHBoxLayout, QDialog, QMessageBox)
import pandas as pd
import numpy as np
import interpolation as inter
import os

class IntWindow(QDialog):
    def __init__(self, parent = None, fName = 'f(x)', fDir = ''):
        super(IntWindow, self).__init__(parent)
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
    #self.setFixedSize(300, 460)
    
    def interpol(self):
        self.InterpolWindow = inter.InterpolWindow(self, fDir = self.file, fName = 'U(y)')
        self.InterpolWindow.loadButton.setEnabled(True)
        self.InterpolWindow.show()
        self.close()

    def integral(self):
        self.grid = self.fGrid
        self.showMessageBox('Успешно', 'Интеграл вычислен')
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
        self.fromle = QLineEdit('0')
        tol = QLabel('До : ')
        self.tole = QLineEdit('1')
        button = QPushButton('Сохранить')
        button.clicked.connect(self.saveBorder)
        
        grid = QGridLayout()
        
        grid.addWidget(froml, 0, 0)
        grid.addWidget(self.fromle, 0, 1)
        grid.addWidget(tol, 1, 0)
        grid.addWidget(self.tole, 1, 1)
        grid.addWidget(button, 2, 0, 1, -1)
        
        groupBox.setLayout(grid)
        return groupBox
    
    def saveBorder(self):
        self.showMessageBox('Успешно', 'Функция ' + self.fName + ' будет интегрироваться на отрезке: \n [ ' + self.fromle.text() + ', ' + self.tole.text() + ']')
    
    def pButton_click(self):
        name = QFileDialog.getOpenFileName(self, 'Open file', './data',  filter="Comma-Separated Values (*.csv)")[0]
        if name:
            self.pDir.setText(name)
            self.loadButton.setEnabled(True)

    def load(self):
        data = pd.read_csv(self.pDir.text())
        self.fGrid = np.array(data)
        #self.w = ar[:, 0]
        #print(ar[:, 1])
        #self.p = ar[:, 1]
        self.showMessageBox('Успешно', 'Сетка ' + self.fName + ' загружена.')
        self.button.setEnabled(True)
        #self.intButton.setEnabled(True)
    
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
        data = pd.DataFrame(self.grid)
        self.file = ''
        self.file = self.Dir.text() + self.name.text() + '.csv'
        data.to_csv(self.file)
        self.showMessageBox('Успешно', 'Табулированные значения функции находятся в файле: \n' + self.file)
        self.button1.setEnabled(True)
    


    '''def save(self):
        data = pd.DataFrame([1, 1, 1, 1, 1])
        file = ''
        if (self.toFile.text()):
            file = self.toFile.text() + '/U.csv'
        else:
            file = './U.csv'
        data.to_csv(file)
        self.showMessageBox('Успешно', 'Интерполяцтонные коэффиценты находятся в файле: \n' + file)'''
