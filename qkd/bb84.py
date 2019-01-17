from SimulaQron.cqc.pythonLib.cqc import qubit

def BB84_encode(conn, bit, basis):
    qb = qubit(conn)

    if bit == 1:
        qb.X()

    if basis == 1:
        qb.H()

    return qb

def BB84_decode(qb, basis):
    if basis == 1:
        qb.H()

    return qb.measure()

def find_common_bases(bases1, bases2):
    assert len(bases1) == len(bases2)
    common_bases = []
    for i in range(len(bases1)):
        if bases1[i] == bases2[i]:
            common_bases.append(i)
    return common_bases
