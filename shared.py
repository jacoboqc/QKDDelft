import argparse
from SimulaQron.cqc.pythonLib.cqc import qubit

MSG_RECV_AND_MEAS = 1

def encode(conn, bit, basis):
    qb = qubit(conn)

    if bit == 1:
        qb.X()

    if basis == 1:
        qb.H()

    return qb

def decode(conn, qb, basis):
    if basis == 1:
        qb.H()

    return qb.measure()

def parse_num_bits():
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int)
    args = parser.parse_args()
    return args.n

def find_common_bases(bases1, bases2):
    assert len(bases1) == len(bases2)
    common_bases = []
    for i in range(len(bases1)):
        if bases1[i] == bases2[i]:
            common_bases.append(i)
    return common_bases

def deserialize(msg, to_list=False):
    if to_list:
        return list(msg)
    else:
        return int.from_bytes(msg, byteorder='big')

def filter_bits(bits, indices):
    filtered = []
    for i in indices:
        filtered.append(bits[i])
    return filtered

def simple_extractor(x, r):
    key = 0
    for i in range(len(x)):
        key = (key + (x[i] * r[i])) % 2
    return key

def list_sum(a, b):
    assert len(a) == len(b)
    return [ (a[i] + b[i]) % 2 for i in range(len(a)) ]

def list_to_binary_num(x):
    b = 0
    for i in range(len(x)):
        b += x[i] << (len(x) - i - 1)
    return b

def pad_len_7(x):
    padded = [0 for i in range(7)]
    for i in range(len(x)):
        padded[i] = x[i]
    return padded

def unpad_len_7(x, orig_len):
    return x[:orig_len]

HAMMING_ERROR_ESITMATE = {
    0b000: [0, 0, 0, 0, 0, 0, 0],
    0b111: [0, 0, 0, 0, 0, 0, 1],
    0b011: [0, 0, 0, 0, 0, 1, 0],
    0b101: [0, 0, 0, 0, 1, 0, 0],
    0b001: [0, 0, 0, 1, 0, 0, 0],
    0b110: [0, 0, 1, 0, 0, 0, 0],
    0b010: [0, 1, 0, 0, 0, 0, 0],
    0b100: [1, 0, 0, 0, 0, 0, 0],
}

def estimate_error(cs):
    codeword = list_to_binary_num(cs)
    return HAMMING_ERROR_ESITMATE[codeword]

def recon_decode(ca, xb):
    assert len(xb) == 7
    cb = hamming(xb)
    cs = list_sum(ca, cb)
    s_est = estimate_error(cs)
    return list_sum(xb, s_est)

def hamming(v):
    assert isinstance(v, list) and len(v) == 7
    a = (v[0] + v[2] + v[4] + v[6]) % 2
    b = (v[1] + v[2] + v[5] + v[6]) % 2
    c = (v[3] + v[4] + v[5] + v[6]) % 2
    return [a, b, c]