


import traceback
# run this pyuic5 Gui.ui -o gui.py
from PyQt5 import QtWidgets, uic
from gui import Ui_MainWindow  # importing our generated file
import sys
qtCreatorFile = "Gui.ui"


class Gui_App(QtWidgets.QMainWindow):
    # signal_check_logical = QtCore.pyqtSignal(int)
    # signal_check_process = QtCore.pyqtSignal(int)
    # signal_check_raw = QtCore.pyqtSignal(int)
    # signal_ = QtCore.pyqtSignal(int)

    def __init__(self):
        try:
            #win = uic.loadUi(qtCreatorFile)  # specify the location of your .ui file
            super(Gui_App, self).__init__()
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            # self.ui.pushButton.setText('***')
        except:
            traceback.print_exc()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = Gui_App()
    application.show()
    # win = uic.loadUi(qtCreatorFile)  # specify the location of your .ui file
    # win.show()
    sys.exit(app.exec())