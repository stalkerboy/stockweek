import sys
from PyQt5.QtWidgets import QApplication

from ui.mainui import MainUI

if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainUI = MainUI()

    mainUI.initialize()

    mainUI.show()

    app.exec_()
