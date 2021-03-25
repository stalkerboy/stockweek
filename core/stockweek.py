from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QEventLoop, QObject
from PyQt5 import QtCore
import json

from mylogging import Logging

from core.errorCode import errors
from core.strategy.buy.simple import SimpleBuyStrategy
from core.strategy.sell.simple import SimpleSellStrategy
from core.strategy import Strategy

from core.resource import Account, Market
from core.runningstate import RunningState

from api.hughkiwoom import HughKiwoom


class StockWeek(QObject):
    threadLogEvent = QtCore.pyqtSignal(str)
    threadStateEvent = QtCore.pyqtSignal(RunningState)

    def __init__(self):
        super().__init__()
        self.logger = Logging().logger
        self.runningState = RunningState.STOP
        self.kiwoom: HughKiwoom = HughKiwoom(self, False)
        self.strategy_list = {"buy": {"simpleBuy": SimpleBuyStrategy}, "sell": {"simpleSell": SimpleSellStrategy}}
        self.buy_strategy = Strategy()
        self.sell_strategy = Strategy()

        with open('config/config.json') as f:
            config = json.load(f)

        # 리소스 정의
        self.account = Account()
        self.market = Market()

        # 로그인 요청용 이벤트루프
        # self.login_event_loop = QEventLoop()

    def login(self):
        self.kiwoom.CommConnect(True)
        # self.login_event_loop.exec_()

    def handler_login(self, err_code):
        self.logging(errors(err_code)[1])
        # self.login_event_loop.exit()
        if errors(err_code)[1] == '정상처리':
            self.change_running_state(RunningState.READY)
        else:
            self.change_running_state(RunningState.ERROR)

    def handler_tr(self, screen, rqname, trcode, record, next):
        pass

    def run(self):
        self.change_running_state(RunningState.RUNNING)

        # self.detail_account_info_event_loop.exec_()

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

    def logging(self, log):
        self.logger.debug(str(log))
        self.threadLogEvent.emit(str(log))
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

    def manual_request(self, stock_code, order_type, is_good_price, price, quantity):
        try:
            self.logging(
                f'"stock_code:{stock_code} order_type:{order_type} is_good_price:{is_good_price} price:{price} quantity:{quantity}')
            # "005930"

            # 계좌번호는 11을 붙여서 10자리임
            account_list = self.kiwoom.GetLoginInfo("ACCNO")
            account = account_list[0]
            # opw00001 요청
            df = self.kiwoom.block_request("opw00001", 계좌번호=account, 비밀번호="", 비밀번호입력매체구분="00",
                                           조회구분=1, output="예수금상세현황", next=0)

            # 예수금
            # 예수금 = int(df['예수금'][0])
            # print(예수금)
            # print(df)
            for column in df.columns:
                print(column, df.loc[0][column])
        except Exception as e:
            self.logging("except" + str(e))

    def request_load_account(self):
        account_list = self.kiwoom.GetLoginInfo("ACCNO")  # 계좌번호 반환
        self.logging(f"account_list:{account_list}")

    def onclick_test_btn1(self):
        self.logging('onclick_test_btn1')
        try:
            account_no = self.kiwoom.GetLoginInfo("ACCNO")
            self.logging(str(account_no))
            # code_list = self.request.get_code_list_by_market(0)
            # self.logging(str(code_list))
        except Exception as e:
            self.logging("except" + str(e))

    def onclick_test_btn2(self):
        self.logging('onclick_test_btn2')
        try:
            account_no = self.kiwoom.GetLoginInfo("ACCOUNT_CNT")
            self.logging(str(account_no))
            account_no = self.kiwoom.GetLoginInfo("USER_ID")
            self.logging(str(account_no))
        except Exception as e:
            self.logging("except" + str(e))

    def onclick_test_btn3(self):
        self.logging('onclick_test_btn3')
        try:
            print(self.kiwoom.GetLoginInfo("ACCNO"))
            print(self.kiwoom.ocx.dynamicCall("GetLoginInfo(QString)", "ACCNO"))
            print(self.kiwoom.connected)
        except Exception as e:
            self.logging("except" + str(e))
        self.logging(self.account.str_account_stock())
