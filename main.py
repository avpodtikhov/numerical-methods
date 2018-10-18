#!/usr/local/bin/python3
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication, QGridLayout, QGroupBox, QPushButton, QRadioButton, QVBoxLayout, QWidget, QFileDialog, QLabel, QLineEdit, QHBoxLayout, QMessageBox
import graphics
import func
import integral
import koshi
import interpolation
import difeq
from functools import partial
import os

class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.title = 'Программа'
        self.width = 520
        self.height = 430
        self.IntWindow = None
        self.KoshiWindow = None
        self.InterpolWindow = None
        self.GraphicsWindow = None
        self.FuncWindow = None
        self.mode = 0
        self.f = ''
        os.makedirs('./data', exist_ok=True)
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.addWidget(self.chooseMode(), 0, 0, 1, 1)
        grid.addWidget(self.useCase(), 0, 1, -1, 1)
        grid.addWidget(self.chooseDirectory(), 1, 0)
        grid.addWidget(self.chooseF(), 2, 0)

        self.setLayout(grid)
        self.setWindowTitle(self.title)
    #self.setFixedSize(self.width, self.height)

    def useCase(self):
        groupBoxUC = QGroupBox('Use-case')
        
        button1 = QPushButton('Задание функций p,z,S')
        button2 = QPushButton('Табулирование U(y)')
        button3 = QPushButton('Решение задачи Коши')

        button1.clicked.connect(self.openPZS)
        button2.clicked.connect(self.openU)
        button3.clicked.connect(self.openKoshi)

        vboxUC = QVBoxLayout()
        #vboxUC.setAlignment(Qt.AlignTop)
        vboxUC.addWidget(button1)
        vboxUC.addWidget(button2)
        vboxUC.addWidget(button3)
        groupBoxUC.setLayout(vboxUC)

        groupBoxM = QGroupBox('Модули')

        button4 = QPushButton('Задание функций')
        button5 = QPushButton('Интерполяция')
        button6 = QPushButton('Интегрирование')
        button7 = QPushButton('Решение ОДУ')
        button8 = QPushButton('Графики')

        button4.clicked.connect(self.openFunc)
        button5.clicked.connect(self.openInterpolation)
        button6.clicked.connect(self.openInt)
        button7.clicked.connect(self.openDE)
        button8.clicked.connect(self.openGraph)

        vboxM = QVBoxLayout()
        vboxM.setAlignment(Qt.AlignBottom)
        vboxM.addWidget(button4)
        vboxM.addWidget(button5)
        vboxM.addWidget(button6)
        vboxM.addWidget(button7)
        vboxM.addWidget(button8)

        groupBoxM.setLayout(vboxM)

        groupBoxMain = QGroupBox()
        vboxMain = QVBoxLayout()
        vboxMain.addWidget(groupBoxM)
        vboxMain.addWidget(groupBoxUC)
        groupBoxMain.setLayout(vboxMain)

        return groupBoxMain

    def openDE(self):
        self.DifEqWindow = difeq.DifEqWindow(self)
        self.DifEqWindow.show()

    def openU(self):
        if (self.pDir.text() == ''):
            self.showMessageBox('Ошибка', 'Введите путь к табулированной функции p(w)')
        else:
            self.IntWindowP = integral.IntWindow(self, fName = 'p(w)', fDir = self.pDir.text())
            self.IntWindowP.loadButton.setEnabled(True)
            self.IntWindowP.show()

    def openPZS(self):
        self.pWindow = func.FuncWindow(self, 'p(w)', 1)
        self.pWindow.show()
        self.zWindow = func.FuncWindow(self, 'z(t)', 2)
        self.zWindow.show()
        self.SWindow = func.FuncWindow(self, 'S(t)', 3)
        self.SWindow.show()

    def chooseMode(self):
        groupBox = QGroupBox('Режим запуска программы')

        radio1 = QRadioButton('Ручной')
        radio2 = QRadioButton('Автоматический')
        radio1.toggled.connect(self.manualMode)
        radio2.toggled.connect(self.autoMode)

        radio1.setChecked(True)

        vbox = QVBoxLayout()
        vbox.addWidget(radio1)
        vbox.addWidget(radio2)

        groupBox.setLayout(vbox)
        return groupBox

    def chooseDirectory(self):
        groupBox = QGroupBox('Пути к файлам')

        grid = QGridLayout()

        p = QLabel('p(w):')
        self.pDir = QLineEdit()
        self.pDir.setReadOnly(True)
        pDirButton = QPushButton('...')
        pDirButton.clicked.connect(self.pButton_click)

        s = QLabel('S(t):')
        self.sDir = QLineEdit()
        self.sDir.setReadOnly(True)
        sDirButton = QPushButton('...')
        sDirButton.clicked.connect(self.sButton_click)
        
        z = QLabel('z(t):')
        self.zDir = QLineEdit()
        self.zDir.setReadOnly(True)
        zDirButton = QPushButton('...')
        zDirButton.clicked.connect(self.zButton_click)
        
        u = QLabel('U(y):')
        self.uDir = QLineEdit()
        self.uDir.setReadOnly(True)
        uDirButton = QPushButton('...')
        uDirButton.clicked.connect(self.uButton_click)

        grid.addWidget(p, 0, 0)
        grid.addWidget(self.pDir, 0, 1)
        grid.addWidget(pDirButton, 0, 2)

        grid.addWidget(s, 1, 0)
        grid.addWidget(self.sDir, 1, 1)
        grid.addWidget(sDirButton, 1, 2)

        grid.addWidget(z, 2, 0)
        grid.addWidget(self.zDir, 2, 1)
        grid.addWidget(zDirButton, 2, 2)

        grid.addWidget(u, 3, 0)
        grid.addWidget(self.uDir, 3, 1)
        grid.addWidget(uDirButton, 3, 2)
        groupBox.setLayout(grid)
        return groupBox

    def chooseF(self):
        groupBox = QGroupBox('Выбор f')
        
        f = QLabel('f(z,x,S,b) = ')
        self.fEdit = QLineEdit()
        button = QPushButton('Сохранить')
        button.clicked.connect(self.saveF)
        vbox = QGridLayout()
        vbox.addWidget(f, 0, 0)
        vbox.addWidget(self.fEdit, 0, 1)
        vbox.addWidget(button, 1, 0, 1, -1)

        groupBox.setLayout(vbox)
        return groupBox

    def showMessageBox(self, title, message):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        button = msg.addButton('ОК', QMessageBox.AcceptRole)
        msg.exec_()
        msg.deleteLater()

    def saveF(self):
        try:
            z = 0
            x = 0
            S = 0
            b = 0
            print(eval(self.fEdit.text()))
            self.f = self.fEdit.text()
            self.showMessageBox('Успешно', 'Функция сохранена: \n f(z,x ,S, b) = ' + self.f)
        except:
            self.showMessageBox('Ошибка', 'Недопустимый вид функции.')

    def pButton_click(self):
        name = QFileDialog.getOpenFileName(self, 'Open file', './data', 'Comma-Separated Values (*.csv)')[0]
        if name:
            self.pDir.setText(name)

    def sButton_click(self):
        name = QFileDialog.getOpenFileName(self, 'Open file', './data', 'Comma-Separated Values (*.csv)')[0]
        if name:
            self.sDir.setText(name)

    def zButton_click(self):
        name = QFileDialog.getOpenFileName(self, 'Open file', './data',  'Comma-Separated Values (*.csv)')[0]
        if name:
            self.zDir.setText(name)

    def uButton_click(self):
        name = QFileDialog.getOpenFileName(self, 'Open file', './data',  'Comma-Separated Values (*.csv)')[0]
        if name:
            self.uDir.setText(name)

    def autoMode(self):
        self.mode = 1

    def manualMode(self):
        self.mode = 0

    def openInt(self):
        self.IntWindow = integral.IntWindow(self)
        self.IntWindow.show()

    def openKoshi(self):
        if (self.sDir.text() == ''):
            self.showMessageBox('Ошибка', 'Введите путь к табулированной функции S(t)')
        elif (self.zDir.text() == ''):
            self.showMessageBox('Ошибка', 'Введите путь к табулированной функции z(t)')
        elif (self.uDir.text() == ''):
            self.showMessageBox('Ошибка', 'Введите путь к табулированной функции U(y)')
        elif (self.f == ''):
            self.showMessageBox('Ошибка', 'Выберите класс функций f')
        else:
            self.KoshiWindow = koshi.KoshiWindow(self, self.mode, self.sDir.text(), self.zDir.text(), self.uDir.text(), self.f)
            self.KoshiWindow.show()
    def openFunc(self):
        self.FuncWindow = func.FuncWindow(self)
        self.FuncWindow.show()

    def openInterpolation(self):
        self.InterpolWindow = interpolation.InterpolWindow(self)
        self.InterpolWindow.show()

    def openGraph(self):
        self.GraphicsWindow = graphics.GraphicsWindow(self)
        self.GraphicsWindow.show()

if __name__ == '__main__':
    import sys
    QApplication.setStyle("fusion") #here
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
