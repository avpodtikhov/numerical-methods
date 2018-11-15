#!/usr/local/bin/python3
from PyQt5.QtWidgets import QGridLayout, QGroupBox, QPushButton, QFileDialog, QLabel, QLineEdit, QDialog, QMessageBox
import pandas as pd
import numpy as np
from math import *
import os

class TabWindow(QDialog):
    def __init__(self, parent=None, funcName = None, valName = None, func = None):
        super(TabWindow, self).__init__(parent)
        self.title = 'Табуляция'
        self.width = 300
        self.height = 350
        self.funcName = funcName
        self.valName= valName
        self.lower = None
        self.upper = None
        self.func = func
        self.h = 0
        self.setMinimumWidth(310)
        self.minimized = True
        self.initUI()

    def initUI(self):
        lfunc = QLabel('Функция: ' + self.funcName + ' = ' + self.func)
        self.buttonT = QPushButton('Табулировать')
        self.buttonT.clicked.connect(self.tab)
        self.buttonT.setEnabled(False)

        grid = QGridLayout()
        grid.addWidget(lfunc, 0, 0)
        grid.addWidget(self.makeGroup(), 1, 0)
        grid.addWidget(self.chooseDirectory(), 2, 0)
        grid.addWidget(self.buttonT, 3, 0)

        self.setLayout(grid)
        self.setWindowTitle(self.title)
        #self.setFixedSize(self.width, self.height)

    def buttonClick(self):
        name = str(QFileDialog.getExistingDirectory(self, directory = './data'))
        if name:
            self.Dir.setText(name + '/')
            print(self.Dir.text())

    def chooseDirectory(self):
        groupBox = QGroupBox('Выбор директории')

        grid = QGridLayout()

        self.Dir = QLineEdit(os.getcwd() + '/data/')
        self.Dir.setReadOnly(True)
        DirButton = QPushButton('...')
        DirButton.clicked.connect(self.buttonClick)
        lname = QLabel('Имя файла : ')
        self.name = QLineEdit(self.funcName[0])
        format = QLabel('.csv')
        
        grid.addWidget(self.Dir, 0, 0, 1, 2)
        grid.addWidget(DirButton, 0, 2)
        grid.addWidget(lname, 1, 0)
        grid.addWidget(self.name, 1, 1)
        grid.addWidget(format, 1, 2)
        
        groupBox.setLayout(grid)
        return groupBox

    def makeGroup(self):
        groupBox = QGroupBox('Параметры сетки')
        
        l = QLabel(self.valName + '   =    [')
        l1 = QLabel(', ')
        l2 = QLabel(']')
        l3 = QLabel('N : ')
        self.leLower = QLineEdit()
        #self.leLower.setMinimumWidth(50)
        self.leUpper = QLineEdit()
        #self.leUpper.setMinimumWidth(50)
        self.leH = QLineEdit()
        buttonS = QPushButton('Сохранить')
        buttonS.clicked.connect(self.save)
        #buttonS.setMinimumWidth(240)

        grid = QGridLayout()
        
        grid.addWidget(l, 0, 0)
        grid.addWidget(self.leLower, 0, 1)
        grid.addWidget(l1, 0, 2)
        grid.addWidget(self.leUpper, 0, 3)
        grid.addWidget(l2, 0, 4)
        grid.addWidget(l3, 1, 0)
        grid.addWidget(self.leH, 1, 1)
        grid.addWidget(buttonS, 2, 0, 1, -1)

        groupBox.setLayout(grid)
        return groupBox

    def showMessageBox(self, title, message):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        button = msg.addButton('ОК', QMessageBox.AcceptRole)
        msg.exec_()
        msg.deleteLater()

    def save(self):
        try:
            self.lower = np.float32(self.leLower.text())
            self.upper = np.float32(self.leUpper.text())
            if (self.lower > self.upper):
                raise RuntimeError()
            self.n = np.float32(self.leH.text()) - 1
            if (self.n <= 0):
                raise NameError()
            self.showMessageBox('Успешно', 'Значения сохранены.')
            self.buttonT.setEnabled(True)
        except ValueError:
            self.showMessageBox('Ошибка', 'Неправильный тип данных параметров. \n Допустимый тип:  np.float32.')
            self.leLower.setText('')
            self.leUpper.setText('')
            self.buttonT.setEnabled(False)
        except NameError:
            self.showMessageBox('Ошибка', 'Неправильное колличество узлов сетки.')
            self.leLower.setText('')
            self.leUpper.setText('')
            self.buttonT.setEnabled(False)      
        except RuntimeError:
            self.showMessageBox('Ошибка', 'Правая граница больше левой.')
            self.leLower.setText('')
            self.leUpper.setText('')
            self.buttonT.setEnabled(False)

    def tab(self):
        if (len(set(self.name.text()) & set('\/:*?"<>|+')) != 0 ):
            self.showMessageBox('Ошибка', 'Недопустимые функции в названии файла.')
            return
        h = (self.upper - self.lower) / self.n
        print(h)
        if (self.funcName == 'p(w)'):
            t_arr = np.arange(self.lower, self.upper + h, h)
            function = np.empty_like(t_arr)
            print(function.shape)
            for i in range(function.shape[0]):
                w = t_arr[i]
                function[i] = eval(self.func)
        if (self.funcName == 'f(x)'):
            t_arr = np.arange(self.lower, self.upper + h, h)
            function = np.empty_like(t_arr)
            print(function.shape)
            for i in range(function.shape[0]):
                x = t_arr[i]
                function[i] = eval(self.func)
        else:
            t_arr = np.arange(self.lower, self.upper + h, h)
            function = np.empty_like(t_arr)
            print(function.shape)
            for i in range(function.shape[0]):
                t = t_arr[i]
                function[i] = eval(self.func)
        data = pd.DataFrame(function, t_arr)
        file = ''
        file = self.Dir.text() + self.name.text() + '.csv'
        data.to_csv(file)
        self.showMessageBox('Успешно', 'Табулированные значения функции находятся в файле: \n' + file)
