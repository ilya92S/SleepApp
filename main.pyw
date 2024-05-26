import sys
import os
from PyQt6.QtWidgets import (QApplication, QHBoxLayout,
                             QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox)
from PyQt6.QtCore import QTimer, Qt


class ShutdownTimerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Таймер выключения')
        self.setGeometry(100, 100, 300, 150)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.layout = QVBoxLayout()

        self.label = QLabel('Введи время в минутах:')
        self.layout.addWidget(self.label)

        self.time_input = QLineEdit(self)
        self.layout.addWidget(self.time_input)

        self.start_button = QPushButton('Вкл. таймер', self)
        self.start_button.clicked.connect(self.start_timer)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton('Выкл. таймер', self)
        self.stop_button.clicked.connect(self.stop_timer)
        self.layout.addWidget(self.stop_button)

        hbox = QHBoxLayout()

        self.minim_button = QPushButton('Скрыть', self)
        self.minim_button.clicked.connect(self.showMinimized)
        hbox.addWidget(self.minim_button)

        self.close_button = QPushButton('Закрыть', self)
        self.close_button.clicked.connect(self.close)
        hbox.addWidget(self.close_button)

        self.layout.addLayout(hbox)

        self.setLayout(self.layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.shutdown_computer)
        self.shutdown_scheduled = False

    def start_timer(self):
        try:
            minutes = int(self.time_input.text())
            if minutes <= 0:
                raise ValueError

            seconds = minutes * 60
            self.timer.start(seconds * 1000)
            self.shutdown_scheduled = True
            QMessageBox.information(self, 'Таймер включен', f'Компьютер '
                                                            f'будет выключен через {minutes} мин.')
        except ValueError:
            QMessageBox.warning(self, 'Некорректный ввод', 'Введите число в минутах.')

    def stop_timer(self):
        if self.shutdown_scheduled:
            self.timer.stop()
            self.shutdown_scheduled = False
            os.system('shutdown -a')
            QMessageBox.information(self, 'Таймер выключен', 'Отключение компьютера отменено.')
        else:
            QMessageBox.warning(self, 'Таймер', 'В данный момент таймер выключения не запущен.')

    def shutdown_computer(self):
        os.system('shutdown /s /t 0')
        self.shutdown_scheduled = False


def main():
    app = QApplication(sys.argv)
    window = ShutdownTimerApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
