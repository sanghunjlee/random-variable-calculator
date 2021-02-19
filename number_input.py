import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#GLOBAL VARIABLES
PM = '+ / -'
WIN_HEIGHT = 240
WIN_WIDTH = 450
DISPLAY_LIMIT = 24 # this implies: ~16.8 width per one number


class NumberInput(QDialog, object):

    def __init__(self, flag='float'):

        super().__init__()
        self.initiating = True
        self.hasPeriod = False
        self.wordLimit = 0
        self.valueFormat = flag
        self.returnVal = None
        self.initUI()

    def initUI(self):
        self.setFixedSize(WIN_WIDTH, WIN_HEIGHT)
        self.grid_layout = QGridLayout(self)


        self.display = QLabel(self)
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.display.setStyleSheet("background:dark gray; color:white; font: bold 'MS Sans Serif'; font-size: 24px;"
                                   "padding:4px 4px 4px 4px;")
        self.display.setText("input numbers")

        self.scrollArea = QScrollArea(self)
        self.scrollBar = self.scrollArea.verticalScrollBar()
        self.scrollArea.setMinimumHeight(64)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.display)

        self.grid_layout.addWidget(self.scrollArea, 0, 0, 1, 4)

        # creating shortcuts
        self.shortcuts = {i: QShortcut(QKeySequence(str(i)), self) for i in range(1, 10)}
        self.shortcuts[10] = QShortcut(QKeySequence(Qt.Key_Minus), self)
        self.shortcuts[11] = QShortcut(QKeySequence(Qt.Key_0), self)
        self.shortcuts[12] = QShortcut(QKeySequence(Qt.Key_Period), self)
        self.shortcuts['enter'] = QShortcut(QKeySequence(Qt.Key_Return), self)
        self.shortcuts['esc'] = QShortcut(QKeySequence(Qt.Key_Escape), self)
        self.shortcuts['del'] = QShortcut(QKeySequence(Qt.Key_Backspace), self)

        # creating buttons
        self.number_btns = {i: QPushButton(str(i), self) for i in range(1, 10)}
        self.number_btns[10] = QPushButton(PM, self)
        self.number_btns[11] = QPushButton('0', self)
        self.number_btns[12] = QPushButton('.', self)

        self.del_btn = QPushButton('DEL', self)
        self.clr_btn = QPushButton('CLR', self)
        self.ok_btn = QPushButton('OK', self)

        # setting the button focus policy
        for i in range(1, 13):
            self.number_btns[i].setFocusPolicy(Qt.NoFocus)
        self.del_btn.setFocusPolicy(Qt.NoFocus)
        self.clr_btn.setFocusPolicy(Qt.NoFocus)
        self.ok_btn.setFocusPolicy(Qt.NoFocus)

        for i in [10, 12]:
            self.number_btns[i].setStyleSheet('background-color:rgb(191, 191, 191);')

        for i in range(12):
            self.grid_layout.addWidget(self.number_btns[i+1], 1 + i//3, i%3)
        self.grid_layout.addWidget(self.del_btn, 2, 3)
        self.grid_layout.addWidget(self.clr_btn, 3, 3)
        self.grid_layout.addWidget(self.ok_btn, 4, 3)

        # connecting shortcuts
        for i in range(1, 13):
            self.shortcuts[i].activated.connect(lambda x=i: self.numberPushed(x))
        self.shortcuts['enter'].activated.connect(self.confirm)
        self.shortcuts['esc'].activated.connect(self.clear)
        self.shortcuts['del'].activated.connect(self.delete)

        # connecting buttons
        self.number_btns[1].clicked.connect(lambda: self.numberPushed(1))
        self.number_btns[2].clicked.connect(lambda: self.numberPushed(2))
        self.number_btns[3].clicked.connect(lambda: self.numberPushed(3))
        self.number_btns[4].clicked.connect(lambda: self.numberPushed(4))
        self.number_btns[5].clicked.connect(lambda: self.numberPushed(5))
        self.number_btns[6].clicked.connect(lambda: self.numberPushed(6))
        self.number_btns[7].clicked.connect(lambda: self.numberPushed(7))
        self.number_btns[8].clicked.connect(lambda: self.numberPushed(8))
        self.number_btns[9].clicked.connect(lambda: self.numberPushed(9))
        self.number_btns[10].clicked.connect(lambda: self.numberPushed(10))
        self.number_btns[11].clicked.connect(lambda: self.numberPushed(11))
        self.number_btns[12].clicked.connect(lambda: self.numberPushed(12))

        self.del_btn.clicked.connect(self.delete)
        self.clr_btn.clicked.connect(self.clear)
        self.ok_btn.clicked.connect(self.confirm)

        if self.valueFormat == 'int':
            self.number_btns[12].setEnabled(False)

        self.show()
        print(f"height = {self.height()} and width = {self.width()}")

    def numberPushed(self, i):
        #print(f"number <<{i}>> pressed")

        if self.initiating:
            self.display.setText("")
            self.initiating = False

        # PLUS/MINUS
        if i == 10:
            if '-' in self.display.text():
                self.display.setText(self.display.text().lstrip('-'))
            else:
                self.display.setText('-' + self.display.text())

        # PERIOD
        elif i == 12:
            if self.hasPeriod:
                if self.display.text().endswith('.'):
                    if self.display.text().endswith('0.'):
                        self.wordLimit -= 1
                    self.display.setText(self.display.text().rstrip('.'))
                    self.hasPeriod = False
            else:
                if self.display.text().lstrip('-') == "":
                    self.display.setText(self.display.text()+'0.')
                    self.wordLimit += 1
                else:
                    self.display.setText(self.display.text() + '.')
                self.hasPeriod = True

        # regular numbers input
        else:
            self.scrollBar.setValue(self.scrollBar.maximum())
            if self.wordLimit % (DISPLAY_LIMIT + 1) == DISPLAY_LIMIT:
                self.display.setText(self.display.text() + '\n')
            if self.display.text().lstrip('-') == '0':
                self.display.setText(self.display.text().rstrip('0'))
                self.wordLimit -= 1
            self.display.setText(self.display.text() + str(i%11))
            self.wordLimit += 1

    def delete(self):
        #print("deleting")
        if self.display.text().endswith('.'):
            self.hasPeriod = False
        else:
            if self.wordLimit > 0:
                self.wordLimit -= 1
        self.display.setText(self.display.text()[:-1])
        if self.display.text().endswith('\n'):
            self.display.setText(self.display.text()[:-1])

    def clear(self):
        #print("clearing")
        self.display.setText("")
        self.wordLimit = 0

    def confirm(self):
        #print("confirming")
        if self.initiating is True:
            self.display.setText("ERROR: input a number")
            return
        if self.valueFormat is 'float':
            self.returnVal = float(self.display.text())
            print(f"returning: {self.returnVal}")
            self.accept()

    def exec(self):
        super(NumberInput, self).exec()
        return self.returnVal


if __name__ == "__main__":
    app = QApplication(sys.argv)
    test = NumberInput()
    sys.exit(app.exec())
