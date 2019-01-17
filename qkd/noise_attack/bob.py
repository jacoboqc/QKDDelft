from random import randint
import sys
sys.path.append('../..')

from SimulaQron.cqc.pythonLib.cqc import CQCConnection

from qkd.bb84 import BB84_decode, find_common_bases
from qkd.utils import deserialize, simple_extractor, parse_n
from qkd.messages import MSG_RECV_AND_MEAS
from qkd.noise import  testing, errorconversion, update_filtered


def decode(conn, qb, basis):
    if basis == 1:
        qb.H()

    return qb.measure()


def main(n):
    with CQCConnection('Bob') as bob:
        #STEP 2 BB84: Bob chooses basis string and measures qubits
        bases = [ randint(0, 1) for i in range(n) ]
        print("Bob bases:", bases)

        qubits = []

        for i in range(n):
            qubits.append(bob.recvQubit())

        bits = [ BB84_decode(qubits[i], bases[i]) for i in range(n) ]
        print("Bob bits:", bits)



        #STEP 3 BB84: Bob sends message to Alice that he has recieved the bits. 
        bob.sendClassical('Alice', MSG_RECV_AND_MEAS)



        #STEP 4 BB84: Alice and Bob tell each other their basis strings
        alice_bases = deserialize(bob.recvClassical(), to_list=True)
        assert len(alice_bases) == n, "Expected bases list of length {}".format(n)
        bob.sendClassical('Alice', bases)


        #STEP 5 BB84: Alice and Bob discard all rounds in which they didn't measure in the same basis
        common_bases = find_common_bases(bases, alice_bases)
        filtered = [bits[i] for i in common_bases]
        filt_count = len(filtered)
        

        #STEP 6 BB84: Alice picks a random subset and tells Bob
        testindex = deserialize(bob.recvClassical(), to_list=True)


        #STEP 7 BB84: Alice and Bob announce there test bitstring and compute the error
        test_bob = [filtered[i] for i in testindex]
        bob.sendClassical('Alice', test_bob)
        test_alice = deserialize(bob.recvClassical(), to_list=True) 

        e_s, e_h = testing(test_alice, test_bob, testindex, common_bases, filtered, bases)
        e_t, e_s, e_h = errorconversion(e_s, e_h, test_bob)
        print("Errors on Bob's side \nerror = {}% \nerror standard basis= {}% \nerror hadamard basis= {}% \n".format(e_t, e_s, e_h))
        filtered_update = update_filtered(testindex, filtered)



        #Finally; The remaining bits are used for the one time pad to create a 1 bit key

        seed = deserialize(bob.recvClassical(), to_list=True)
        assert len(seed) == len(filtered_update), "Expected seed of length {}, but was {}".format(len(filtered_update), len(seed))

        key = simple_extractor(filtered_update, seed)
        print("Bob key:", key)


if __name__ == '__main__':
    n = parse_n()
    main(n)