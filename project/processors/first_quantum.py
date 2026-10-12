
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Create a circuit with 1 qubit and 1 classical bit
circuit = QuantumCircuit(1, 1)

# Put the qubit into a superposition
circuit.h(0)

# Measure the qubit
circuit.measure(0, 0)

# Run the circuit on a simulator
simulator = AerSimulator()
job = simulator.run(circuit, shots=1000)
result = job.result()

print("Quantum circuit:")
print(circuit.draw())
print("Measurement results:")
print(result.get_counts())
