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
