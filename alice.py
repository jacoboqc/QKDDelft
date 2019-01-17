from random import randint

from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit
from shared import *


def encode(conn, bit, basis):
    qb = qubit(conn)

    if bit == 1:
        qb.X()

    if basis == 1:
        qb.H()

    return qb


def main(n):
    with CQCConnection('Alice') as alice:

        bits = [ randint(0, 1) for i in range(n) ]
        # print("Alice bits:", bits)

        bases = [ randint(0, 1) for i in range(n) ]
        # print("Alice bases:", bases)

        qubits = [ encode(alice, bits[i], bases[i]) for i in range(n) ]

        for qb in qubits:
            alice.sendQubit(qb, 'Bob')

        msg = deserialize(alice.recvClassical())
        assert msg == MSG_RECV_AND_MEAS, "Unexpected message from Bob"

        alice.sendClassical('Bob', bases)

        bob_bases = deserialize(alice.recvClassical(), to_list=True)
        assert len(bob_bases) == n, "Expected bases list of length {}".format(n)

        common_bases = find_common_bases(n, bases, bob_bases)
        # print("common bases:", common_bases)

        filtered = filter_bits(bits, common_bases)
        filt_count = len(filtered)
        print("Alice filtered:", filtered)

        padded = pad_len_7(filtered)
        print("Alice padded:", padded)
        syndrome = hamming(padded)
        print('syndrome:', syndrome)

        alice.sendClassical('Bob', syndrome)

        seed = [ randint(0, 1) for i in range(filt_count) ]
        print('seed:', seed)

        key = simple_extractor(filt_count, filtered, seed)
        print("Alice key:", key)

        alice.sendClassical('Bob', seed)


if __name__ == '__main__':
    n = parse_num_bits()
    main(n)