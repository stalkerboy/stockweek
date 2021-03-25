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
        self.type: StockType = None
        self.code = None
        self.code_nm = None
        self.current_price = None  # 현재가
        self.current_time = None
        self.screen_real_stock = None  # 스크린번호
        self.screen_meme_stock = None  # 주문용스크린번호


class AccountStock(Stock):
    def __init__(self):
        super().__init__()
        self.type = StockType.ACCOUNT
        self.quantity = None
        self.buy_price = None  # 매입가
        self.earning_rate = None  # 수익률(%)
        self.total_purchase_price = None  # 총 매입금액
        self.possible_quantity = None  # 매입 가능 갯수


class OrderStock(Stock):
    def __init__(self):
        super().__init__()
        self.type = StockType.ORDER
        self.orderType: OrderType = None
        self.quantity = None


class MarketStock(Stock):
    def __init__(self):
        super().__init__()
        self.type = StockType.ORDER
