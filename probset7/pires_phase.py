import cirq
import numpy as np 
import matplotlib.pyplot as plt
# define the length of the grid.


class QftInverse(cirq.Gate):
    """Quantum gate for the inverse Quantum Fourier Transformation
    """

    def __init__(self, num_qubits):
        super(QftInverse, self)
        self._num_qubits = num_qubits

    def num_qubits(self):
        return self._num_qubits

    def _decompose_(self, qubits):
        """A quantum circuit (QFT_inv) with the following structure.

        ---H--@-------@--------@----------------------------------------------
              |       |        |
        ------@^-0.5--+--------+---------H--@-------@-------------------------
                      |        |            |       |
        --------------@^-0.25--+------------@^-0.5--+---------H--@------------
                               |                    |            |
        -----------------------@^-0.125-------------@^-0.25------@^-0.5---H---

        The number of qubits can be arbitrary.
        """

        qubits = list(qubits)
        while len(qubits) > 0:
            q_head = qubits.pop(0)
            yield cirq.H(q_head)
            for i, qubit in enumerate(qubits):
                yield (cirq.CZ**(-1/2.0**(i+1)))(qubit, q_head)


def set_io_qubits(qubit_count):
    """Add the specified number of input and output qubits."""
    input_qubits = [cirq.GridQubit(i, 0) for i in range(qubit_count)]
    return input_qubits

p=(0,0.02,0.04,0.06,0.08,0.1,0.12,0.14,0.16,0.18)
qubit_count = 9
circuit_sample_count = 10

    #Set up input and output qubits.
input_qubits = set_io_qubits(qubit_count)
phi = cirq.GridQubit(qubit_count + 1, 0)
#gate = cirq.SingleQubitMatrixGate(matrix=np.array([[1, 0], [0, 1]]))

estimate = []
for k in range(10):
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q) for q in input_qubits)
    circuit.append(cirq.DepolarizingChannel(k/50).on_each(*input_qubits))
    for i in range(qubit_count):
        gate = (cirq.SingleQubitMatrixGate(matrix=np.array([[np.exp(2j), 0], [0, 1]])))**2**i
        cgate = gate.controlled_by(input_qubits[qubit_count-1-i])
        circuit.append(cgate(phi))
        circuit.append(cirq.DepolarizingChannel(k/50).on_each(*input_qubits))
    circuit.append(QftInverse(qubit_count)(*input_qubits))
    circuit.append(cirq.DepolarizingChannel(k/50).on_each(*input_qubits))

# Measure the result.
    circuit.append(cirq.measure(*input_qubits, key='phase'))


    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)

    fold_func = lambda ms: ''.join(np.flip(ms, 0).astype(int).astype(str))

    hist = result.histogram(key='phase', fold_func=fold_func)

    
    estimate_bin = hist.most_common(1)[0][0]
    estimate.append((sum([float(s)*0.5**(order+1)
        for order, s in enumerate(estimate_bin)])))
    
plt.plot(p, estimate)

print("Actual", "Estimate")
print(1/np.pi, estimate)

#print(circuit)