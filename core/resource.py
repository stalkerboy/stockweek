from core.stock import AccountStock, OrderStock, MarketStock


class Market:
    def __init__(self):
        pass
        # self.marketStock = MarketStock()


class Account:
    def __init__(self):
        self.deposit = None  # 예수금
        self.output_deposit = None  # 출금가능금액

        self.use_money = None
        self.use_money_percent = 0.1

        self.total_buy_money = None  # 총매입금액
        self.total_profit_loss_money = None  # 총평가손익금액
        self.total_profit_loss_rate = None  # 총수익률(%)

        self.account_stock_dict = {}
        # self.accountStock = AccountStock()
        # self.orderStock = OrderStock()

    def str_account_stock(self):
        out_str = ''
        for code, stock in self.account_stock_dict.items():
            out_str += str(stock) + '\t'
        return out_str




