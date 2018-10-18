#!/usr/local/bin/python3
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget, QFileDialog, QLabel, QLineEdit, QHBoxLayout, QDialog, QMessageBox)
import pandas as pd
import numpy as np
import interpolation as inter
import os

class DifEqWindow(QDialog):
    def __init__(self, parent = None, f1Name = 'x1', f1Dir = '', f2Name = 'x2', f2Dir = '', x10 = 0, x20 = 0):
        super(DifEqWindow, self).__init__(parent)
        self.f1Name = f1Name
        self.f1Dir = f1Dir
        self.f2Name = f2Name
        self.f2Dir = f2Dir
        self.x10 = x10
        self.x20 = x20
        self.initUI()

    def initUI(self):
        groupBox1 = QGroupBox('Введите систему ОДУ в виде интерполяций')
        groupBox2 = QGroupBox('Начальные значения функций')
        groupBox3 = QGroupBox('Сохранение результатов')
        
        l1 = QLabel('d' + self.f1Name + ' / dt = ')
        self.le1 = QLineEdit(self.f1Dir)
        self.le1.setReadOnly(True)
        button1 = QPushButton('...')
        button1.clicked.connect(self.button1_click)
        
        l2 = QLabel('d' + self.f2Name + ' / dt = ')
        self.le2 = QLineEdit(self.f2Dir)
        self.le2.setReadOnly(True)
        button2 = QPushButton('...')
        button2.clicked.connect(self.button2_click)
        
        f1l = QLabel(self.f1Name + '_0 = ')
        self.f1le = QLineEdit(str(self.x10))
        
        f2l = QLabel(self.f2Name + '_0 = ')
        self.f2le = QLineEdit(str(self.x20))
        
        button = QPushButton('Решить систему ОДУ')
        button.clicked.connect(self.solve)
        
        grid1 = QGridLayout()
        grid1.setAlignment(Qt.AlignTop)
        grid1.addWidget(l1, 0, 0)
        grid1.addWidget(self.le1, 0, 1)
        grid1.addWidget(button1, 0, 2)
        
        grid1.addWidget(l2, 1, 0)
        grid1.addWidget(self.le2, 1, 1)
        grid1.addWidget(button2, 1, 2)
        groupBox1.setLayout(grid1)
        
        grid2 = QGridLayout()
        grid2.setAlignment(Qt.AlignTop)
        grid2.addWidget(f1l, 0, 0)
        grid2.addWidget(self.f1le, 0, 1, 1, -1)
        
        grid2.addWidget(f2l, 1, 0)
        grid2.addWidget(self.f2le, 1, 1, 1, -1)
        
        groupBox2.setLayout(grid2)
            
        grid3 = QGridLayout()
        num = self.f2Dir.rfind('/')
        
        if (self.f1Dir != ''):
            num = self.f1Dir.rfind('/')
            self.Dir1 = QLineEdit(self.f1Dir[:num] + '/')
            self.Dir1.setReadOnly(True)
        else:
            self.Dir1 = QLineEdit(os.getcwd() + '/data/')
            self.Dir1.setReadOnly(True)
        DirButton1 = QPushButton('...')
        DirButton1.clicked.connect(self.buttonClick1)
        lname1 = QLabel('Имя файла : ')
        self.name1 = QLineEdit(self.f1Name)
        format1 = QLabel('.csv')

        if (self.f2Dir != ''):
            num = self.f2Dir.rfind('/')
            self.Dir2 = QLineEdit(self.f2Dir[:num] + '/')
            self.Dir2.setReadOnly(True)
        else:
            self.Dir2 = QLineEdit(os.getcwd() + '/data/')
            self.Dir2.setReadOnly(True)
        DirButton2 = QPushButton('...')
        DirButton2.clicked.connect(self.buttonClick2)
        lname2 = QLabel('Имя файла : ')
        self.name2 = QLineEdit(self.f2Name)
        format2 = QLabel('.csv')

        grid3.addWidget(self.Dir1, 0, 0, 1, 2)
        grid3.addWidget(DirButton1, 0, 2)
        grid3.addWidget(lname1, 1, 0)
        grid3.addWidget(self.name1, 1, 1)
        grid3.addWidget(format1, 1, 2)

        grid3.addWidget(self.Dir2, 2, 0, 1, 2)
        grid3.addWidget(DirButton2, 2, 2)
        grid3.addWidget(lname2, 3, 0)
        grid3.addWidget(self.name2, 3, 1)
        grid3.addWidget(format2, 3, 2)

        groupBox3.setLayout(grid3)
        
        self.buttonS = QPushButton('Сохранить')
        self.buttonS.clicked.connect(self.saveF)
        self.buttonS.setEnabled(False)
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop)
        vbox.addWidget(groupBox1)
        vbox.addWidget(groupBox2)
        vbox.addWidget(button)
        vbox.addWidget(groupBox3)
        vbox.addWidget(self.buttonS)
        self.setLayout(vbox)

        self.setWindowTitle("Решение ОДУ")
    #self.setFixedSize(340, 480)
    
    def buttonClick1(self):
        name = str(QFileDialog.getExistingDirectory(self, directory = './data'))
        if name:
            self.Dir1.setText(name + '/')
            print(self.Dir1.text())

    def buttonClick2(self):
        name = str(QFileDialog.getExistingDirectory(self, directory = './data'))
        if name:
            self.Dir2.setText(name + '/')
            print(self.Dir2.text())

    def saveF(self):
        if (len(set(self.name1.text()) & set('\/:*?"<>|+')) != 0 ):
            self.showMessageBox('Ошибка', 'Недопустимые функции в названии первого файла.')
            return
        if (len(set(self.name2.text()) & set('\/:*?"<>|+')) != 0 ):
            self.showMessageBox('Ошибка', 'Недопустимые функции в названии второго файла.')
            return
        data1 = pd.DataFrame([1, 1, 1, 1])
        data2 = pd.DataFrame([2, 2, 2, 2])
        file = ''
        file = self.Dir2.text() + self.name1.text() + '.csv'
        data1.to_csv(file)
        self.showMessageBox('Успешно', 'Табулированные значения функции находятся в файле: \n' + file)
        file = ''
        file = self.Dir2.text() + self.name2.text() + '.csv'
        data2.to_csv(file)
        self.showMessageBox('Успешно', 'Табулированные значения функции находятся в файле: \n' + file)

    def solve(self):
        try:
            self.x10 = float(self.f1le.text())
            self.x20 = float(self.f2le.text())
            if ((self.le1.text() == './') or (self.le2.text() == './')):
                self.showMessageBox('Ошибка', 'Не выбраны функции производных')
                self.buttonS.setEnabled(False)
            else:
                self.showMessageBox('Успешно', 'Система успешно решена!')
                self.buttonS.setEnabled(True)
        except:
            self.showMessageBox('Ошибка', 'Неправильный тип данных начальных условий. \n Допустимый тип:  float.')

    def button1_click(self):
        name = QFileDialog.getOpenFileName(self, 'Open file', './data', 'Comma-Separated Values (*.csv)')[0]
        if name:
            self.le1.setText(name)

    def button2_click(self):
        name = QFileDialog.getOpenFileName(self, 'Open file', './data', 'Comma-Separated Values (*.csv)')[0]
        if name:
            self.le2.setText(name)

    def showMessageBox(self, title, message):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        button = msg.addButton('ОК', QMessageBox.AcceptRole)
        msg.exec_()
        msg.deleteLater()
