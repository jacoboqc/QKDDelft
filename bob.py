from random import randint
from SimulaQron.cqc.pythonLib.cqc import CQCConnection
from shared import *


def main(n):
    with CQCConnection('Bob') as bob:

        theta_tilde = [ randint(0, 1) for i in range(n) ]
        print("Bob bases:   ", theta_tilde)

        qubits = []

        for i in range(n):
            qubits.append(bob.recvQubit())
            r = randint(0, 5)
            if r == 0:
                qubits[i].X()

        x_tilde = [ decode(bob, qubits[i], theta_tilde[i]) for i in range(n) ]
        print("Bob bits:    ", x_tilde)

        bob.sendClassical('Alice', MSG_RECV_AND_MEAS)

        theta = deserialize(bob.recvClassical(), to_list=True)
        assert len(theta) == n, "Expected bases list of length {}".format(n)

        bob.sendClassical('Alice', theta_tilde)

        theta_common = find_common_bases(theta, theta_tilde)

        x_common = filter_bits(x_tilde, theta_common)
        x_common_count = len(x_common)
        print("Bob x_common_count:", x_common_count)

        alice_syndrome = deserialize(bob.recvClassical(), to_list=True)
        error_estimate_padded = recon_decode(alice_syndrome, pad_len_7(x_common))
        print("Bob estimate padded:", error_estimate_padded)
        filtered_estimate = unpad_len_7(error_estimate_padded, x_common_count)
        print("Bob estimate:", filtered_estimate)

        seed = deserialize(bob.recvClassical(), to_list=True)
        assert len(seed) == x_common_count, "Expected seed of length {}".format(x_common_count)

        key = simple_extractor(x_common, seed)
        print("Bob key:", key)


if __name__ == '__main__':
    n = parse_num_bits()
    main(n)