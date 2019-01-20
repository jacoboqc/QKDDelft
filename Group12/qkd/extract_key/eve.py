import sys
sys.path.append('../..')

from SimulaQron.cqc.pythonLib.cqc import CQCConnection
from qkd.utils import parse_n


def main(n):
    with CQCConnection('Eve') as eve:

        for i in range(n):
            qb = eve.recvQubit()
            eve.sendQubit(qb, "Bob")


if __name__ == '__main__':
    n = parse_n()
    main(n)