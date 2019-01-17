from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit
import random
import time


def error_rate(cqc, x_remain):
    test_string = []
    test_rounds = []
    num_test = len(x_remain)/2

    while len(test_rounds) < num_test and len(x_remain) > 0:
        r = random.randint(0, len(x_remain) - 1)
        test_string.append(x_remain.pop(r))
        test_rounds.append(r)

    print("Alice chooses test rounds: ", test_rounds)
    print("Alice test string: ", test_string)

    cqc.sendClassical("Bob", test_rounds)
    bob_test_string = list(cqc.recvClassical())
    cqc.sendClassical("Bob", test_string)
    print("Alice: Bob test string: ", bob_test_string)

    error = 0
    for alice_bit, bob_bit in zip(test_string, bob_test_string):
        if alice_bit != bob_bit:
            error += 1

    return error / num_test


def main():
    n = 10

    with CQCConnection("Alice") as Alice:
        x = [random.randint(0, 1) for _ in range(n)]
        theta = [random.randint(0, 1) for _ in range(n)]
        for i in range(0, n):
            q = qubit(Alice)
            if theta[i]==1:
                q.H()
            if x[i]==1:
                q.X()
            Alice.sendQubit(q, "Eve")
            print("Alice has sent state {} in base {} to Bob".format(x[i], theta[i]))

        Alice.sendClassical("Eve", theta)
        theta_tilde = Alice.recvClassical()

        # filter strings for those rounds whith equal basis
        x_remain = []
        for i in range(n):
            if theta[i] == theta_tilde[i]:
                x_remain.append(theta[i])

        # generate seed for extractor
        r = [random.randint(0, 1) for _ in range(len(x_remain))]
        Alice.sendClassical("Eve", r)

        # seeded extractor
        k = 0
        for i in range(len(x_remain)):
            k = (k + x_remain[i] + r[i]) % 2

        print("> (Alice) The key is: {}".format(k))

        # error rate (Alice and Bob compute error rates without Eve interfering)
        time.sleep(5)
        error = error_rate(Alice, x_remain)
        print("Alice computed error rate: ", error)


if __name__ == '__main__':
    main()
