import argparse

MSG_RECV_AND_MEAS = 1

def parse_num_bits():
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int)
    args = parser.parse_args()
    return args.n

def find_common_bases(n, bases1, bases2):
    common_bases = []
    for i in range(n):
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

def simple_extractor(n, x, r):
    key = 0
    for i in range(n):
        key = (key + (x[i] * r[i])) % 2
    return key