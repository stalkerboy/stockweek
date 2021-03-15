import sys
from PyQt5.QtWidgets import QMainWindow, QInputDialog
from PyQt5.QtGui import QIcon
from PyQt5 import uic

from core.stockweek import RunningState, StockWeek
from ui.manual import ManualUI

form_class = uic.loadUiType("ui/main.ui")[0]


class MainUI(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('img/iconH.png'))

        # button binding
        self.loginBtn.clicked.connect(self.onclick_login_btn)
        self.startBtn.clicked.connect(self.onclick_start_btn)
        self.pauseBtn.clicked.connect(self.onclick_pause_btn)
        self.stopBtn.clicked.connect(self.onclick_stop_btn)

        self.buyBtn.clicked.connect(self.onclick_buy_btn)
        self.sellBtn.clicked.connect(self.onclick_sell_btn)

        self.manualBtn.clicked.connect(self.onclick_manual_btn)

        self.program = StockWeek()
        self.program.threadLogEvent.connect(self.logging)
        self.program.threadStateEvent.connect(self.change_state_btn)

    def initialize(self):
        init_buy_strategy = "simpleBuy"
        init_sell_strategy = "simpleSell"
        self.program.change_buy_strategy(init_buy_strategy)
        self.buyLabel.setText(init_buy_strategy)
        self.program.change_sell_strategy(init_sell_strategy)
        self.sellLabel.setText(init_sell_strategy)

    def set_program(self, program):
        self.program = program

    def onclick_login_btn(self, event):
        self.program.login()

    def onclick_start_btn(self, event):
        self.program.run()

    def onclick_stop_btn(self):
        self.program.stop()

    def onclick_pause_btn(self):
        self.program.pause()

    def onclick_buy_btn(self):
        items = self.program.strategy_list['buy'].keys()
        item, ok = QInputDialog.getItem(self, "select buy strategy",
                                        "list of strategy", items, 0, False)
        if ok and item:
            self.program.change_buy_strategy(item)
            self.buyLabel.setText(item)

    def onclick_sell_btn(self):
        items = self.program.strategy_list['sell'].keys()
        item, ok = QInputDialog.getItem(self, "select sell strategy",
                                        "list of strategy", items, 0, False)
        if ok and item:
            self.program.change_sell_strategy(item)
            self.sellLabel.setText(item)

    def onclick_manual_btn(self):
        manual_ui = ManualUI(self.program)
        manual_ui.exec_()

    def change_state_btn(self, running_state):
        self.loginBtn.setEnabled(False)
        self.startBtn.setEnabled(False)
        self.stopBtn.setEnabled(False)
        self.pauseBtn.setEnabled(False)

        self.buyBtn.setEnabled(False)
        self.sellBtn.setEnabled(False)

        self.manualBtn.setEnabled(False)

        if running_state == RunningState.STOP:
            self.loginBtn.setEnabled(True)
            self.buyBtn.setEnabled(True)
            self.sellBtn.setEnabled(True)
        elif running_state == RunningState.READY:
            self.startBtn.setEnabled(True)
            self.stopBtn.setEnabled(True)
            self.buyBtn.setEnabled(True)
            self.sellBtn.setEnabled(True)
            self.manualBtn.setEnabled(True)
        elif running_state == RunningState.RUNNING:
            self.stopBtn.setEnabled(True)
            self.pauseBtn.setEnabled(True)
        elif running_state == RunningState.ERROR:
            self.stopBtn.setEnabled(True)
        else:
            self.stopBtn.setEnabled(True)

        self.runningLabel.setText(running_state.value)
        self.logging(running_state.value)

    def logging(self, log):
        self.logEditText.appendPlainText(log)


