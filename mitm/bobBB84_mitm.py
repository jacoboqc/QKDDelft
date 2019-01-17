import random
import sys
sys.path.append('..')

from SimulaQron.cqc.pythonLib.cqc import CQCConnection
from shared import *


def error_rate(cqc, x_remain):
    test_string = []
    test_rounds = list(cqc.recvClassical())

    for i in test_rounds:
        test_string.append((x_remain.pop(i)))

    print("Bob test rounds: ", test_rounds)
    print("Bob test string: ", test_string)

    cqc.sendClassical("Alice", test_string)
    alice_test_string = list(cqc.recvClassical())
    print("Bob: Alice test string: ", alice_test_string)

    num_test = len(test_string)
    error = 0
    for bob_bit, alice_bit in zip(test_string, alice_test_string):
        if alice_bit != bob_bit:
            error += 1

    return error / num_test


def main():
    n = 10

    with CQCConnection("Bob") as Bob:
        theta_tilde = [ random.randint(0, 1) for _ in range(n) ]
        x_tilde = []


        for i in range(0, n):
            q = Bob.recvQubit()
            if theta_tilde[i] == 1:
                q.H()
            x_tilde.append(q.measure())
            print("Bob has received the state {}, measured in base {}".format(x_tilde[i], theta_tilde[i]))

        theta = Bob.recvClassical()
        Bob.sendClassical("Eve", theta_tilde)

        # filter strings for those rounds with equal basis
        theta_common = find_common_bases(theta, theta_tilde)
        x_remain = [ x_tilde[i] for i in theta_common ]

        # receive seed for extractor
        r = list(Bob.recvClassical())

        # seeded extractor
        k = simple_extractor(x_remain, r)

        print("> (Bob) The key is: {}".format(k))

        # error rate (Alice and Bob compute error rates without Eve interfering)
        error = error_rate(Bob, x_remain)
        print("Bob computed error rate: ", error)


if __name__ == '__main__':
    main()
