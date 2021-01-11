import os
import sys
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from config.errorCode import *
from PyQt5.QtTest import *
from config.kiwoomType import *
from config.log_class import *
from config.slack import *


class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self.realType = RealType()
        self.logging = Logging()
        self.slack = Slack() #슬랙 동작

        #print("kiwoom() class start. ")
        self.logging.logger.debug("Kiwoom() class start.")

        ####### event loop를 실행하기 위한 변수모음
        self.login_event_loop = QEventLoop() #로그인 요청용 이벤트루프
        self.detail_account_info_event_loop = QEventLoop() # 예수금 요청용 이벤트루프
        self.calculator_event_loop = QEventLoop()
        #########################################

        ########### 전체 종목 관리
        self.all_stock_dict = {}
        ###########################


        ####### 계좌 관련된 변수
        self.account_stock_dict = {}
        self.not_account_stock_dict = {}
        self.deposit = 0 #예수금
        self.use_money = 0 #실제 투자에 사용할 금액
        self.use_money_percent = 0.5 #예수금에서 실제 사용할 비율
        self.output_deposit = 0 #출력가능 금액
        self.total_profit_loss_money = 0 #총평가손익금액
        self.total_profit_loss_rate = 0.0 #총수익률(%)
        ########################################

        ######## 종목 정보 가져오기
        self.portfolio_stock_dict = {}
        self.jango_dict = {}
        ########################

        ########### 종목 분석 용
        self.calcul_data = []
        ##########################################


        ####### 요청 스크린 번호
        self.screen_my_info = "2000" #계좌 관련한 스크린 번호
        self.screen_calculation_stock = "4000" #계산용 스크린 번호
        self.screen_real_stock = "5000" #종목별 할당할 스크린 번호
        self.screen_meme_stock = "6000" #종목별 할당할 주문용스크린 번호
        self.screen_start_stop_real = "1000" #장 시작/종료 실시간 스크린번호
        ########################################

        ######### 초기 셋팅 함수들 바로 실행
        self.get_ocx_instance() #OCX 방식을 파이썬에 사용할 수 있게 변환해 주는 함수
        self.event_slots() # 키움과 연결하기 위한 시그널 / 슬롯 모음
        self.real_event_slot()  # 실시간 이벤트 시그널 / 슬롯 연결
        self.signal_login_commConnect() #로그인 요청 시그널 포함
        self.get_account_info() #계좌번호 가져오기

        self.detail_account_info() #예수금 요청 시그널 포함
        self.detail_account_mystock() #계좌평가잔고내역 요청 시그널 포함
        QTimer.singleShot(5000, self.not_concluded_account) #5초 뒤에 미체결 종목들 가져오기 실행
        #########################################

        QTest.qWait(10000)
        self.read_code()
        self.screen_number_setting()


        QTest.qWait(5000)

        #실시간 수신 관련 함수
        self.dynamicCall("SetRealReg(QString, QString, QString, QString)", self.screen_start_stop_real, '', self.realType.REALTYPE['장시작시간']['장운영구분'], "0")

        for code in self.portfolio_stock_dict.keys():
            screen_num = self.portfolio_stock_dict[code]['스크린번호']
            fids = self.realType.REALTYPE['주식체결']['체결시간']
            self.dynamicCall("SetRealReg(QString, QString, QString, QString)", screen_num, code, fids, "1")


        self.slack.notification(
            pretext="주식자동화 프로그램 동작",
            title="주식 자동화 프로그램 동작",
            fallback="주식 자동화 프로그램 동작",
            text="주식 자동화 프로그램이 동작 되었습니다."
        )