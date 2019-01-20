from random import randint
import time
import sys
sys.path.append('../..')

from SimulaQron.cqc.pythonLib.cqc import CQCConnection

from qkd.bb84 import BB84_encode, find_common_bases
from qkd.utils import parse_n, deserialize, simple_extractor
from qkd.messages import MSG_RECV_AND_MEAS


def error_rate(cqc, x_remain):
    test_string = []
    test_rounds = []
    num_test = len(x_remain)/2

    while len(test_rounds) < num_test and len(x_remain) > 0:
        r = randint(0, len(x_remain) - 1)
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

def main(n):
    with CQCConnection('Alice') as alice:

        x = [randint(0, 1) for i in range(n)]
        theta = [randint(0, 1) for i in range(n)]

        qubits = [BB84_encode(alice, x[i], theta[i]) for i in range(n)]

        for qb in qubits:
            alice.sendQubit(qb, 'Eve')

        msg = deserialize(alice.recvClassical())
        assert msg == MSG_RECV_AND_MEAS, "Unexpected message from Bob"

        alice.sendClassical('Eve', theta)

        theta_tilde = deserialize(alice.recvClassical(), to_list=True)
        assert len(theta_tilde) == n, "Expected bases list of length {}".format(n)

        # filter strings for those rounds with equal basis
        theta_common = find_common_bases(theta, theta_tilde)

        x_remain = [x[i] for i in theta_common]
        x_remain_count = len(x_remain)

        # generate seed for extractor
        seed = [randint(0, 1) for i in range(x_remain_count)]

        # seeded extractor
        key = simple_extractor(x_remain, seed)

        alice.sendClassical('Eve', seed)

        print("> (Alice) The key is: {}".format(key))

        # error rate (Alice and Bob compute error rates without Eve interfering)
        time.sleep(5)
        error = error_rate(alice, x_remain)
        print("Alice computed error rate: ", error)


if __name__ == '__main__':
    n = parse_n()
    main(n)