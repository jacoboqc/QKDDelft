from random import randint
import sys
sys.path.append('../..')

from SimulaQron.cqc.pythonLib.cqc import CQCConnection
from qkd.bb84 import BB84_encode


def main():
    with CQCConnection('Alice') as alice:

        x = randint(0, 1)
        theta = randint(0, 1)

        qb = BB84_encode(alice, x, theta)

        alice.sendQubit(qb, 'Eve')

        print("ALICE\t key:", x)


if __name__ == '__main__':
    main()