import sys
import math

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from NumberInput import NumberInput

class NormalCDF(QDialog, object):

    def __init__(self):
        super().__init__()

        self.height = 300
        self.width = 500

        self.parameters = {'x':None, 'mean':None, 'stndev':None, 'var':None}

        self.initUI()

    def initUI(self):
        self.resize(self.width, self.height)
        self.move(600, 300)

        self.grid = QGridLayout(self)

        self.display = QLabel()
        self.display.setStyleSheet("background-color: gray; color:white;")
        self.display.setAlignment(Qt.AlignCenter)
        self.x_btn = QPushButton("X")
        self.mean_btn = QPushButton("Mean")
        self.var_btn = QPushButton("Variance")
        self.stndev_btn = QPushButton("Standard Deviation")
        self.calc_btn = QPushButton("Calculate")
        self.cancel_btn = QPushButton("Cancel")

        self.btns = {'x':self.x_btn, 'mean':self.mean_btn, 'stndev':self.stndev_btn, 'var':self.var_btn}
        for p, b in self.btns.items():
            b.clicked.connect(lambda state, x=p : self.param_input(x))
        self.calc_btn.clicked.connect(self.calculation)
        self.cancel_btn.clicked.connect(self.close)

        self.grid.addWidget(self.display, 0,0,2,3)
        self.grid.addWidget(self.x_btn, 2, 0, 1, 2)
        self.grid.addWidget(self.mean_btn, 3, 0, 1, 2)
        self.grid.addWidget(self.var_btn, 4, 0, 1, 2)
        self.grid.addWidget(self.stndev_btn, 5, 0, 1, 2)
        self.grid.addWidget(self.calc_btn, 4, 2, 1, 1)
        self.grid.addWidget(self.cancel_btn, 5, 2, 1, 1)

        self.show()

    def param_input(self, param):
        scanner = NumberInput()
        value = scanner.exec_()
        if value:
            self.parameters[param] = value
            self.btns[param].setText(f"{param} = {value:.3f}")
            if param == 'var':
                self.parameters['stndev'] = math.sqrt(value)
                self.btns['stndev'].setText(f"Standard Deviation = {math.sqrt(value):.3f}")
            elif param == 'stndev':
                self.parameters['var'] = math.pow(value, 2)
                self.btns['var'].setText(f"Variance = {math.pow(value, 2):.3f}")

    def calculation(self):
        if None not in self.parameters.values():
            x, m, s, v = self.parameters.values()
            z = ( x - m ) / s
            if z < 0:
                result = 1 - self.cdf(-z)
            elif z == 0:
                result = 0.5
            else:
                result = self.cdf(z)

            self.display.setText(f'cdf({z:.3f}) = {result:.3f}')


    def cdf(self, z):
        n = 1000000
        dz = z / n
        pre = 2 * math.pi
        pre = math.sqrt(pre)
        pre = 1 / pre
        sum = 0
        for i in range(1, n+1):
            a = math.pow(i * dz, 2.0)
            b = math.pow((i+1)*dz, 2.0)
            e_i = math.exp(- (a / 2)) + math.exp(- (b / 2))
            e_i = e_i / 2
            #print(str(i*dz) + ": " + str(e_i) + " >> " + str(dz*e_i))
            sum += dz * e_i
        return 0.5 + pre * sum


if __name__ == "__main__":
    app = QApplication(sys.argv)

    n = NormalCDF()

    sys.exit(app.exec_())

