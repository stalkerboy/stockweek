import sys
from PyQt5.QtWidgets import QDialog, QInputDialog, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import Qt

form_class = uic.loadUiType("ui/manual.ui")[0]


class ManualUI(QDialog, form_class):
    def __init__(self, program):
        super().__init__()
        self.setupUi(self)
        self.program = program

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        # self.buyRBtn.clicked.connect(self.onclick_choice_radio)
        # self.sellRBtn.clicked.connect(self.onclick_choice_radio)

        # button binding
        self.requestBtn.clicked.connect(self.onclick_request_btn)

        self.program.threadLogEvent.connect(self.logging)

    def initialize(self):
        pass

    def onclick_request_btn(self):
        if not (self.buyRBtn.isChecked() or self.sellRBtn.isChecked()) :
            QMessageBox.warning(self, "Error", "매매버튼을 선택하세요")
            return
        trade_type = "buy" if self.buyRBtn.isChecked() else "sell"
        is_good_price = self.goodCBtn.isChecked()
        price = self.priceSpBox.value()
        # self.program.manual_request(type, is_good_price, price )
        QMessageBox.information(self, "request", f'trade_type:{trade_type} is_good_price:{is_good_price} price:{price}')

    def logging(self, log):
        self.logEditText.appendPlainText(log)
