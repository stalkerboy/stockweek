from core.strategy import BuyStrategy


class SimpleBuyStrategy(BuyStrategy):
    def __init__(self):
        super().__init__()
        self.strategyName = "SimpleBuy"

    def loop_run(self):
        super().loop_run()
