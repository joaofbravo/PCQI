# The function U_f uses H, X, CNOT as cirq.H, cirq.X and cirq.CNOT
# Alternatively, you can change yield [X(qn)] to yield [cirq.X(qn)] inside the function U_f
import cirq

# This function takes as input an array of n+1 qubits, Q, where n=3
def U_f(Q):
    # We consider a simple function where f[x]=f_1[b0]+f_2[b1]+f_3[b2] mod 2
    # In this case f_1[0]=f_2[0]=f_3[0]=f_1[1]=f_2[1]=f_3[1]=1
    qn = Q[-1];
    print('f=1')
    for i in range(len(Q)-1):
       # qi = Q[i];
       yield [cirq.X(qn)]