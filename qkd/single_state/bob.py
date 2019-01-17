from random import randint
import sys
sys.path.append('../..')

from SimulaQron.cqc.pythonLib.cqc import CQCConnection
from qkd.bb84 import BB84_decode


def main():
    with CQCConnection('Bob') as bob:

        theta_tilde = randint(0, 1)

        qb = bob.recvQubit()

        x_tilde = BB84_decode(qb, theta_tilde)

        print("BOB\t key:", x_tilde)


if __name__ == '__main__':
    main()