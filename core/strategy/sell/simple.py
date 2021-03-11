from core.strategy import SellStrategy


class SimpleSellStrategy(SellStrategy):
    def __init__(self):
        super().__init__()
        self.strategyName = "SimpleSell"
