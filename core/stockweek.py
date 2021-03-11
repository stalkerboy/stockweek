from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QEventLoop, QObject
from PyQt5 import QtCore
from enum import Enum

from mylogging import Logging

from core.errorCode import errors
from core.strategy.buy.simple import SimpleBuyStrategy
from core.strategy.sell.simple import SimpleSellStrategy
from core.strategy import Strategy

from core.stock import AccountStock, OrderStock, MarketStock


class RunningState(Enum):
    STOP = '정지'
    READY = '준비중'
    RUNNING = '동작중'
    ERROR = '에러'


class StockWeek(QObject):
    threadLogEvent = QtCore.pyqtSignal(str)
    threadStateEvent = QtCore.pyqtSignal(RunningState)

    def __init__(self):
        super().__init__()
        self.logger = Logging().logger
        self.runningState = RunningState.STOP
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.strategy_list = {"buy": {"simpleBuy": SimpleBuyStrategy}, "sell": {"simpleSell": SimpleSellStrategy}}
        self.buy_strategy = Strategy()
        self.sell_strategy = Strategy()
        # 로그인 요청용 이벤트루프
        self.login_event_loop = QEventLoop()

        self.detail_account_info_event_loop = QEventLoop()  # 예수금 요청용 이벤트루프

        self.kiwoom.OnEventConnect.connect(self.login_slot)
        self.kiwoom.OnReceiveTrData.connect(self.trdata_slot)  # 트랜잭션 요청 관련 이벤트

        self.accountStock = AccountStock()
        self.accountStock = OrderStock()
        self.accountStock = MarketStock()

    def login(self):
        self.kiwoom.dynamicCall("CommConnect()")
        self.logging('로그인 시도')
        # 이벤트루프 실행
        self.login_event_loop.exec_()

    def run(self):
        self.change_running_state(RunningState.RUNNING)

        self.detail_account_info_event_loop.exec_()

        self.buy_strategy.start()
        self.sell_strategy.start()

    def stop(self):
        self.buy_strategy.stop()
        self.sell_strategy.stop()
        self.change_running_state(RunningState.STOP)

    def pause(self):
        self.buy_strategy.stop()
        self.sell_strategy.stop()
        self.change_running_state(RunningState.READY)

    def login_slot(self, err_code):
        self.logging(errors(err_code)[1])
        if errors(err_code)[1] == '정상처리':
            self.change_running_state(RunningState.READY)
        else:
            self.change_running_state(RunningState.ERROR)

        self.login_event_loop.exit()

    def trdata_slot(self, err_code):
        pass

    def logging(self, log):
        self.logger.debug(log)
        self.threadLogEvent.emit(log)
        # self.ui.logging(log)

    def change_running_state(self, state):
        if isinstance(state, RunningState):
            self.runningState = state
            self.logging("state 변경 : " + self.runningState.value)
            self.threadStateEvent.emit(self.runningState)
            # self.ui.change_state_btn(self.runningState)

    def change_buy_strategy(self, name):
        if self.runningState != RunningState.STOP and self.runningState != RunningState.READY:
            self.logging("Stop Pause 후 변경 : 현재상태:" + self.runningState.value)
            return

        self.buy_strategy = self.strategy_list['buy'][name]()
        self.buy_strategy.threadLogEvent.connect(self.logging)
        self.logging("매수전략 변경 : " + name)

    def change_sell_strategy(self, name):
        if self.runningState != RunningState.STOP and self.runningState != RunningState.READY:
            self.logging("Stop Pause 후 변경 : 현재상태:" + self.runningState.value)
            return

        self.sell_strategy = self.strategy_list['sell'][name]()
        self.sell_strategy.threadLogEvent.connect(self.logging)
        self.logging("매매전략 변경 : " + name)

    def manual_request(self, trade_type, is_good_price, price):
        pass
