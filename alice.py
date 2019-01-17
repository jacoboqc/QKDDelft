from random import randint

from SimulaQron.cqc.pythonLib.cqc import CQCConnection
from shared import *


def main(n):
    with CQCConnection('Alice') as alice:

        x = [ randint(0, 1) for i in range(n) ]
        print("Alice bits:  ", x)

        theta = [ randint(0, 1) for i in range(n) ]
        print("Alice bases: ", theta)

        qubits = [ encode(alice, x[i], theta[i]) for i in range(n) ]

        for qb in qubits:
            alice.sendQubit(qb, 'Bob')

        msg = deserialize(alice.recvClassical())
        assert msg == MSG_RECV_AND_MEAS, "Unexpected message from Bob"

        alice.sendClassical('Bob', theta)

        theta_tilde = deserialize(alice.recvClassical(), to_list=True)
        assert len(theta_tilde) == n, "Expected bases list of length {}".format(n)

        theta_common = find_common_bases(theta, theta_tilde)
        # print("common bases:", theta_common)

        x_common = filter_bits(x, theta_common)
        x_common_count = len(x_common)
        print("Alice x_common_count:", x_common_count)

        padded = pad_len_7(x_common)
        print("Alice padded:", padded)
        syndrome = hamming(padded)
        print('syndrome:', syndrome)

        alice.sendClassical('Bob', syndrome)

        seed = [ randint(0, 1) for i in range(x_common_count) ]
        print('seed:', seed)

        key = simple_extractor(x_common, seed)
        print("Alice key:", key)

        alice.sendClassical('Bob', seed)


if __name__ == '__main__':
    n = parse_num_bits()
    main(n)