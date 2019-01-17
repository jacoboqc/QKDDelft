from SimulaQron.cqc.pythonLib.cqc import CQCConnection


def main():
    with CQCConnection('Eve') as eve:

        qb = eve.recvQubit()
        eve.sendQubit(qb, "Bob")


if __name__ == '__main__':
    main()