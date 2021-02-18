import time
import math

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from latex_text import mathTex_to_QPixmap
from NumberInput import NumberInput

# GLOBAL VARIABLES
LAMBDA = '\u03bb'
RV_DICT = {'uniform':['X(list)'],
           'binomial':['r(list)', 'n(int)', 'p'],
           'poisson':['k(list)', LAMBDA, 'w=1'],
           'geometric':['n', 'p'],
           'negative':['n', 'p', 'r'],
           'hyper':['N', 'n', 'r', 'k']}
INFO_DICT = {'uniform': ["The probability mass function: $p(x) = \\frac{1}{n}$",
                            "The expected value: $E(X) = \\frac{\sum x_i}{n}$",
                            "The variance: $Var(X) = \\frac{\sum x_i^2}{n} - \left(\\frac{\sum x_i}{n}\\right)^2$"],

                'binomial': ["The probability mass function: $p(r) = _{n}C_{r} p^r (1-p)^{n-r}$",
                             "The expected value: $E(X) = np$",
                             "The variance: $Var(X) = np(1-p)$"],

                'poisson': ["The probability mass function: $p(X(w)=k) = e^{-\lambda w}\\frac{(\lambda w)^k}{k!}$",
                            "The expected value: $E(X) = \lambda w$",
                            "The variance: $Var(X) = \lambda w$"],

                'geometric': ["The probability mass function: $p(n) = p(1-p)^{n-1}$",
                              "The expected value: $E(X) = \\frac{1}{p}$",
                              "The variance: $Var(X) = \\frac{1-p}{p^2}$"],

                'negative': ["The probability mass function: $p(n) = {}_{n-1}C_{r-1} p^r (1-p)^{n-r}$",
                             "The expected value: $E(X) = \\frac{r}{p}$",
                             "The variance: $Var(X) = \\frac{r(1-p)}{p^2}$"],

                'hyper': ["The probability mass function: $p(X=k) = \\frac{{}_nC_k {}_{N-n}C_{r-k}}{{}_NC_r}$",
                          "The expected value: $E(X) = \\frac{rn}{N}$",
                          "The variance: $Var(X) = \\frac{rn}{N}\cdot\\frac{N-r}{N}\cdot\\frac{N-n}{N-1}$"]}


# LOCAL FUNCTION
def nCr(n,r):
    n = int(n)
    r = int(r)
    print("finding max")
    r = max(r, n-r)
    print("getting the denom")
    denom = math.factorial(n-r)
    print("setting for the numer")
    n_nr = range(n, r, -1)
    n = 1
    print("getting the numer")
    for i in n_nr:
        n = n*i
    return float(n//denom)


def imgLabel(pix):
    img = QLabel()
    img.setPixmap(pix)
    return img


def displayMath(text, alignment=Qt.AlignCenter):
    qh = QHBoxLayout()
    if "$" not in text:
        qh.addWidget(QLabel(text), alignment=alignment)
    else:
        phrases = text.split("$")
        for i in range(len(phrases) - 1 if phrases[len(phrases) - 1] == "" else len(phrases)):
            if i % 2 == 0:
                qh.addWidget(QLabel(phrases[i]), alignment=Qt.AlignLeft)
            else:
                qh.addWidget(imgLabel(mathTex_to_QPixmap("$" + phrases[i] + "$", 10, 'w')), alignment=Qt.AlignLeft)
    return qh

def clearLayout(layout):
    for i in range(layout.count()):
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())


