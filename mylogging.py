import logging.config
from datetime import datetime


class Logging:
    def __init__(self):
        '''
        logging.config.fileConfig('config/logging.conf')

        fh = logging.FileHandler('log/{:%Y-%m-%d}.log'.format(datetime.now()), encoding="utf-8")
        # formatter = logging.Formatter('[%(asctime)s] I %(filename)s |  %(name)s  > %(message)s')
        formatter = logging.Formatter('[%(asctime)s] | %(name)s  > %(message)s')

        fh.setFormatter(formatter)
        self.logger = logging.getLogger('Kiwoom')
        self.logger.addHandler(fh)
        '''
        logging.config.fileConfig('config/logging.conf')

        fh = logging.FileHandler('log/{:%Y-%m-%d}.log'.format(datetime.now()), encoding="utf-8")
        # formatter = logging.Formatter('[%(asctime)s] I %(filename)s |  %(name)s  > %(message)s')
        formatter = logging.Formatter('[%(asctime)s] | %(name)s  > %(message)s')

        fh.setFormatter(formatter)

        logging.basicConfig(handlers=fh)

        self.logger = logging.getLogger()
        self.logger.addHandler(fh)
