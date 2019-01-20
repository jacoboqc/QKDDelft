from random import choice
import sys
sys.path.append('../..')

from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit

from qkd.utils import parse_n


def encode(conn, bit, basis):
    qb = qubit(conn)

    if bit == 1:
        qb.X()

    if basis == 1:
        qb.H()

    return qb

    #Here one can form eve's attack
def attack(qb):
    #Within choicelist one can put the gates Eve should randomly apply
    choicelist = ["X", "Z", "H", "", "", "", "", "", "", ""]
    c = choice(choicelist)
    if c == "X":
        qb.X()
    if c == "Z":
        qb.Z()
    if c == "H":
        qb.H()
    return qb, c
    


def main(n):
    with CQCConnection('Eve') as eve:

        #Eve recieves the qubits and passes them on to Bob, however 
        #She may apply some quantum gates to the qubits, which can be set
        #in the attack function

        qubits = []
        newqubits = []

        for i in range(n):
            qubits.append(eve.recvQubit())

        Evegates = []

        for i in range(n):
            new_qubit, c = attack(qubits[i])
            newqubits.append(new_qubit)
            Evegates.append(c)

        print("Eve applied following gates to the qb's: {}".format(Evegates))


        for qb in newqubits:
            eve.sendQubit(qb, 'Bob')


if __name__ == '__main__':
    n = parse_n()
    main(n)