class DialogWindow(QDialog, object):
    def __init__(self, rvType):
        super().__init__()

        # Setting the variables
        self.rv = rvType.lower().split(' ')[0].split('-')[0]
        self.parameters = RV_DICT[self.rv]
        self.variableDict = dict()

        # initiate the UI
        self.initUI(rvType)


    def initUI(self, rvType):
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint |
                                   Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        self.setWindowTitle(rvType)
        self.resize(400,300)
        #self.dialog.setAttribute(Qt.WA_DeleteOnClose)

        print("setting the widgets and layout")
        # Setting the widgets & layouts
        outer_vBox = QVBoxLayout(self)
        bottom_Box = QWidget(self)
        inner_hBox = QHBoxLayout(bottom_Box)
        left_vBox = QVBoxLayout()
        right_vBox = QVBoxLayout()

        self.infoDisplay = QLabel(self)
        self.infoLayout = QVBoxLayout(self.infoDisplay)
        self.infoDisplay.setStyleSheet("color: white; background-color:gray; padding: 5px 5px 5px 5px;")

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setMinimumHeight(240)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.infoDisplay)

        outer_vBox.addWidget(self.scrollArea)
        outer_vBox.addWidget(bottom_Box)

        self.paramInfoDisplay = QLabel()
        #self.paramInfoDisplay.setStyleSheet("color: white; background-color:gray; padding: 5px 5px 5px 5px;")
        left_vBox.addWidget(self.paramInfoDisplay)

        print("displaying info")
        # Displaying info
        self.infoLayout.addWidget(QLabel("<u><b>%s<\\b><\\u>" % rvType), alignment=Qt.AlignCenter)
        self.infoLayout.addSpacerItem(QSpacerItem(1, 1))
        self.infoLayout.addWidget(QLabel("Given: X:='discrete random variable', n:='# of items in X'"),
                                  alignment=Qt.AlignCenter)
        print(rvType.split(' ')[0].lower())
        for stuff in INFO_DICT[self.rv]:
            print(stuff + " getting processed")
            self.infoLayout.addLayout(displayMath(stuff))
        self.infoLayout.addStretch(1)

        print("getting the parameters")
        self.paramInfoDisplay.setText("Input the parameters for the calculation:")
        print(self.parameters)
        '''
        for var in self.parameters:
            print(var)
            preassigned = False
            pretyped = False
            if "=" in var:
                preassigned = True
                var, value = var.split("=")
            elif "(" and ")" in var:
                pretyped = True
                var, varType = var.split('(')
                varType = varType.strip(')')
            p = QWidget()
            h = QHBoxLayout(p)
            varLabel = QLabel(var + " = ")
            if pretyped and varType == 'list':
                varLine = QLineEdit('item1, item2, item3, etc')
            else:
                varLine = QLineEdit(value if preassigned else "0")
                varLine.setValidator(QDoubleValidator(0,1,5))
            self.variableDict[var] = varLine
            h.addWidget(varLabel)
            h.addWidget(varLine)
            left_vBox.addWidget(p)
        '''
        self.buttonDict = {}
        for var in self.parameters:
            preassigned = False
            pretyped = False
            if "=" in var:
                preassigned = True
                var, value = var.split("=")
            elif "(" and ")" in var:
                pretyped = True
                var, varType = var.split('(')
                varType = varType.strip(')')
            if preassigned:
                varBtn = QPushButton(var + " = " + value)
                self.variableDict[var] = value
            else:
                varBtn = QPushButton(var)
            if pretyped:
                varBtn.clicked.connect(lambda state, x=var, f=varType : self.inputNumbers(x, f))
            else:
                varBtn.clicked.connect(lambda state, x=var: self.inputNumbers(x))
            self.buttonDict[var] = varBtn
            left_vBox.addWidget(varBtn)


        print("setting the buttons")
        # Configuring Calculate|Quit buttons
        calcBtn = QPushButton("Calculate", self)
        calcBtn.setStyleSheet('color: black; background-color: light gray;')
        calcBtn.clicked.connect(self.rvCalculation)

        quitBtn = QPushButton("Quit", self)
        quitBtn.setStyleSheet('color: black; background-color: light gray;')
        quitBtn.clicked.connect(self.close)

        right_vBox.addStretch(1)
        right_vBox.addWidget(calcBtn)
        right_vBox.addWidget(quitBtn)

        inner_hBox.addLayout(left_vBox)
        inner_hBox.addLayout(right_vBox)

    def inputNumbers(self, var, varType = 'float'):
        numbScanner = NumberInput().exec()
        if numbScanner:
            self.variableDict[var] = numbScanner
            print(self.variableDict)
            self.buttonDict[var].setText(var + " = " + str(numbScanner))


    def rvCalculation(self):
        # Recalibrating the rv parameter list to something workable
        print("recalibrating")
        rv_values = dict()
        '''
        for k, v in self.variableDict.items():
            if 'range' in v.text():
                abc = v.text().split('range')[1].lstrip('(').rstrip(')').split(',')
                if len(abc) == 1:
                    rv_values[k] = range(abc[0])
                elif len(abc) == 2:
                    rv_values[k] = range(abc[0], abc[1])
                elif len(abc) >= 3:
                    rv_values[k] = range(abc[0], abc[1], abc[2])
            elif ',' in v.text():
                l = v.text().split(',')
                for i in range(len(l)):
                    l[i] = float(l[i])
                rv_values[k] = sorted(l)
            else:
                rv_values[k] = float(v.text())
        '''

        rv_values = self.variableDict
        print(rv_values)

        if self.rv == 'uniform':
            X = rv_values['X']
            if type(X) is not list:
                X = [X]
            XX = [x*x for x in X]

            pmf = "The probability of any x in X = " + str(1/len(X))
            expectedValue = sum(X)/len(X)
            variance = sum(XX)/len(XX) - expectedValue**2
        elif self.rv == 'binomial':
            r = rv_values['r']
            if type(r) is not list:
                r = [r]
            n = int(rv_values['n'])
            p = rv_values['p']


            pmf = ["r \t | \t p(r)"]
            for i in r:
                p_i = nCr(n, i)
                p_i *= math.pow(p, i)*math.pow(1-p, n-i)
                pmf.append(str(int(i)) + " \t | \t %1.4f" % p_i)
            expectedValue = n*p
            variance = n*p*(1-p)
        elif self.rv == 'poisson':
            k = rv_values['k']
            if type(k) is not list:
                k = [k]
            hw = rv_values[LAMBDA] * rv_values['w']
            print(k, hw)
            pmf = ["k \t | \t p(k)"]
            for i in k:
                i = int(i)
                p_i = math.exp(-hw)
                p_i *= math.pow(hw, i)
                p_i /= math.factorial(i)
                print(p_i)
                pmf.append(str(i)+ " \t | \t %1.4f" % p_i)
            expectedValue = hw
            variance = hw
        elif self.rv == 'geometric':
            pass
        elif self.rv == 'negative':
            pass
        elif self.rv == 'hyper':
            N = rv_values['N']
            n = rv_values['n']
            r = rv_values['r']
            k = rv_values['k']

            pmf = nCr(n,k)
            pmf *= nCr(N-n, r-k)
            pmf /= nCr(N, r)
            expectedValue = r*n/N
            variance = (r*n*(N-r)*(N-n))/(N*N*(N-1))

        print("setting up the calc display")
        clearLayout(self.infoLayout)
        self.infoLayout.addLayout(displayMath("Expected Value = $%1.3f$" % expectedValue))
        self.infoLayout.addLayout(displayMath("Variance = $%1.3f$" % variance))
        self.infoLayout.addLayout(displayMath("Probability Values:", alignment=Qt.AlignLeft))
        if type(pmf) is list:
            self.infoDisplay.setMinimumHeight(30*len(pmf) + 120)
            for stuff in pmf:
                self.infoLayout.addLayout(displayMath(stuff))
        elif type(pmf) is str:
            self.infoLayout.addLayout(displayMath(pmf))
        self.infoLayout.addStretch(1)
