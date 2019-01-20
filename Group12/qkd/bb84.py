from random import randint

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

def sample_subset(x):
    assert isinstance(x, list)
    indices = []
    for i in range(len(x)):
        if randint(0, 1) == 0:
            indices.append(i)

    subset = [x[i] for i in indices]
    return subset, indices

def get_remaining(x, test_indices):
    remaining = []
    for i in range(len(x)):
        if i not in test_indices:
            remaining.append(x[i])

    return remaining

def count_errors(x_test, x_test_tilde):
    return sum(i != j for i, j in zip(x_test, x_test_tilde))