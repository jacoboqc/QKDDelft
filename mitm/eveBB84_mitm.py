from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit


def main():
    n = 10

    with CQCConnection("Eve") as Eve: 
        qubits = []
        measurements = []
        for i in range(0, n):
            q = Eve.recvQubit()
            qubits.append(q)
        
        theta = Eve.recvClassical()
        
        for i in range(0, n):
            q = qubits[i]
            if theta[i] == 1:
                q.H()
            m = q.measure()
            measurements.append(m)
            
        for i in range(0, n):
            q = qubit(Eve)
            if theta[i] == 1:
                q.H()
            if measurements[i] == 1:
                q.X()
            Eve.sendQubit(q, "Bob")
        
        Eve.sendClassical("Bob", list(theta))
        theta_tilde = Eve.recvClassical()
        
        S = []
        for i in range(n):
            if theta[i] == theta_tilde[i]:
                S.append(theta[i])
        
        Eve.sendClassical("Alice", list(theta_tilde))
        
        r = Eve.recvClassical()
        k = 0
        for i in range(len(S)):
            k = (k + S[i] + r[i]) % 2

        print("> (Eve) The key is: {}".format(k))
        Eve.sendClassical("Bob", list(r))


if __name__ == '__main__':
    main()
