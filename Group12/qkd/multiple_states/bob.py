from random import randint
import sys
sys.path.append('../..')

from SimulaQron.cqc.pythonLib.cqc import CQCConnection

from qkd.bb84 import BB84_decode
from qkd.utils import parse_n


def main(n):
    with CQCConnection('Bob') as bob:

        theta_tilde = [randint(0, 1) for i in range(n)]

        qubits = []

        for i in range(n):
            qubits.append(bob.recvQubit())

        x_tilde = [BB84_decode(qubits[i], theta_tilde[i]) for i in range(n)]

        print("BOB\t key:", x_tilde)


if __name__ == '__main__':
    n = parse_n()
    main(n)