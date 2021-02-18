import math
import time


class RandomVariable():
    def __init__(self):
        self.desc_u = "Uniform Discrete Random Variable\n"\
                      "\tThe probability mass function:\t$p(x_i)=\\frac{1}{n}$, for $i=1,2,\\cdots, n$\n"\
                      "\tThe expected value:\t$E(X)=\\frac{\sum(X)}{n}$\n"\
                      "\tThe variance: $Var(X)=\\frac{\sum(X^2)}{n} - {\\frac{sum(X)}{n}}^2$"

    def UniformDiscreteRV(self, x):
        print(
            "Uniform Discrete Random Variable\n"
            "\tThe probability mass function:\tp(x_i)=1/n, for i=1,2,..., n\n"
            "\tThe expected value:\tE(X)=sum(X)/n\n"
            "\tThe variance: Var(X)=sum(X^2)/n - (sum(X)/n)^2\n\n"
            "Given X = {" + str(x).lstrip('[').rstrip(']') + "}"
        )

        p = 1/len(x)
        E = sum(x)/len(x)
        xx = list()
        for i in x:
            xx.append(i*i)
        V = sum(xx)/len(x) - E*E
        print("The probability mass function (pmf):")
        print("\t x \t | \t \t pmf \t \t ")
        print("--------------------------")
        for i in x:
            print("\t"+ str(i) + "\t | \t \t " + str(p))
        print(
            "E(X) = " + str(E) + "\n"
            "Var(X) = " + str(V) + "\n"
        )


    def BinomialDistributionRV(self, n, p):
        if p > 1:
            return print("ERROR: p is greater than 1")
        elif p < 0:
            return print("ERROR: p is less than 0")
        else:
            print(
                "Binomial Distribution Random Variable\n"
                "Given: n:='# of trials', r:='# of successes', p:='probability of success'\n"
                "\tThe Binomial mass function: p(r) = nCr p^r (1-p)^(n-r)\n"
                "\tThe expected value: E(X) = np\n"
                "\tThe variance: Var(X) = np(1-p)\n\n"
                "Given n=" + str(n) + " and p=" + str(p) + ":"
            )
            q = 1.0 - p
            E = n * p
            V = n * p * q
            print("The probability mass function (pmf):")
            print("\t r \t | \t \t pmf \t \t ")
            print("--------------------------")
            check_prob = 0
            for r in range(n+1):
                Pr = nCr(n, r) * math.pow(p, r) * math.pow(q, n-r)
                check_prob+=Pr
                print("\t" + str(r) + "\t |   %1.8f" %Pr)
            print(
                "E(X) = " + str(E) + "\n"
                "Var(X) = " + str(V) + "\n"
            )
            print("CHECK: Σp(r) = %1.1f" % check_prob)


    def PoissonRV(self, k, h, w=1):
        if w <= 0:
            return print("ERROR: w has to be greater than 0!")
        description = "Poisson Random Variable\n"\
                      "\tThe probability mass function: p(k)=e^{-λw} (λw)^k/(k!), w>0, k=0,1,2,...\n"\
                      "\tThe expected value: E(X) = λw\n"\
                      "\tThe variance: Var(X) = λw\n\n"\
                      "Given:\tw := 'a period of time or space',\n"\
                      "\t\tλ := 'the average # of successes per unit time or space',\n"\
                      "\t\tk := '# of success'"
        print(description)
        hw = h*w
        Pk = math.exp(-hw) * (math.pow(hw, k) / math.factorial(k))
        E = hw
        V = hw

        print(
            "\np(x = %1.1f) =  %f\n"
            "E(X) = %1.1f\n"
            "Var(X) = %1.1f\n"
            % (k, Pk, E, V)
        )


    def GeometricRV(self, n, p):
        introduction = "Geometric Random Variable\n" \
                       "\tThe probability mass function: p(x)=p(1-p)^{n-1}\n" \
                       "\tThe expected value: E(X)=1/p\n" \
                       "\tThe variance: Var(X)=(1-p)/(p^2)\n\n" \
                       "Given:\tn := '# of trials needed to achieve the first success'\n" \
                       "\t\tp := 'probability of success'"
        print(introduction)
        q = 1 - p
        Pn = p * math.pow(q, n-1)
        E = 1.0/p
        V = (1.0 - p) / (p**2)
        result = "p(n=%1.1f) = %f\n" \
                 "E(X) = %1.1f\n" \
                 "Var(X) = %1.1f" \
                 % (n, Pn, E, V)
        print(result)


def nCr(n,r):
    r = max(r, n-r)
    denom = math.factorial(n-r)
    n_nr = range(n, r, -1)
    n = 1
    for i in n_nr:
        n = n*i
    return n//denom

if __name__ == "__main__":
    start_time = time.time()
    rv = RandomVariable()
    rv.GeometricRV(10, 0.5)
    print("%s seconds" %(time.time()-start_time))