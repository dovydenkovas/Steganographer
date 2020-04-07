"""
gui.py is consist of MainWindow class for steganography cipher program
"""
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
    """
    Main Window include:
        - run function for ciphering or deciphering
        - check_result
        - get_output_file
        - get_input_file
        - view_tools
        - show_about_info
        - show_help
        - create_window
    """

    def __init__(self, read_thread, write_thread, ciphers):
        super().__init__()
        self.message = None
        self.read_thread = read_thread
        self.write_thread = write_thread
        self.ciphers = ciphers
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_result)
        self.timer.start(500)

        # create window
        self.resize(900, 600)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowTitle('Стеганограф-Шифратор')
        self.setWindowIcon(QIcon('data/images/icon.png'))
        self.statusBar()
        self.setStyleSheet("QLabel,QPushButton,QLineEdit,QComboBox,QRadioButton,QTextEdit {font: 10pt Comic Sans MS}")

        self.window = QWidget(self)
        self.window.setObjectName("centralWidget")

        # Create menubar and hotkeys
        menu_bar = self.menuBar()
        file_menu_bar = menu_bar.addMenu('&Файл')

        get_input_file_action = QAction('&Входное изображение', self)
        get_input_file_action.setShortcut('Ctrl+O')
        get_input_file_action.setStatusTip(
            'Изображение из которого надо прочитать сообщение или в которое надо записать изображение')
        get_input_file_action.triggered.connect(self.get_input_file)
        file_menu_bar.addAction(get_input_file_action)

        get_output_file_action = QAction('&Результат', self)
        get_output_file_action.setShortcut('Ctrl+S')
        get_output_file_action.setStatusTip('Имя изображения с сообщением')
        get_output_file_action.triggered.connect(self.get_output_file)
        file_menu_bar.addAction(get_output_file_action)

        file_menu_bar.addSeparator()

        exit_action = QAction('&Выход', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Закрыть приложение')
        exit_action.triggered.connect(qApp.quit)
        file_menu_bar.addAction(exit_action)

        file_menu_bar = menu_bar.addMenu('&Вид')
        show_tools_action = QAction('&Показать/Скрыть панель инструментов', self)
        show_tools_action.setStatusTip('Вы можете скрыть панель инструментов, в левой части окна')
        self.is_view_control = True
        show_tools_action.triggered.connect(self.view_tools)
        file_menu_bar.addAction(show_tools_action)

        file_menu_bar = menu_bar.addMenu('&Помощь')
        help_action = QAction('&Как пользоваться', self)
        help_action.setShortcut('F1')
        help_action.setStatusTip('Инструкция по применению приложения')
        help_action.triggered.connect(self.show_help)
        file_menu_bar.addAction(help_action)
        exit_action = QAction('&Версия', self)
        exit_action.setStatusTip('Версия программы')
        exit_action.triggered.connect(self.show_about_info)
        file_menu_bar.addAction(exit_action)

        # Create toolbar
        hbox = QHBoxLayout(self.window)
        self.text_frame = QFrame(self.window)
        self.text_frame.setFrameShape(QFrame.StyledPanel)
        self.text_layout = self.control_layout = QHBoxLayout(self.text_frame)
        self.text = QTextEdit()
        self.text_layout.addWidget(self.text)

        self.control_frame = QFrame(self.window)
        self.control_frame.setFrameShape(QFrame.StyledPanel)
        self.control_layout = QVBoxLayout(self.control_frame)

        self.radio_btn_cipher = QRadioButton("Шифровать")
        self.radio_btn_un_cipher = QRadioButton("Расшифровать")
        self.select_mode_layout = QHBoxLayout()
        self.select_mode_layout.addWidget(self.radio_btn_cipher)
        self.select_mode_layout.addWidget(self.radio_btn_un_cipher)
        self.radio_btn_cipher.setChecked(True)
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.radio_btn_cipher)
        self.button_group.addButton(self.radio_btn_un_cipher)

        self.input_label = QLabel("Входное изображение")
        self.input_button = QPushButton("Выбрать")
        self.input_button.clicked.connect(self.get_input_file)
        self.input_layout = QHBoxLayout()
        self.input_textedit = QLineEdit()
        self.input_layout.addWidget(self.input_label)
        self.input_layout.addWidget(self.input_button)

        self.output_label = QLabel("Результат")
        self.output_button = QPushButton("Выбрать")
        self.output_button.clicked.connect(self.get_output_file)
        self.output_textedit = QLineEdit()
        self.output_layout = QHBoxLayout()
        self.output_layout.addWidget(self.output_label)
        self.output_layout.addWidget(self.output_button)

        self.cipher_type_label = QLabel("Выберите тип шифрования")
        self.cipher_types = QComboBox()
        self.cipher_types.addItems(map(lambda a: a.name, self.ciphers))
        self.password_label = QLabel("Введите ключ шифрования")
        self.password_textedit = QLineEdit()
        self.run_button = QPushButton("Выполнить")
        self.run_button.clicked.connect(self.run)

        self.control_frame.setMaximumWidth(280)
        self.control_layout.addLayout(self.select_mode_layout)
        self.control_layout.addLayout(self.input_layout)
        self.control_layout.addWidget(self.input_textedit)
        self.control_layout.addLayout(self.output_layout)
        self.control_layout.addWidget(self.output_textedit)
        self.control_layout.addWidget(self.cipher_type_label)
        self.control_layout.addWidget(self.cipher_types)
        self.control_layout.addWidget(self.password_label)
        self.control_layout.addWidget(self.password_textedit)
        self.control_layout.addWidget(self.run_button)
        self.control_layout.setSpacing(15)
        self.control_layout.addStretch(1)
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.control_frame)
        self.splitter.addWidget(self.text_frame)

        hbox.addWidget(self.splitter)
        self.window.setLayout(hbox)
        self.setCentralWidget(self.window)

        self.show()

    def run(self):
        """
        Run function is started when pressed run button.
        This function check input data and
        start thread with ciphering or deciphering function.
        """
        self.statusBar().showMessage('Чтение входных данных')
        text = self.text.toPlainText()
        key = self.password_textedit.text()
        cipher_type = str(self.cipher_types.currentText())
        infile = self.input_textedit.text()
        output = self.output_textedit.text()

        # check fail input data
        if len(infile) == 0:
            self.statusBar().showMessage('Предупреждение: Выберите исходное изображение!')
            return

        if self.button_group.checkedButton().text() == "Шифровать":
            if len(output) == 0:
                self.statusBar().showMessage('Предупреждение: Выберите имя конечного изображения!')
            elif len(text) == 0:
                self.statusBar().showMessage('Предупреждение: Введите текст сообщения!')
            else:  # if input data is correct
                self.statusBar().showMessage('Кодирование...')
                try:
                    thread = Thread(target=self.write_thread, args=(
                                    infile, output, text, key, cipher_type,
                                    self.ciphers, self.statusBar().showMessage))
                    thread.start()
                    thread.join(0)
                except:
                    self.statusBar().showMessage('Предупреждение: Плохое исходное изображение!')
        else:  # if deciphering
            self.statusBar().showMessage('Декодирование')
            try:
                thread = Thread(target=self.read_thread,
                                args=(infile, key, cipher_type, self.ciphers, self.statusBar().showMessage, self))
                thread.start()
                thread.join(0)
            except:
                self.statusBar().showMessage('Предупреждение: Ошика входных данных!')

    def check_result(self):
        """
            start every 0.5 sec. Check result. if message is ready, insert it in textbox.
        """
        if self.message is not None:
            self.text.setText(self.message)
            self.message = None

    def get_output_file(self):
        """ Select output file dialog """
        if self.button_group.checkedButton().text() == "Шифровать":
            filename = QFileDialog.getSaveFileName(self, 'Результат', '', "*.png *.jpg")[0]
        else:
            filename = QFileDialog.getSaveFileName(self, 'Результат', '', "*")[0]
        self.output_textedit.setText(filename)

    def get_input_file(self):
        """ Select input file dialog """
        filename = QFileDialog.getOpenFileName(self, 'Входное изображение', '', "*.png *.jpg")[0]
        self.input_textedit.setText(filename)

    def view_tools(self):
        """ show or hide tools menu (left menu) """
        if self.is_view_control:
            self.control_frame.setMaximumWidth(0)
        else:
            self.control_frame.setMaximumWidth(300)
        self.is_view_control = not self.is_view_control

    def show_about_info(self):
        """ Show info message with version of program """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Версия")
        msg.setText("Стеганограф-Шифратор 1.1")
        msg.addButton('Понятно', QMessageBox.AcceptRole)
        msg.exec()

    def show_help(self):
        """Open help html document"""
        webbrowser.open(f"{getcwd()}/data/Help/index.html", new=1)
