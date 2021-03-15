
class Request:
    def __init__(self, kiwoom, event_loop, account_num):
        self.kiwoom = kiwoom
        self.event_loop = event_loop
        self.screen_my_info = 2000
        self.account_num = account_num

    def load_account_num(self):
        account_list = self.kiwoom.dynamicCall("GetLoginInfo(QString)", "ACCNO")  # 계좌번호 반환
        account_num = account_list.split(';')[0]
        self.account_num = account_num

    def call_detail_account_info(self, sPrevNext="0"):
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "계좌번호", self.account_num)
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "비밀번호", "0000")
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "비밀번호입력매체구분", "00")
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "조회구분", "1")
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "예수금상세현황요청", "opw00001",
                                sPrevNext, self.screen_my_info)
        self.event_loop.exec_()

    def call_detail_account_stock(self, sPrevNext="0"):
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "계좌번호", self.account_num)
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "비밀번호", "0000")
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "비밀번호입력매체구분", "00")
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "조회구분", "1")
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "계좌평가잔고내역요청", "opw00018",
                                sPrevNext, self.screen_my_info)
        self.event_loop.exec_()

    def call_detail_account_outstanding(self, sPrevNext="0"):
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "계좌번호", self.account_num)
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "체결구분", "1")
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "매매구분", "0")
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "실시간미체결요청", "opt10075",
                                sPrevNext, self.screen_my_info)
        self.event_loop.exec_()

    def get_code_list_by_market(self, market_code):
        """
        종목코드 리스트 받기
        #0:장내, 10:코스닥

        :param market_code: 시장코드 입력
        :return:
        """
        code_list = self.kiwoom.dynamicCall("GetCodeListByMarket(QString)", market_code)
        # code_list = code_list.split(';')[:-1]

        return code_list

