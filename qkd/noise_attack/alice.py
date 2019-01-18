from random import randint
import sys
sys.path.append('../..')

from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit

from qkd.bb84 import BB84_encode, find_common_bases
from qkd.utils import deserialize, simple_extractor, parse_n
from qkd.messages import MSG_RECV_AND_MEAS
from qkd.noise import testround, testing, errorconversion


def main(n):
    with CQCConnection('Alice') as alice:
    	#STEP 1 BB84: Alice creates a string x and basis string, encodes it in qubits and sends it to bob
        bits = [ randint(0, 1) for i in range(n) ]
        print("Alice bits:", bits)

        bases = [ randint(0, 1) for i in range(n) ]
        print("Alice bases:", bases)

        qubits = [ BB84_encode(alice, bits[i], bases[i]) for i in range(n) ]

        for qb in qubits:
            alice.sendQubit(qb, 'Eve')



      	#STEP 3 BB84: Alice recieves message from bob that he has measured and recieved the bits.
        msg = deserialize(alice.recvClassical())
        assert msg == MSG_RECV_AND_MEAS, "Unexpected message from Bob"




        #STEP 4 BB84: Alice and Bob tell each other their basis strings
        alice.sendClassical('Bob', bases)
        bob_bases = deserialize(alice.recvClassical(), to_list=True)
        assert len(bob_bases) == n, "Expected bases list of length {}".format(n)

        

        #STEP 5 BB84: Alice and Bob discard all rounds in which they didn't measure in the same basis
        common_bases = find_common_bases(bases, bob_bases)
        print("common bases:", common_bases)
        filtered = [bits[i] for i in common_bases]
        filt_count = len(filtered)
        print("The filtered bits are: {}".format(filtered))
        



        #STEP 6 BB84: Alice picks a random subset and tells Bob
        test_alice, testindex, filtered_update = testround(filt_count, filtered)  
        alice.sendClassical('Bob', testindex)       
        print("The indexes of filtered used for testing are: {}".format(testindex))

        #STEP 7 BB84: Alice and Bob announce there test bitstring and compute the error
        test_bob= deserialize(alice.recvClassical(), to_list=True)
        alice.sendClassical('Bob', test_alice)        
        e_s, e_h = testing(test_alice, test_bob, testindex, common_bases, filtered, bases)
        e_t, e_s, e_h = errorconversion(e_s, e_h, test_alice)     
        print("Errors on Alice's side \nerror = {}% \nerror standard basis= {}% \nerror hadamard basis= {}% \n".format(e_t, e_s, e_h))



        #STEP 8 BB84: if the error rate is not 0, Alice and Bob abort the protocol.
        if e_t > 0: 
            print("There are errors in the tested bits, the protocol will be aborted")
            exit()



        # Finally; The remaining bits are used for the one time pad to create a 1 bit key
        seed = [ randint(0, 1) for i in range(len(filtered_update)) ]
        
        print('seed:', seed)

        key = simple_extractor(filtered_update, seed)
        print("Alice key:", key)

        alice.sendClassical('Bob', seed)


if __name__ == '__main__':
    n = parse_n()
    main(n)
