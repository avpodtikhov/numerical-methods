#!/usr/local/bin/python3
from PyQt5.QtWidgets import QGridLayout, QGroupBox, QPushButton, QLabel, QLineEdit, QDialog, QMessageBox
from PyQt5.QtCore import QPoint
import tab
from math import *

class FuncWindow(QDialog):
    def __init__(self, parent=None, fName = 'f(x)', index = 0):
        super(FuncWindow, self).__init__(parent)
        print(fName)
        self.title = 'Задание функций'
        self.width = 300
        self.height = 120
        self.fName = fName
        self.index = index
        self.initUI()
    
    def initUI(self):
        groupBox = QGroupBox('Введите ' + self.fName)
        if (self.index != 0):
            p = QPoint(100 + self.index * (self.width + 20), 400)
            self.move(p)
        lF = QLabel()
        lF.setText(self.fName + ' = ')
        self.leF = QLineEdit()
        
        buttonS = QPushButton('Сохранить')
        buttonS.clicked.connect(self.saveF)
        self.buttonFR = QPushButton('Табулировать')
        self.buttonFR.setEnabled(False)
        self.buttonFR.clicked.connect(self.tabF)
        
        grid = QGridLayout()
        
        grid.addWidget(lF, 0, 0)
        grid.addWidget(self.leF, 0, 1)
        grid.addWidget(buttonS, 1, 0)
        grid.addWidget(self.buttonFR, 1, 1)
        
        groupBox.setLayout(grid)
    
        grid = QGridLayout()
        grid.addWidget(groupBox, 0, 0)
        self.setLayout(grid)
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)

    def showMessageBox(self, title, message):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        button = msg.addButton('ОК', QMessageBox.AcceptRole)
        msg.exec_()
        msg.deleteLater()

    def saveF(self):
        try:
            w = 0
            x = 0
            t = 0
            self.fText = self.leF.text()
            print(eval(self.fText))
            self.showMessageBox('Успешно', 'Функция приняла вид:\n' + self.fName + ' = ' + self.fText)
            self.buttonFR.setEnabled(True)
        except:
            self.showMessageBox('Ошибка', 'Недопустимый вид функции.')
            self.buttonFR.setEnabled(False)

    def tabF(self):
        self.TabWindowF = tab.TabWindow(self, funcName = self.fName, valName = self.fName[2], func = self.fText)
        self.TabWindowF.show()
        self.close()
