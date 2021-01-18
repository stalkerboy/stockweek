import sys
from core import *


class StockWeek:
    def __init__(self, argv):
        if len(argv) > 1:
            if argv[1] == "-d":
                logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)
        logging.debug("StockWeek started")

        Account()
        Market()
        AccountStock()
        OrderStock()
        MarketStock()


if __name__ == "__main__":
    StockWeek(sys.argv)
