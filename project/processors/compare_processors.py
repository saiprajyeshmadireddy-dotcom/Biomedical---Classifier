import csv
import json
from pathlib import Path

from qiskit import QuantumCircuit, transpile
from qiskit.circuit import Parameter
from qiskit.transpiler import Target, InstructionProperties
from qiskit.circuit.library import CXGate, XGate, RZGate, SXGate

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parents[1]
RESULTS_DIR = ROOT_DIR / "results"
PROCESSOR_DIR = BASE_DIR


def load_processor(filename):
    with (PROCESSOR_DIR / filename).open("r", encoding="utf-8") as file:
        return json.load(file)


def build_target(config):
    num_qubits = config["num_qubits"]
    target = Target(num_qubits=num_qubits)

    # Assumption: these one-qubit gates are available on every configured qubit.
    for gate in (RZGate(Parameter("theta")), SXGate(), XGate()):
        target.add_instruction(
            gate,
            {(q,): InstructionProperties() for q in range(num_qubits)},
        )

    # Assumption: each listed coupling edge supports CX in both directions.
    directed_edges = []
    for q1, q2 in config["coupling_map"]:
        directed_edges.extend(((q1, q2), (q2, q1)))

    target.add_instruction(
        CXGate(),
        {(q1, q2): InstructionProperties() for q1, q2 in directed_edges},
    )
    return target


def main():
    # A small compilation-only circuit, not an ECG classifier.
    test_circuit = QuantumCircuit(5)
    test_circuit.h(0)
    test_circuit.cx(0, 4)
    test_circuit.cx(1, 3)
    test_circuit.cx(2, 4)

    rows = []
    for filename in ("processor_A.json", "processor_B.json"):
        config = load_processor(filename)
        target = build_target(config)
        compiled = transpile(
            test_circuit,
            target=target,
            optimization_level=0,
            seed_transpiler=42,
        )
        counts = compiled.count_ops()
        row = {
            "processor": config["name"],
            "configured_qubits": config["num_qubits"],
            "logical_circuit_qubits": test_circuit.num_qubits,
            "depth": compiled.depth(),
            "total_operations": sum(counts.values()),
            "cx_count": int(counts.get("cx", 0)),
            "swap_count": int(counts.get("swap", 0)),
            "rz_count": int(counts.get("rz", 0)),
            "sx_count": int(counts.get("sx", 0)),
            "definition_status": config.get("definition_status", "not_recorded"),
            "connectivity_assumption": "Listed edges treated as bidirectional",
        }
        rows.append(row)

        print(f"\n{config['name']}")
        print("Circuit depth:", row["depth"])
        print("Operation counts:", counts)
        print(compiled.draw())

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RESULTS_DIR / "processor_comparison.csv"
    fieldnames = list(rows[0].keys())
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # Read the file back and fail immediately if the generated artifact is malformed.
    with output_path.open("r", newline="", encoding="utf-8") as file:
        saved_rows = list(csv.DictReader(file))

    expected_processors = {"Processor A", "Processor B"}
    actual_processors = {row.get("processor") for row in saved_rows}
    if len(saved_rows) != 2 or actual_processors != expected_processors:
        raise RuntimeError(
            f"Generated comparison CSV has unexpected rows/processors: {actual_processors}"
        )

    required_columns = {
        "processor", "configured_qubits", "logical_circuit_qubits", "depth",
        "total_operations", "cx_count", "swap_count", "rz_count", "sx_count",
        "definition_status", "connectivity_assumption",
    }
    if not required_columns.issubset(saved_rows[0].keys()):
        raise RuntimeError("Generated comparison CSV is missing required columns.")

    for row in saved_rows:
        for column in (
            "configured_qubits", "logical_circuit_qubits", "depth",
            "total_operations", "cx_count", "swap_count", "rz_count", "sx_count",
        ):
            try:
                value = int(row[column])
            except (KeyError, TypeError, ValueError) as exc:
                raise RuntimeError(
                    f"Generated comparison CSV has an invalid {column} for {row.get('processor')}"
                ) from exc
            if value < 0:
                raise RuntimeError(
                    f"Generated comparison CSV has a negative {column} for {row.get('processor')}"
                )

    print(f"\nSaved and verified fresh comparison CSV: {output_path}")
    print(f"Verified {len(saved_rows)} rows and {len(required_columns)} required columns.")
    print("Note: this is a synthetic transpilation test, not a physical-hardware or ECG-classifier benchmark.")


if __name__ == "__main__":
    main()
