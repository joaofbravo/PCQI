import random

# This is for the device
from lisbon28device import Lisbon28Device

# This is for the optimisers
from cnotopt import CNOTOptimizer, ReplaceHadamards

# Import the Grover implementation
from groverimpl import *

"""
Start mapping and optimisation
"""
qubit_count = 2
circuit_sample_count = 10

#Set up input and output qubits.
(input_qubits, output_qubit) = set_io_qubits(qubit_count)

#Choose the x' and make an oracle which can recognize it.
x_bits = [random.randint(0, 1) for _ in range(qubit_count)]
print('Secret bit sequence: {}'.format(x_bits))

# Make oracle (black box)
oracle = make_oracle(input_qubits, output_qubit, x_bits)

# Embed the oracle into a quantum circuit implementing Grover's algorithm.
# circuit = make_grover_circuit(input_qubits, output_qubit, oracle)
print('Circuit:')
circuit = cirq.Circuit.from_ops(
    make_grover_circuit(input_qubits, output_qubit, oracle),
    device=Lisbon28Device(7, 4)
)
print(circuit)

# Make sure that the Hadamards are next to the CNOT
circuit_earliest = cirq.Circuit.from_ops(circuit.all_operations())

print("\nOptimize the CNOTs")
cnotopt = CNOTOptimizer()
cnotopt.optimize_circuit(circuit_earliest)
print(circuit_earliest)

print("\nReplace Hadamards")
hopt = ReplaceHadamards()
hopt.optimize_circuit(circuit_earliest)
print(circuit_earliest)

print("\nRemove empty moments")
remempty = cirq.DropEmptyMoments()
remempty.optimize_circuit(circuit_earliest)
print(circuit_earliest)

print("\n")

circuit_earliest = cirq.Circuit.from_ops(circuit_earliest.all_operations())
print(circuit_earliest)

