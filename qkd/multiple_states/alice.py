from random import randint
import sys
sys.path.append('../..')

from SimulaQron.cqc.pythonLib.cqc import CQCConnection

from qkd.bb84 import BB84_encode
from qkd.utils import parse_n


def main(n):
    with CQCConnection('Alice') as alice:

        x = [randint(0, 1) for i in range(n)]
        theta = [randint(0, 1) for i in range(n)]

        qubits = [BB84_encode(alice, x[i], theta[i]) for i in range(n)]

        for qb in qubits:
            alice.sendQubit(qb, 'Eve')

        print("ALICE\t key:", x)


if __name__ == '__main__':
    n = parse_n()
    main(n)