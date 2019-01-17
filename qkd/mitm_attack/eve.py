import sys
sys.path.append('../..')

from SimulaQron.cqc.pythonLib.cqc import CQCConnection

from qkd.bb84 import BB84_encode, BB84_decode, find_common_bases
from qkd.utils import parse_n, deserialize, simple_extractor


def main(n):
    with CQCConnection('Eve') as eve:
        qubits = []

        for i in range(n):
            qubits.append(eve.recvQubit())

        theta = deserialize(eve.recvClassical(), to_list=True)
        measurements = [BB84_decode(qubits[i], theta[i]) for i in range(n)]

        newQubits = [BB84_encode(eve, measurements[i], theta[i]) for i in range(n)]

        for qb in newQubits:
            eve.sendQubit(qb, "Bob")

        eve.sendClassical("Bob", theta)

        theta_tilde = deserialize(eve.recvClassical(), to_list=True)

        theta_common = find_common_bases(theta, theta_tilde)

        x_remain = [measurements[i] for i in theta_common]

        eve.sendClassical("Alice", theta_tilde)

        seed = deserialize(eve.recvClassical(), to_list=True)
        key = simple_extractor(x_remain, seed)

        print("> (Eve) The key is: {}".format(key))
        eve.sendClassical("Bob", seed)


if __name__ == '__main__':
    n = parse_n()
    main(n)
