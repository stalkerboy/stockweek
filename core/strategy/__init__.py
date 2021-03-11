from PyQt5.QtCore import QThread
from PyQt5 import QtCore


class Strategy(QThread):
    strategyType = "기본"
    strategyName = "기본 Strategy Name"
    threadLogEvent = QtCore.pyqtSignal(str)

    def __init__(self, start_time=None, loop_time=1000*60*60, is_real_trading=False):
        super().__init__()
        self.start_time = start_time
        self.loop_time = 10000
        self._isRun = False
        self.is_real_trading = is_real_trading
        self.loop_cnt = 0

    def run(self):
        self.logging(self.strategyType + " Type : " + self.strategyName + " 실행")
        self._isRun = True

        while self._isRun:
            self.loop_cnt += 1
            # self.logging(self.strategyType + " Type : " + self.strategyName + " Loop 실행 " + str(self.loop_cnt))
            self.loop_run()
            self.sleep(self.loop_time)

    def stop(self):
        self._isRun = False

    def logging(self, msg):
        self.threadLogEvent.emit(msg)

    def loop_run(self):
        pass


class BuyStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.strategyType = "buy"


class SellStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.strategyType = "sell"
