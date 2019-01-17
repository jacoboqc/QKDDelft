from SimulaQron.cqc.pythonLib.cqc import CQCConnection
import random


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
        theta = [random.randint(0, 1) for _ in range(n)]
        for i in range(0, n):
            q = Bob.recvQubit()
            if theta[i] == 1:
                q.H()
            m = q.measure()
            print("Bob has received the state {}, measured in base {}".format(m, theta[i]))

        theta_tilde = Bob.recvClassical()
        Bob.sendClassical("Eve", theta)

        # filter strings for those rounds whith equal basis
        s = []
        for i in range(n):
            if theta[i] == theta_tilde[i]:
                s.append(theta[i])

        # receive seed for extractor
        r = list(Bob.recvClassical())

        # seeded extractor
        k = 0
        for i in range(len(s)):
            k = (k + s[i] + r[i]) % 2

        print("> (Bob) The key is: {}".format(k))

        # error rate (Alice and Bob compute error rates without Eve interfering)
        error = error_rate(Bob, s)
        print("Bob computed error rate: ", error)


if __name__ == '__main__':
    main()
