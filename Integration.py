import math

NUMBERS = [0,1,2,3,4,5,6,7,8,9]
OPERATORS = ['+', '-', '*', '/', '^', '\sqrt']

def distinguish(equation):
    equations = [equation]
    eq_l = []
    # check for operators
    for op in OPERATORS:
        for exp in equations:
            if op in exp:
                for stuff in exp.split(op):
                    eq_l.append(stuff)
                    eq_l.append(op)

    print(eq_l)



if __name__ == "__main__":
    eq = "x * e^(-x)"
    distinguish(eq)