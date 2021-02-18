import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5 import uic
import logging.config
from datetime import datetime
from core.stockweek import StockWeek, RunningState

form_class = uic.loadUiType("ui/main.ui")[0]


# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('img/iconH.png'))

        # button binding
        self.loginBtn.clicked.connect(self.onclick_login_btn)
        self.startBtn.clicked.connect(self.onclick_start_btn)
        self.stopBtn.clicked.connect(self.onclick_stop_btn)

        # self.logEditText.setPlainText("에디티텍스트")

        logging.config.fileConfig('config/logging.conf')

        fh = logging.FileHandler('log/{:%Y-%m-%d}.log'.format(datetime.now()), encoding="utf-8")
        formatter = logging.Formatter('[%(asctime)s] I %(filename)s |  %(name)s  > %(message)s')

        fh.setFormatter(formatter)
        self.logger = logging.getLogger('Kiwoom')
        self.logger.addHandler(fh)

        self.logging('started')
        self.stockweek = StockWeek(self.logging)
        self.change_state_btn()

    def logging(self, log):
        self.logger.debug(log)
        self.logEditText.appendPlainText(log)

    def onclick_login_btn(self, event):
        self.stockweek.login()
        self.change_state_btn()
        # QMessageBox.information(self, 'Message', 'login_btn')

    def onclick_start_btn(self, event):
        QMessageBox.information(self, 'Message', 'start_btn')

    def onclick_stop_btn(self):
        QMessageBox.information(self, 'Message', 'stop_Btn')

    def change_state_btn(self):
        self.loginBtn.setEnabled(False)
        self.startBtn.setEnabled(False)
        self.stopBtn.setEnabled(False)
        if self.stockweek.runningState == RunningState.STOP:
            self.loginBtn.setEnabled(True)
        elif self.stockweek.runningState == RunningState.READY:
            self.startBtn.setEnabled(True)
        elif self.stockweek.runningState == RunningState.RUNNING:
            self.stopBtn.setEnabled(True)
        elif self.stockweek.runningState == RunningState.ERROR:
            self.stopBtn.setEnabled(True)
        else:
            self.stopBtn.setEnabled(True)

        self.runningLabel.setText(self.stockweek.runningState.value)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
