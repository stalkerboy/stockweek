from core.resource import Account, Market
from core.stock import AccountStock, OrderStock, MarketStock, OrderType


class Request:
    def __init__(self, program, event_loop, account_num):
        self.program = program
        self.event_loop = event_loop
        self.screen_my_info = 2000
        self.account_num = account_num

    def get_account_num(self):
        account_list = self.program.dynamicCall("GetLoginInfo(QString)", "ACCNO")  # 계좌번호 반환
        account_num = account_list.split(';')[0]
        self.account_num = account_num
        return account_num

    # 예수금상세현황요청
    def call_detail_account_info(self, sPrevNext="0"):
        self.program.dynamicCall("SetInputValue(QString, QString)", "계좌번호", self.account_num)
        self.program.dynamicCall("SetInputValue(QString, QString)", "비밀번호", "0000")
        self.program.dynamicCall("SetInputValue(QString, QString)", "비밀번호입력매체구분", "00")
        self.program.dynamicCall("SetInputValue(QString, QString)", "조회구분", "1")
        self.program.dynamicCall("CommRqData(QString, QString, int, QString)", "예수금상세현황요청", "opw00001",
                                 sPrevNext, self.screen_my_info)
        self.event_loop.exec_()

    def handle_detail_account_info(self, account: Account, param):
        sTrCode = param['sTrCode']
        sRQName = param['sRQName']
        deposit = self.program.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "예수금")
        account.deposit = int(deposit)

        use_money = float(account.deposit) * account.use_money_percent
        account.use_money = int(use_money)
        account.use_money = account.use_money / 4

        output_deposit = self.program.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0,
                                                  "출금가능금액")
        account.output_deposit = int(output_deposit)

        self.stop_screen_cancel(self.screen_my_info)

        self.event_loop.exit()

    # 계좌평가잔고내역요청
    def call_detail_account_stock(self, sPrevNext="0"):
        self.program.dynamicCall("SetInputValue(QString, QString)", "계좌번호", self.account_num)
        self.program.dynamicCall("SetInputValue(QString, QString)", "비밀번호", "0000")
        self.program.dynamicCall("SetInputValue(QString, QString)", "비밀번호입력매체구분", "00")
        self.program.dynamicCall("SetInputValue(QString, QString)", "조회구분", "1")
        self.program.dynamicCall("CommRqData(QString, QString, int, QString)", "계좌평가잔고내역요청", "opw00018",
                                 sPrevNext, self.screen_my_info)
        self.event_loop.exec_()

    def handle_detail_account_stock(self, account: Account, param):
        sTrCode = param['sTrCode']
        sRQName = param['sRQName']
        sPrevNext = param['sPrevNext']
        total_buy_money = self.program.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0,
                                                   "총매입금액")
        account.total_buy_money = int(total_buy_money)
        total_profit_loss_money = self.program.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode,
                                                           sRQName, 0,
                                                           "총평가손익금액")
        account.total_profit_loss_money = int(total_profit_loss_money)
        total_profit_loss_rate = self.program.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode,
                                                          sRQName, 0,
                                                          "총수익률(%)")
        account.total_profit_loss_rate = float(total_profit_loss_rate)

        rows = self.program.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRQName)
        for i in range(rows):
            code = self.program.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                            "종목번호")  # 출력 : A039423 // 알파벳 A는 장내주식, J는 ELW종목, Q는 ETN종목
            code = code.strip()[1:]

            code_nm = self.program.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                               "종목명")  # 출럭 : 한국기업평가
            stock_quantity = self.program.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName,
                                                      i, "보유수량")  # 보유수량 : 000000000000010
            buy_price = self.program.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                                 "매입가")  # 매입가 : 000000000054100
            learn_rate = self.program.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                                  "수익률(%)")  # 수익률 : -000000001.94
            current_price = self.program.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                                     "현재가")  # 현재가 : 000000003450
            total_chegual_price = self.program.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode,
                                                           sRQName, i, "매입금액")
            possible_quantity = self.program.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode,
                                                         sRQName, i, "매매가능수량")

            stock = AccountStock()
            stock.code_nm = code_nm.strip()
            stock.stock_quantity = int(stock_quantity.strip())
            stock.buy_price = int(buy_price.strip())
            stock.earning_rate = float(learn_rate.strip())
            stock.current_price = int(current_price.strip())
            stock.total_purchase_price = int(total_chegual_price.strip())
            stock.possible_quantity = int(possible_quantity.strip())

            account.account_stock_dict.update({code: stock})

        if sPrevNext == "2":
            self.call_detail_account_stock(sPrevNext="2")
        else:
            self.event_loop.exit()

    def call_detail_account_outstanding(self, sPrevNext="0"):
        self.program.dynamicCall("SetInputValue(QString, QString)", "계좌번호", self.account_num)
        self.program.dynamicCall("SetInputValue(QString, QString)", "체결구분", "1")
        self.program.dynamicCall("SetInputValue(QString, QString)", "매매구분", "0")
        self.program.dynamicCall("CommRqData(QString, QString, int, QString)", "실시간미체결요청", "opt10075",
                                 sPrevNext, self.screen_my_info)
        self.event_loop.exec_()

    def handle_detail_account_outstanding(self, account: Account, param):
        pass

    def call_send_order_buy(self, stock: OrderStock):
        if stock.orderType != OrderType.BUYING:
            return
        pass
        # order_success = self.dynamicCall(
        #     "SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
        #     ["신규매수", self.portfolio_stock_dict[sCode]["주문용스크린번호"], self.account_num, 1, sCode, quantity, e,
        #      self.realType.SENDTYPE['거래구분']['지정가'], ""]
        # )
        #
        # if order_success == 0:
        #     self.logging.logger.debug("매수주문 전달 성공")
        # else:
        #     self.logging.logger.debug("매수주문 전달 실패")

    def get_code_list_by_market(self, market_code):
        """
        종목코드 리스트 받기
        #0:장내, 10:코스닥

        :param market_code: 시장코드 입력
        :return:
        """
        code_list = self.program.dynamicCall("GetCodeListByMarket(QString)", market_code)
        # code_list = code_list.split(';')[:-1]

        return code_list

    def stop_screen_cancel(self, sScrNo=None):
        self.program.dynamicCall("DisconnectRealData(QString)", sScrNo)  # 스크린번호 연결 끊기
