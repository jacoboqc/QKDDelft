from random import randint
import sys
sys.path.append('../..')

from SimulaQron.cqc.pythonLib.cqc import CQCConnection

from qkd.bb84 import BB84_encode, find_common_bases, sample_subset, get_remaining, count_errors
from qkd.utils import parse_n, deserialize, simple_extractor
from qkd.messages import MSG_RECV_AND_MEAS
from qkd.reconciliation import hamming_syndrome


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

        x_common = [x[i] for i in theta_common]

        x_test, test_indices = sample_subset(x_common)

        alice.sendClassical('Bob', test_indices)
        x_test_tilde = deserialize(alice.recvClassical(), to_list=True)
        alice.sendClassical('Bob', x_test)

        error_count = count_errors(x_test, x_test_tilde)
        if error_count > 1:
            print('(Alice): More than 1 error in tested bits. Abort.')
            exit()

        print('Error count in tested bits is {}. Continuing'.format(error_count))

        x_remain = get_remaining(x_common, test_indices)

        if len(x_remain) > 11:
            x_remain = x_remain[:11]

        print('(Alice) x_remain = {}'.format(x_remain))

        syndrome = hamming_syndrome(x_remain)
        # print('alice syndrome:', syndrome)
        alice.sendClassical('Bob', syndrome)

        seed = [randint(0, 1) for i in range(len(x_remain))]
        # print('seed:', seed)

        key = simple_extractor(x_remain, seed)

        alice.sendClassical('Bob', seed)

        print("ALICE\t key:", key)


if __name__ == '__main__':
    n = parse_n()
    main(n)