import sys
from random import randint
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.mainWidget = QWidget()
        self.mainVBox = QVBoxLayout(self.mainWidget)
        self.setCentralWidget(self.mainWidget)

        btn = QPushButton("Click Me", self)
        btn.clicked.connect(lambda: self.openDialog())
        self.mainVBox.addWidget(btn, alignment=Qt.AlignCenter)

        self.show()

    def openDialog(self):
        dialog = Dialog(self)
        dialog.show()


class Dialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        dialog_vlayout = QVBoxLayout(self)
        dialog_hlayout = QHBoxLayout()

        self.display = QLabel("Would you like to stay here with me?")
        dialog_vlayout.addWidget(self.display)

        stay_button = QPushButton("Stay Here", self)
        quit_button = QPushButton("Quit", self)
        stay_button.clicked.connect(self.stayHere)
        quit_button.clicked.connect(self.reject)

        dialog_hlayout.addWidget(stay_button)
        dialog_hlayout.addWidget(quit_button)
        dialog_vlayout.addLayout(dialog_hlayout)

    def stayHere(self):
        text = ["Yay! Thanks for staying with me!", "You are really staying with me?", "I am so happy that you are staying here!"]
        self.display.setText(text[randint(0,2)])




if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()

    sys.exit(app.exec_())