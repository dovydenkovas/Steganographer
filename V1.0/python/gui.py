# This module contains Qt5 window class
from os import getcwd
from threading import Thread
import webbrowser

from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import qApp
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QButtonGroup
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget



class MainWindow(QMainWindow):
    def __init__(self,ReadTh, WriteTh,ciphers):
        super().__init__()
        self.message = None
        self.ReadTh = ReadTh
        self.WriteTh = WriteTh
        self.ciphers = ciphers
        self.t = QTimer()
        self.t.timeout.connect(self.CheckResult)
        self.t.start(500)
        self.CreateWindow()


    def Run(self):
        self.statusBar().showMessage('Чтение входных данных')
        text = self.Text.toPlainText()
        key = self.KeyWorld.text()
        type = str(self.CipherType.currentText())
        input = self.FileIn.text()
        output = self.FileOut.text()

        if len(input) == 0:
            self.statusBar().showMessage('Предупреждение: Выберите исходное изображение!')
            return

        if self.button_group.checkedButton().text() == "Шифровать":
            if len(output) == 0:
                self.statusBar().showMessage('Предупреждение: Выберите имя конечного изображения!')
                return
            if len(text) == 0:
                self.statusBar().showMessage('Предупреждение: Введите текст сообщения!')
                return
            self.statusBar().showMessage('Кодирование...')
            try:
                TH = Thread(target=self.WriteTh, args=(input, output, text, key, type,self.statusBar().showMessage))
                TH.start()
                TH.join(0)
            except:
                self.statusBar().showMessage('Предупреждение: Плохое исходное изображение!')
        else:
            self.statusBar().showMessage('Декодирование')
            try:
                TH = Thread(target=self.ReadTh, args=(input, key, type, self.statusBar().showMessage, self))
                TH.start()
                TH.join(0)
            except:
                self.statusBar().showMessage('Предупреждение: Ошика входных данных!')


    def CheckResult(self):
        if self.message != None:
            self.Text.setText(self.message)
            self.message = None

    def getOutputFile(self):
        if self.button_group.checkedButton().text() == "Шифровать":
            fname = QFileDialog.getSaveFileName(self, 'Результат', '', "*.png *.jpg")[0]
        else:
            fname = QFileDialog.getSaveFileName(self, 'Результат', '', "*")[0]
        self.FileOut.setText(fname)


    def getInputFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Входное изображение', '', "*.png *.jpg")[0]
        self.FileIn.setText(fname)


    def ViewTools(self):
        if self.ControlView:
            self.ControlFrame.setMaximumWidth(0)
            self.ControlView = False
        else:
            self.ControlFrame.setMaximumWidth(210)
            self.ControlView = True

    def showAboutInfo(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Версия")
        msg.setText("Стеганограф-Шифратор 1.1")
        msg.addButton('Понятно', QMessageBox.AcceptRole)
        msg.exec()

    def showHelpWebSite(self):
        '''Open help html document'''
        webbrowser.open(f"{getcwd()}/data/Help/index.html", new=1)







    def CreateWindow(self):
        self.resize(900,600)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowTitle('Стеганограф-Шифратор')
        self.setWindowIcon(QIcon('data/images/icon.png'))
        self.statusBar()
        self.setStyleSheet("QLabel,QPushButton,QLineEdit,QComboBox,QRadioButton,QTextEdit {font: 10pt Comic Sans MS}")

        self.win = QWidget(self)
        self.win.setObjectName("centralWidget")

        # menubar and Create hotkeys
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Файл')

        exitAction = QAction(QIcon('data\images\getInputFile.png'), '&Входное изображение', self)
        exitAction.setShortcut('Ctrl+O')
        exitAction.setStatusTip('Изображение из которого надо прочитать сообщение или в которое надо записать изображение')
        exitAction.triggered.connect(self.getInputFile)
        fileMenu.addAction(exitAction)

        exitAction = QAction(QIcon('data\images\getOutputFile.png'), '&Результат', self)
        exitAction.setShortcut('Ctrl+S')
        exitAction.setStatusTip('Имя изображения с сообщением')
        exitAction.triggered.connect(self.getOutputFile)
        fileMenu.addAction(exitAction)

        fileMenu.addSeparator()

        exitAction = QAction(QIcon('exit.png'), '&Выход', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Закрыть приложение')
        exitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAction)

        fileMenu = menubar.addMenu('&Вид')
        exitAction = QAction(QIcon('toolbar.png'), '&Показать/Скрыть панель инструментов', self)
        exitAction.setStatusTip('Вы можете скрыть панель инструментов, в левой части окна')
        self.ControlView = True
        exitAction.triggered.connect(self.ViewTools)
        fileMenu.addAction(exitAction)



        fileMenu = menubar.addMenu('&Помощь')
        exitAction = QAction(QIcon('data\images\showHelpWebSite.png'), '&Как пользоваться', self)
        exitAction.setShortcut('F1')
        exitAction.setStatusTip('Инструкция по применению приложения')
        exitAction.triggered.connect(self.showHelpWebSite)
        fileMenu.addAction(exitAction)
        exitAction = QAction(QIcon('data\images\showAboutInfo.png'), '&Версия', self)
        exitAction.setStatusTip('Версия программы')
        exitAction.triggered.connect(self.showAboutInfo)
        fileMenu.addAction(exitAction)

        #Create toolbar
        hbox = QHBoxLayout(self.win)
        self.TextFrame = QFrame(self.win)
        self.TextFrame.setFrameShape(QFrame.StyledPanel)
        self.TextL = self.Control = QHBoxLayout(self.TextFrame)
        self.Text = QTextEdit()
        self.TextL.addWidget(self.Text)

        self.ControlFrame = QFrame(self.win)
        self.ControlFrame.setFrameShape(QFrame.StyledPanel)
        self.Control = QVBoxLayout(self.ControlFrame)

        self.RadioBTN_Cipher = QRadioButton("Шифровать")
        self.RadioBTN_UnCipher = QRadioButton("Расшифровать")
        self.Check = QHBoxLayout()
        self.Check.addWidget(self.RadioBTN_Cipher)
        self.Check.addWidget(self.RadioBTN_UnCipher)
        self.RadioBTN_Cipher.setChecked(True)
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.RadioBTN_Cipher)
        self.button_group.addButton(self.RadioBTN_UnCipher)

        self.labelIn = QLabel("Входное изображение")
        self.FileInBTN = QPushButton("Выбрать")
        self.FileInBTN.clicked.connect(self.getInputFile)
        self.FileInL = QHBoxLayout()
        self.FileInL.addWidget(self.labelIn)
        self.FileInL.addWidget(self.FileInBTN)
        self.FileIn = QLineEdit()

        self.labelOut = QLabel("Результат")
        self.FileOutBTN = QPushButton("Выбрать")
        self.FileOutBTN.clicked.connect(self.getOutputFile)
        self.FileOut = QLineEdit()
        self.FileOutL = QHBoxLayout()
        self.FileOutL.addWidget(self.labelOut)
        self.FileOutL.addWidget(self.FileOutBTN)

        self.labelCipherType = QLabel("Выберите тип шифрования")
        self.CipherType = QComboBox()
        self.CipherType.addItems(map(lambda a:a.name,self.ciphers))
        self.labelKeyWorld = QLabel("Введите ключ шифрования")
        self.KeyWorld = QLineEdit()
        self.runBTN = QPushButton("Выполнить")
        self.runBTN.clicked.connect(self.Run)

        self.ControlFrame.setMaximumWidth(280)
        self.Control.addLayout(self.Check)
        self.Control.addLayout(self.FileInL)
        self.Control.addWidget(self.FileIn)
        self.Control.addLayout(self.FileOutL)
        self.Control.addWidget(self.FileOut)
        self.Control.addWidget(self.labelCipherType)
        self.Control.addWidget(self.CipherType)
        self.Control.addWidget(self.labelKeyWorld)
        self.Control.addWidget(self.KeyWorld)
        self.Control.addWidget(self.runBTN)
        self.Control.setSpacing(15)
        self.Control.addStretch(1)
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.ControlFrame)
        self.splitter.addWidget(self.TextFrame)

        hbox.addWidget(self.splitter)
        self.win.setLayout(hbox)
        self.setCentralWidget(self.win)

        self.show()
