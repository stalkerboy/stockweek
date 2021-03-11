from enum import Enum


class StockType(Enum):
    ACCOUNT = '계좌주식'
    ORDER = '주문주식'
    MARKET = '시장주식'


class OrderType(Enum):
    BUYING = '매수주문'
    CANCEL_BUYING = '매수주문취소'
    SELLING = '매도주문'
    CANCEL_SELLING = '매도주문취소'


class Stock:
    def __init__(self):
        self.code = None
        self.name = None
        self.type = None
        self.price = None
        self.date = None


class AccountStock(Stock):
    def __init__(self):
        super().__init__()
        self.type = StockType.ACCOUNT
        self.quantity = None


class OrderStock(Stock):
    def __init__(self):
        super().__init__()
        self.type = StockType.ORDER
        self.orderType = None
        self.quantity = None


class MarketStock(Stock):
    def __init__(self):
        super().__init__()
        self.type = StockType.ORDER
