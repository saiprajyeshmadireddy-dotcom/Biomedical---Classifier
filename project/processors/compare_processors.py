
import json
from pathlib import Path

from qiskit import QuantumCircuit, transpile
from qiskit.transpiler import CouplingMap, Target, InstructionProperties
from qiskit.circuit.library import CXGate, HGate, XGate, RZGate, SXGate

BASE_DIR = Path(__file__).parent
PROCESSOR_DIR = BASE_DIR / "processors"


def load_processor(filename):
    with open(PROCESSOR_DIR / filename, encoding="utf-8") as f:
        return json.load(f)


def build_target(config):
    target = Target(num_qubits=config["num_qubits"])
    n = config["num_qubits"]
    connections = config["coupling_map"]

    # Add assumed one-qubit gate support on every qubit.
    for gate in [RZGate(0), SXGate(), XGate()]:
        target.add_instruction(
            gate,
            {(q,): InstructionProperties() for q in range(n)}
        )

    # Add CX only on the declared connections.
    
    # Assume each declared connection works in both directions.
    directed_connections = []
    for a, b in connections:
        directed_connections.append((a, b))
        directed_connections.append((b, a))

    target.add_instruction(
        CXGate(),
        {
            (a, b): InstructionProperties()
            for a, b in directed_connections
        }
    )

    return target


# A small test circuit with interactions across the qubits.
test_circuit = QuantumCircuit(5)
test_circuit.h(0)
test_circuit.cx(0, 4)
test_circuit.cx(1, 3)
test_circuit.cx(2, 4)
# Measurement is not needed for this compilation-only test.

for filename in ["processor_A.json", "processor_B.json"]:
    config = load_processor(filename)
    target = build_target(config)

    compiled = transpile(
        test_circuit,
        target=target,
        optimization_level=0,
        seed_transpiler=42
    )

    print(f"\n{config['name']}")
    print("Circuit depth:", compiled.depth())
    print("Total operations:", compiled.count_ops())
    print("Compiled circuit:")
    print(compiled.draw())
