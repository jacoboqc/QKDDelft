from random import randint
import sys
sys.path.append('../..')

from SimulaQron.cqc.pythonLib.cqc import CQCConnection

from qkd.bb84 import BB84_encode, find_common_bases
from qkd.utils import parse_n, deserialize, simple_extractor
from qkd.messages import MSG_RECV_AND_MEAS


def main(n):
    with CQCConnection('Alice') as alice:

        x = [randint(0, 1) for i in range(n)]
        theta = [randint(0, 1) for i in range(n)]

        qubits = [BB84_encode(alice, x[i], theta[i]) for i in range(n)]

        for qb in qubits:
            alice.sendQubit(qb, 'Eve')

        msg = deserialize(alice.recvClassical())
        assert msg == MSG_RECV_AND_MEAS, "Unexpected message from Bob"

        alice.sendClassical('Bob', theta)

        theta_tilde = deserialize(alice.recvClassical(), to_list=True)
        assert len(theta_tilde) == n, "Expected bases list of length {}".format(n)

        theta_common = find_common_bases(theta, theta_tilde)

        x_remain = [x[i] for i in theta_common]
        x_remain_count = len(x_remain)
        # print("Alice x_remain_count:", x_remain_count)

        seed = [randint(0, 1) for i in range(x_remain_count)]
        # print('seed:', seed)

        key = simple_extractor(x_remain, seed)

        alice.sendClassical('Bob', seed)

        print("ALICE\t key:", key)


if __name__ == '__main__':
    n = parse_n()
    main(n)