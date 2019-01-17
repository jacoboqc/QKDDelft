from random import randint
import sys
sys.path.append('../..')

from SimulaQron.cqc.pythonLib.cqc import CQCConnection

from qkd.bb84 import BB84_decode, find_common_bases
from qkd.utils import parse_n, deserialize, simple_extractor
from qkd.messages import MSG_RECV_AND_MEAS


def main(n):
    with CQCConnection('Bob') as bob:

        theta_tilde = [randint(0, 1) for i in range(n)]

        qubits = []

        for i in range(n):
            qubits.append(bob.recvQubit())

        x_tilde = [BB84_decode(qubits[i], theta_tilde[i]) for i in range(n)]

        bob.sendClassical('Alice', MSG_RECV_AND_MEAS)

        theta = deserialize(bob.recvClassical(), to_list=True)
        assert len(theta) == n, "Expected bases list of length {}".format(n)

        bob.sendClassical('Alice', theta_tilde)

        theta_common = find_common_bases(theta, theta_tilde)

        x_remain = [x_tilde[i] for i in theta_common]
        x_remain_count = len(x_remain)
        print("Bob x_remain_count:", x_remain_count)

        seed = deserialize(bob.recvClassical(), to_list=True)
        assert len(seed) == x_remain_count, "Expected seed of length {}".format(x_remain_count)

        key = simple_extractor(x_remain, seed)

        print("BOB\t key:", key)


if __name__ == '__main__':
    n = parse_n()
    main(n)