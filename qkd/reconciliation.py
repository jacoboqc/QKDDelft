import numpy as np

def list_sum(a, b):
    assert len(a) == len(b)
    return [ (a[i] + b[i]) % 2 for i in range(len(a)) ]

def list_to_binary_num(x):
    b = 0
    for i in range(len(x)):
        b += x[i] << (len(x) - i - 1)
    return b

def pad(x, n):
    padded = [0 for i in range(n)]
    for i in range(min(len(x), n)):
        padded[i] = x[i]
    return padded


HAMMING_PARITY_CHECK_3 = np.array(
    [[1, 1, 0],
     [1, 0, 1]]
)

HAMMING_ERROR_ESTIMATE_3 = {
    0b00: [0, 0, 0],
    0b01: [0, 0, 1],
    0b10: [0, 1, 0],
    0b11: [1, 0, 0],
}


HAMMING_PARITY_CHECK_7 = np.array(
    [[1, 1, 1, 0, 1, 0, 0],
     [1, 1, 0, 1, 0, 1, 0],
     [1, 0, 1, 1, 0, 0, 1]]
)

HAMMING_ERROR_ESTIMATE_7 = {
    0b000: [0, 0, 0, 0, 0, 0, 0],
    0b001: [0, 0, 0, 0, 0, 0, 1],
    0b010: [0, 0, 0, 0, 0, 1, 0],
    0b100: [0, 0, 0, 0, 1, 0, 0],
    0b011: [0, 0, 0, 1, 0, 0, 0],
    0b101: [0, 0, 1, 0, 0, 0, 0],
    0b110: [0, 1, 0, 0, 0, 0, 0],
    0b111: [1, 0, 0, 0, 0, 0, 0],
}

HAMMING_PARITY_CHECK_11 = np.array(
    [[1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0],
     [0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0],
     [1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0],
     [1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1]]
)

HAMMING_ERROR_ESTIMATE_11 = {
    0b0000: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    0b0001: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    0b0010: [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    0b0100: [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    0b1000: [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    0b0011: [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    0b0101: [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    0b0110: [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    0b0111: [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    0b1001: [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    0b1010: [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    0b1011: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

    # not used:
    0b1100: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    0b1101: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    0b1110: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    0b1111: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}

def estimate_error(cs):
    bin = list_to_binary_num(cs)
    return ERROR_ESTIMATE_LISTS[len(cs)][bin]

def recon_decode(ca, xb):
    cb = hamming_syndrome(xb)
    cs = list_sum(ca, cb)
    s_est = estimate_error(cs)
    s_est = s_est[:len(xb)]
    return list_sum(xb, s_est), s_est

PARITY_MATRICES = {
    3: HAMMING_PARITY_CHECK_3,
    7: HAMMING_PARITY_CHECK_7,
    11: HAMMING_PARITY_CHECK_11,
}

ERROR_ESTIMATE_LISTS = {
    2: HAMMING_ERROR_ESTIMATE_3,
    3: HAMMING_ERROR_ESTIMATE_7,
    4: HAMMING_ERROR_ESTIMATE_11,
}

def hamming_syndrome(v):
    if len(v) <= 3:
        x = pad(v, 3)
        n = 3
    elif len(v) <= 7:
        x = pad(v, 7)
        n = 7
    elif len(v) <= 11:
        x = pad(v, 11)
        n = 11
    else:
        assert False, "codeword longer than 11 bits"

    arr = np.array(x)
    parity_matrix = PARITY_MATRICES[n]
    codeword = parity_matrix.dot(arr).tolist()
    codeword = [cw % 2 for cw in codeword]
    return codeword
