import argparse


def parse_n():
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int)
    args = parser.parse_args()
    return args.n

def deserialize(msg, to_list=False):
    if to_list:
        return list(msg)
    else:
        return int.from_bytes(msg, byteorder='big')

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