import sys
import time

import serial
from PyQt5 import QtCore, QtWidgets

from morse import morse
from ui import Ui_MainWindow


class Controller:
    def __init__(self):
        self.thread = ArduinoThread()

    def run(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.display_window()
        self.init_send_btn()
        sys.exit(self.app.exec_())

    def display_window(self):
        self.main_win = QtWidgets.QMainWindow()
        self.view = Ui_MainWindow()
        self.view.setupUi(self.main_win)
        self.main_win.show()

    def init_send_btn(self):
        send_btn = SendButton(self.view, self.thread)
        send_btn.run()


class ArduinoThread(QtCore.QThread):

    message = None
    ui = None        

    def run(self):
        self.serial = serial.Serial('/dev/ttyACM0', 9600, timeout=0)
        if self.message is not None:
            self.operate_each_letters()
            self.ui.pushButton.setEnabled(True)

    def process_command(self, command: int, sleep: int):
        
        self.serial.write(b'0')
        time.sleep(0.7)

        if command == 1:
            self.serial.write(b'1')
            time.sleep(sleep)
        elif command == 2:
            self.serial.write(b'2')
            time.sleep(sleep)
        elif command == 3:
            self.serial.write(b'3')
            time.sleep(sleep)
        elif command == 4:
            self.serial.write(b'4')
            time.sleep(sleep)
        elif command == 5:
            self.serial.write(b'5')
            time.sleep(sleep)

    def operate_each_letters(self):
        for letter in self.message:            
            if letter == ' ':
                self.process_command(4, 1.5)

            if letter in morse:
                self.ui.label_2.setText(f"{letter}\n{' '.join(str(morse[letter]))}")
                self.light_each_letter(letter)

        self.process_command(5, 1)

    def light_each_letter(self, letter: str):
        if letter == ' ':
            return

        for value in morse[letter]:
            self.process_command(value, .7)

        self.process_command(3, 1.5)

    def close(self):
        self.serial.close()




class SendButton:
    def __init__(self, ui, thread):
        self.ui = ui
        self.thread = thread

    def run(self):
        self.connect_btn()

    def connect_btn(self):
        ReconnectSignal.reconnect(
            signal=self.ui.pushButton.clicked,
            newhandler=lambda: self.send_cmd()
        )

    def send_cmd(self):
        text = self.ui.lineEdit.text().strip().upper()
        if not text:
            return

        # clear the text edit
        self.ui.textEdit.clear()

        # remove special characters from the text
        result_str = self.remove_all_special_characters(text)
        # clear the line edit
        self.ui.lineEdit.clear()
        # display to text edit
        self.ui.textEdit.insertPlainText(result_str)
        # display 1 by 1 to label
        self.run_arduino(result_str)   

    def remove_all_special_characters(self, message: str):
        allowed_chars = list(range(32, 127))
        return ''.join([c for c in message if ord(c) in allowed_chars])

    def run_arduino(self, message):
        self.ui.pushButton.setEnabled(False)
        self.worker = ArduinoThread()
        self.worker.message = message
        self.worker.ui = self.ui
        self.worker.start()
        

class ReconnectSignal:

    def reconnect(signal, newhandler=None, oldhandler=None):        
        try:
            if oldhandler is not None:
                while True:
                    signal.disconnect(oldhandler)
            else:
                signal.disconnect()
        except TypeError:
            pass
        if newhandler is not None:
            signal.connect(newhandler)

def main():
    controller = Controller()
    controller.run()

if __name__ == "__main__":
    main()