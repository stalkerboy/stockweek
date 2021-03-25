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

        self.testBtn1.clicked.connect(self.onclick_test_btn1)
        self.testBtn2.clicked.connect(self.onclick_test_btn2)
        self.testBtn3.clicked.connect(self.onclick_test_btn3)

        self.goodCBtn.clicked.connect(self.onclick_good_btn)

        self.program.threadLogEvent.connect(self.logging)

    def initialize(self):
        pass

    def onclick_request_btn(self):
        if not (self.buyRBtn.isChecked() or self.sellRBtn.isChecked()) :
            QMessageBox.warning(self, "Error", "매매버튼을 선택하세요")
            return
        stock_code = self.stockEditText.text()
        trade_type = "buy" if self.buyRBtn.isChecked() else "sell"
        is_good_price = self.goodCBtn.isChecked()
        price = self.priceSpBox.value()
        quantity = self.quantitySpBox.value()

        self.program.manual_request(stock_code, trade_type, is_good_price, price, quantity)

    def onclick_test_btn1(self):
        self.program.onclick_test_btn1()

    def onclick_test_btn2(self):
        self.program.onclick_test_btn2()

    def onclick_test_btn3(self):
        self.program.onclick_test_btn3()

    def onclick_good_btn(self):
        self.priceSpBox.setEnabled(not self.goodCBtn.isChecked())

    def logging(self, log):
        self.logEditText.appendPlainText(log)
