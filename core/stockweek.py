from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QEventLoop, QObject
from PyQt5 import QtCore
from enum import Enum
import json

from mylogging import Logging

from core.errorCode import errors
from core.strategy.buy.simple import SimpleBuyStrategy
from core.strategy.sell.simple import SimpleSellStrategy
from core.strategy import Strategy

from core.request import Request
from core.resource import Account, Market


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

        with open('config/config.json') as f:
            config = json.load(f)

        self.request = Request(self.kiwoom, self.detail_account_info_event_loop, config['ACCNO'])
        # self.receive = Receive(self.kiwoom)

        self.kiwoom.OnEventConnect.connect(self.login_slot)
        self.kiwoom.OnReceiveTrData.connect(self.trdata_slot)  # 트랜잭션 요청 관련 이벤트

        # 리소스 정의
        self.account = Account()
        self.market = Market()

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

    def trdata_slot(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
        self.logging("in trdata sRQName: " + sRQName)
        param = {'sScrNo': sScrNo, "sRQName": sRQName, "sTrCode": sTrCode, "sRecordName": sRecordName,
                 "sPrevNext": sPrevNext}
        try:
            if sRQName == "예수금상세현황요청":
                self.request.handle_detail_account_info(self.account, param)
                self.logging(str(f"deposit : {self.account.deposit}"))
                self.logging(str(f"예수금 : {self.account.output_deposit}"))
            elif sRQName == "계좌평가잔고내역요청":
                self.request.handle_detail_account_stock(self.account, param)

        except Exception as e:
            self.logging("err" + str(e))

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

    def manual_request(self, order_type, is_good_price, price, quantity):
        self.logging(f'order_type:{order_type} is_good_price:{is_good_price} price:{price} quantity:{quantity}')

    def request_load_account(self):
        account_list = self.kiwoom.dynamicCall("GetLoginInfo(QString)", "ACCNO")  # 계좌번호 반환
        account_num = account_list
        self.logging(f"account_list:{account_list}")

    def onclick_test_btn1(self):
        self.logging('onclick_test_btn1')
        try:
            account_no = self.request.load_account_num()
            self.logging(str(account_no))
            # code_list = self.request.get_code_list_by_market(0)
            # self.logging(str(code_list))
        except Exception as e:
            self.logging("except" + str(e))

    def onclick_test_btn2(self):
        self.logging('onclick_test_btn2')
        try:
            self.request.call_detail_account_info()
        except Exception as e:
            self.logging("except" + str(e))

    def onclick_test_btn3(self):
        self.logging('onclick_test_btn3')
        try:
            self.request.call_detail_account_stock()
        except Exception as e:
            self.logging("except" + str(e))
        self.logging(self.account.str_account_stock())