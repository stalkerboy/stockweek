from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QEventLoop
from enum import Enum

from core.errorCode import errors


class RunningState(Enum):
    STOP = '정지'
    READY = '준비중(로그인완료)'
    RUNNING = '동작중'
    ERROR = '에러 비정상종료'


class StockWeek:
    def __init__(self, logging):
        self.logging = logging
        self.runningState = RunningState.STOP
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        # 로그인 요청용 이벤트루프
        self.login_event_loop = QEventLoop()

        self.kiwoom.OnEventConnect.connect(self.login_slot)

    def login(self):
        self.kiwoom.dynamicCall("CommConnect()")
        self.logging('로그인 시도')
        # 이벤트루프 실행
        self.login_event_loop.exec_()

    def login_slot(self, err_code):
        self.logging(errors(err_code)[1])
        if errors(err_code)[1] == '정상처리':
            self.runningState = RunningState.READY
        else:
            self.runningState = RunningState.ERROR

        self.login_event_loop.exit()
