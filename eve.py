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
    with CQCConnection('Eve') as eve:

        bits = [ randint(0, 1) for i in range(n) ]
        print("Eve bits:    ", bits)

        bases = [ randint(0, 1) for i in range(n) ]
        print("Eve bases:   ", bases)

        qubits = [ encode(eve, bits[i], bases[i]) for i in range(n) ]

        for qb in qubits:
            eve.sendQubit(qb, 'Bob')


if __name__ == '__main__':
    n = parse_num_bits()
    main(n)