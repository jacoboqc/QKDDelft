from random import randint
import sys
sys.path.append('../..')

from SimulaQron.cqc.pythonLib.cqc import CQCConnection

from qkd.bb84 import BB84_decode, find_common_bases
from qkd.utils import parse_n, deserialize, simple_extractor
from qkd.messages import MSG_RECV_AND_MEAS


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

def main(n):
    with CQCConnection('Bob') as bob:

        theta_tilde = [randint(0, 1) for i in range(n)]

        qubits = []

        for i in range(n):
            qubits.append(bob.recvQubit())

        x_tilde = [BB84_decode(qubits[i], theta_tilde[i]) for i in range(n)]

        #bob.sendClassical('Eve', MSG_RECV_AND_MEAS)

        theta = deserialize(bob.recvClassical(), to_list=True)
        assert len(theta) == n, "Expected bases list of length {}".format(n)

        bob.sendClassical('Eve', theta_tilde)

        # filter strings for those rounds with equal basis
        theta_common = find_common_bases(theta, theta_tilde)

        x_remain = [x_tilde[i] for i in theta_common]
        x_remain_count = len(x_remain)

        # receive seed for extractor
        seed = deserialize(bob.recvClassical(), to_list=True)
        assert len(seed) == x_remain_count, "Expected seed of length {}".format(x_remain_count)

        # seeded extractor
        key = simple_extractor(x_remain, seed)

        print("> (Bob) The key is: {}".format(key))

        # error rate (Alice and Bob compute error rates without Eve interfering)
        error = error_rate(bob, x_remain)
        print("Bob computed error rate: ", error)


if __name__ == '__main__':
    n = parse_n()
    main(n)