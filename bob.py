from random import randint
from SimulaQron.cqc.pythonLib.cqc import CQCConnection
from shared import *


def decode(conn, qb, basis):
    if basis == 1:
        qb.H()

    return qb.measure()


def main(n):
    with CQCConnection('Bob') as bob:

        bases = [ randint(0, 1) for i in range(n) ]
        print("Bob bases:   ", bases)

        qubits = []

        for i in range(n):
            qubits.append(bob.recvQubit())

        bits = [ decode(bob, qubits[i], bases[i]) for i in range(n) ]
        print("Bob bits:    ", bits)

        bob.sendClassical('Alice', MSG_RECV_AND_MEAS)

        alice_bases = deserialize(bob.recvClassical(), to_list=True)
        assert len(alice_bases) == n, "Expected bases list of length {}".format(n)

        bob.sendClassical('Alice', bases)

        common_bases = find_common_bases(n, bases, alice_bases)

        filtered = filter_bits(bits, common_bases)
        filt_count = len(filtered)

        seed = deserialize(bob.recvClassical(), to_list=True)
        assert len(seed) == filt_count, "Expected seed of length {}".format(filt_count)

        key = simple_extractor(filt_count, filtered, seed)
        print("Bob key:", key)


if __name__ == '__main__':
    n = parse_num_bits()
    main(n)