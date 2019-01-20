# Programming a quantum network - Implementing a simple version of BB84  
  
Authors: 
- Bart van der Vecht - 4981332  
- Jurgen Dijkema - 4446984  
- Ruth Guimarey Docampo - 4935462  
- Jacobo Quintáns Castro - 4935470
  
  
## Implementation  
  
All python code is located in the `qkd` folder. In this folder, there are the following modules containing general code:   
  
- `bb84.py`: contains functions specific to the BB84 protocol, a.o. encoding/decoding BB84 states  
  
- `messages.py`: macros for messages to be sent over the classical channel  
  
- `noise.py`: functions specific for testing and error analyzing in the scenario where eve applies noise to the qubits  
  
- `reconciliation.py`: functions for information reconciliation. Uses hamming parity check matrices to compute syndromes and to estimates errors.  
  
- `utils.py`: miscellaneous functions

Furthermore, `qkd` contains a folder for each individual scenario in the exercises. They all contain a `run.sh` file, which executes the `alice.py`, `bob.py` and `eve.py` processes. These `run.sh` files should be run from their own folders, not from parent folders.
The scenarios are explained below.

## Scenarios
- `single_state` Alice encodes a single bit in a BB84 state and sends it to Bob, through Eve. Eve does not tamper with the qubit. Bob decodes the state with a random basis.
- `multiple_states` Alice encodes n bits (to be specified in `run.sh`) in BB84 states and sends them to Bob, through Eve. Eve does not tamper with the qubits. Bob decodes the states with random bases.
- `extract_key` Alice and Bob engage in the BB84 protocol starting with n states, but they do not perform error checking. Eve does not tamper with the qubits. Alice and Bob extract 1 bit of key.
- `noise_attack` Alice and Bob engage in the BB84 protocol starting with n states, but they do not perform error checking. Eve applies random gates to the qubits before sending them on to Bob. Both Alice and Bob calculate the error rate in the standard and Hadamard bases.
- `mitm_attack` Alice and Bob engage in the BB84 protocol starting with n states, but they do not perform error checking. Eve performs a man-in-the-middle attack on both the quantum channel and the classical channel. In this way, Alice and Bob successfully obtain a shared key, but now Eve also has the exact same key.
- `info_recon` Alice and Bob engage in the BB84 protocol starting with n states. Eve applies random gates before sending the qubits on to Bob. Alice and Bob check how many errors there are. If there is at most 1 error in their test bits, they perform information reconciliation, where Alice sends the Hamming syndrome of her remaining bits. Only when there is at most 1 error in the remaining bits the reconciliation will work. Note that the default number of qubits used here requires the SimulaQron setting `maxqubits_per_node` to be at least 40.

Note: when running on windows, sometimes the python processes are not killed appropriately. When errors occur when testing a certain scenario, it might help to first kill all python processes with the `killPythonProcsWin.sh` script, before running the test again.