import sys
import time
import math

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#from rand_variable import RandomVariable
from DialogWindow import DialogWindow

#GLOBAL VARIABLES
WIN_HEIGHT = 400
WIN_WIDTH = 670
homeMSG = "This is a Random Variable calculator developed by Josef Yi.\n\n" \
          "Please select the type of Random Variable you would like to use."



# LOCAL FUNCTIONS


# CLASSES IN SESSION
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # setting up the main window
        #exitAct = QAction(QIcon('anime.png'), '&Exit', self)
        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        urvAct = QAction('&Uniform Random Variable', self)
        urvAct.setShortcut('Ctrl+U')
        urvAct.setStatusTip('Calculate Uniform Discrete Random Variable')
        urvAct.triggered.connect(lambda: self.parameterDialog('Uniform Random Variable', ['n']))


        self.statusBar()
        self.statusBar().showMessage('Ready')

        # Setting up the menu
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)
        toolsMenu = menubar.addMenu('&Tools')
        toolsMenu.addAction(urvAct)

        self.setFixedSize(WIN_WIDTH, WIN_HEIGHT)
        self.statusBar().setSizeGripEnabled(False)
        self.center()
        self.move(self.x()-100, self.y())
        self.setWindowTitle('Random Variable Calculator')
        #self.setWindowIcon(QIcon('anime.png'))


        # setting up the main widget
        # -- setting the central widget of the main window
        self.calcWidget = QWidget(self)
        self.setCentralWidget(self.calcWidget)

        # -- setting the VBOX layout
        self.mainVBox = QVBoxLayout(self.calcWidget)
        self.setLayout(self.mainVBox)

        # -- setting the display label
        self.displayLabel = QLabel()
        self.displayLabel.setStyleSheet("color: white; background-color:gray; "
                                        "padding: 24px 8px 24px 8px;")
        self.displayLabel.setAlignment(Qt.AlignHCenter)
        self.mainVBox.addWidget(self.displayLabel)
        self.mainVBox.addStretch(1)

        # Set up the home message
        self.displayLabel.setText(homeMSG)

        # -- setting the cute anime png
        self.img1 = QLabel(self)
        anime_thinking_img = QPixmap('math_think.png').scaledToHeight(210)
        self.img1.setPixmap(anime_thinking_img)
        self.img1.resize(anime_thinking_img.width() ,anime_thinking_img.height())
        self.img1.move(20, 150)


        # -- setting the btns frames
        self.btnHBox = QHBoxLayout()
        self.random_variable_frame = QFrame(self.calcWidget)
        self.random_variable_frame.setMinimumWidth(300)
        self.random_variable_frame.setFrameShape(QFrame.StyledPanel)
        self.rv_frame_layout = QVBoxLayout(self.random_variable_frame)

        # Discrete Random Variables
        # Define the buttons
        self.u = QPushButton('Uniform Discrete Random Variables', self.calcWidget)
        self.b = QPushButton('Binomial Distribution Random Variables', self.calcWidget)
        self.p = QPushButton('Poisson Random Variables', self.calcWidget)
        self.g = QPushButton('Geometric Random Variables', self.calcWidget)
        self.n = QPushButton('Negative Binomial Random Variables', self.calcWidget)
        self.h = QPushButton('Hyper-geometric Variables', self.calcWidget)

        # Configure the buttons
        self.u.clicked.connect(lambda: self.openDialog(self.u.text()))
        self.b.clicked.connect(lambda: self.openDialog(self.b.text()))
        self.p.clicked.connect(lambda: self.openDialog(self.p.text()))
        self.g.clicked.connect(lambda: self.openDialog(self.g.text()))
        self.n.clicked.connect(lambda: self.openDialog(self.n.text()))
        self.h.clicked.connect(lambda: self.openDialog(self.h.text()))

        # Set up the UI for btns
        self.btnHBox.addStretch(1)
        self.buttons = [self.u, self.b, self.p, self.g, self.n, self.h]
        for btn in self.buttons:
            self.rv_frame_layout.addWidget(btn)
        self.btnHBox.addWidget(self.random_variable_frame)
        self.mainVBox.addLayout(self.btnHBox)

        # Finally, show them off plz
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def enableButtons(self, switch=True):
        for btn in self.buttons:
            btn.setEnabled(switch)

    # Defining Main Functions
    def getBackHome(self):
        self.clearLayout(self.shLayout)
        self.enableButtons()
        self.sh.setAlignment(Qt.AlignCenter)
        self.sh.setText(homeMSG)

    def openDialog(self, rvType):
        rv_dialog = DialogWindow(rvType)
        rv_dialog.resize(rv_dialog.width(), self.height())
        rv_dialog.move(self.x()+self.width()+10, self.y())
        rv_dialog.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Death Confirmation', "Are you sure to quit?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':

    app = QApplication(sys.argv)

    #test = NumberInput()
    #value = test.exec_()
    #if value:
    #    print(value)

    calc = MainWindow()

    sys.exit(app.exec_())