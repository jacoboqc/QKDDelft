from random import randint
import sys
sys.path.append('../..')

from SimulaQron.cqc.pythonLib.cqc import CQCConnection

from qkd.bb84 import BB84_decode, find_common_bases, get_remaining, count_errors
from qkd.utils import parse_n, deserialize, simple_extractor
from qkd.messages import MSG_RECV_AND_MEAS
from qkd.reconciliation import recon_decode


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
        # print('Alice theta_common:', theta_common)

        x_common = [x_tilde[i] for i in theta_common]

        test_indices = deserialize(bob.recvClassical(), to_list=True)
        x_test_tilde = [x_common[i] for i in test_indices]
        bob.sendClassical('Alice', x_test_tilde)
        x_test = deserialize(bob.recvClassical(), to_list=True)

        if count_errors(x_test, x_test_tilde) > 1:
            print('(Bob): More than 1 error in tested bits. Abort.')
            exit()

        x_remain_tilde = get_remaining(x_common, test_indices)

        if len(x_remain_tilde) > 11:
            x_remain_tilde = x_remain_tilde[:11]

        print('(Bob) x_remain_tilde = {}'.format(x_remain_tilde))

        syndrome_alice = deserialize(bob.recvClassical(), to_list=True)

        x_remain_est, err_est = recon_decode(syndrome_alice, x_remain_tilde)
        print('(Bob) error estimate:', err_est)
        print('(Bob) x_remain estimate:', x_remain_est)

        seed = deserialize(bob.recvClassical(), to_list=True)
        assert len(seed) == len(x_remain_est), "Expected seed of length {}".format(len(x_remain_est))

        key = simple_extractor(x_remain_est, seed)

        print("BOB\t key:", key)


if __name__ == '__main__':
    n = parse_n()
    main(n)